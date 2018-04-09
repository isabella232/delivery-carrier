# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.osv import expression


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    e_nr = fields.Char("E-Nr", copy=False)

    transit_qty = fields.Float(
        compute='_get_transit_qty',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Transit'
    )

    product_class = fields.Many2one('product.class', string='Product Class')

    color_code = fields.Many2one(
        'product.color.code',
        string='Color Code NCS/RAL'
    )

    harmsys_code = fields.Many2one(
        'product.harmsys.code',
        string='Harmonized System Code'
    )

    manual_code = fields.Many2one(
        'product.manual.code',
        string='Manual Code'
    )

    export_to_pim = fields.Boolean(
        default=False,
        string='PIM',
    )

    _sql_constraints = [
        ('e_nr_unique', 'unique(e_nr)',
         'E-Nr should be unique'),
    ]

    @api.depends('virtual_available')
    def _get_transit_qty(self):
        """Compute the quantity of product that is in transit.
        """
        for tmpl in self:
            tmpl.transit_qty = sum(
                product.transit_qty for product in tmpl.product_variant_ids
            )

    @api.multi
    def action_transit_move(self):
        """ Return stock.move list view for this product filtered by
        Transit from China location.
        """
        self.ensure_one()

        transit_loc = self.env.ref('scenario.location_transit_cn')

        context = self.env.context.copy()
        context['search_default_product_id'] = self.product_variant_ids[0].id
        # In stock_view.xml, location search name is "name"....
        context['search_default_name'] = transit_loc.complete_name

        return {
            'name': 'Transit moves',
            'type': 'ir.actions.act_window',
            'view_type': 'list',
            'view_mode': 'list',
            'res_model': 'stock.move',
            'target': 'current',
            'view_id': self.env.ref('stock.view_move_tree').id,
            'context': context,
        }

    @api.depends('seller_ids',
                 'seller_ids.product_code')
    def _get_supplier_code_name(self):
        '''
        It will concatenate the product reference of suppliers
        '''
        res = {}
        for product in self:
            supplier_name = []
            for supplier in product.seller_ids:
                if supplier.product_code:
                    supplier_name.append(supplier.product_code)
            res[product.id] = '/'.join(supplier_name)
        return res

    def _supplier_code_name_search(self, operator, operand):
        product_supplier_obj = self.env['product.supplierinfo']
        product_supplier_product = product_supplier_obj.search_read(
            [('product_code', operator, operand)], ['product_tmpl_id'])
        if product_supplier_product:
            return_vals = [x['product_tmpl_id'][0] for x in
                           product_supplier_product]
            return [('id', 'in', tuple(return_vals))]
        else:
            return [('id', '=', 0)]

    supplier_code_name = fields.Char(compute='_get_supplier_code_name',
                                     string="Supplier Code",
                                     search='_supplier_code_name_search')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(readonly=True)

    transit_qty = fields.Float(
        compute='_get_transit_qty',
        digits=dp.get_precision('Product Unit of Measure'),
        string='Transit'
    )

    @api.depends('virtual_available')
    def _get_transit_qty(self):
        """Compute the quantity of product that is in transit.
        """
        move_model = self.env['stock.move']

        transit_loc = self.env.ref('scenario.location_transit_cn')

        domain = None
        if transit_loc:
            domain = [
                ('state', 'not in', ('done', 'cancel', 'draft', 'waiting')),
                ('location_id', '=', transit_loc.id)
            ]

        for product in self:
            if not domain or not product.virtual_available:
                product.transit_qty = 0
            else:
                transit_moves = move_model.search(
                    domain + [('product_id', '=', product.id)]
                )
                product.transit_qty = sum(
                    move.product_qty for move in transit_moves
                )

    @api.model
    def create(self, vals):
        """ Fill default_code (if needed) with new sequence value.
        """
        if not vals.get('default_code'):
            vals['default_code'] = self.env['ir.sequence'].next_by_code(
                'product.product'
            )
        return super().create(vals)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['default_code'] = False
        return super().copy(default)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """ Allow to search by E-Nr or internal ref """
        args = args or []
        filter_known = []
        products = self.browse()
        if name:

            for search_field in ['e_nr', 'default_code']:
                if limit is None or limit > 1:
                    domain = [(search_field, '=ilike', name + '%')]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = ['&'] + domain
                    domain = filter_known + domain
                    recs = self.search(domain + args, limit=limit)
                    if limit is not None:
                        limit -= len(recs)
                    products |= recs
                    if products:
                        filter_known = [('id', 'not in', products.ids)]

        name_result = super().name_search(
            name, args=filter_known + args, operator=operator, limit=limit)

        if products:
            result = products.name_get()
            name_result = name_result
            result.extend(name_result)
            return result
        return name_result

    @api.multi
    def action_transit_move(self):
        """ Return stock.move list view for this product filtered by
        Transit from China location.
        """
        return self.product_tmpl_id.action_transit_move()
