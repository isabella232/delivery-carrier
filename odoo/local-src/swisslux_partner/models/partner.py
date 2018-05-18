# Copyright 2015 Swisslux
# Copyright 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('is_company', 'name', 'parent_id.name', 'type',
                 'company_name', 'parent_id', 'ref', 'city')
    def _compute_display_name(self):
        super()._compute_display_name()

    ref = fields.Char('Code', readonly=True)
    parent_category_id = fields.Many2many(
        related='parent_id.category_id',
        string="Tags parent",
        store=False,
        readonly=True
    )
    name2 = fields.Char('Additional name')

    eori_number = fields.Char("EORI number")

    # EEV infos
    eev_member = fields.Boolean('EEV-Mitglied')
    eev_number = fields.Char('EEV Nr.')
    eev_alarm = fields.Boolean('Haftungsablehnung')

    # PO box
    pobox_nr = fields.Char('PO Box Nr')
    pobox_zip = fields.Char('PO Box Zip')
    pobox_city = fields.Char('PO Box City')

    companytype = fields.Selection(
        (('headquarter', 'Hauptsitz'),
         ('branch', 'Filiale')),
        'Firmen Typ'
    )
    headquarter_id = fields.Many2one(
        'res.partner',
        'Headquarter',
        ondelete='set null'
    )

    partner_shipping_id = fields.Many2one(
        'res.partner',
        'Shipping Partner',
        ondelete='set null'
    )
    partner_invoicing_id = fields.Many2one(
        'res.partner',
        'Invoicing Partner',
        ondelete='set null'
    )

    mailing = fields.Selection(
        (('0', 'keine Dokus'),
         ('1', '1 Exemplar'),
         ('5', '5 Exemplare'),
         ('10', '10 Exemplare'),
         ('25', '25 Exemplare'),
         ('50', '50 Exemplare'),
         ('100', '100 Exemplare')),
        'Dokuversand'
    )
    mailing_email = fields.Selection(
        (('0', 'abmelden'),
         ('1', 'anmelden')),
        'E-Mail Newsletter'
    )

    department = fields.Char('Department')
    partner_state = fields.Selection(
        [('qualified', 'qualifiziert'),
         ('potential_partner', 'potenzieller Partner'),
         ('active', 'aktiv begleitet'),
         ],
        'Partnerstatus'
    )

    influence = fields.Selection(
        [('installer_a', 'Installateur A'),
         ('installer_b', 'Installateur B'),
         ('installer_c', 'Installateur C'),
         ('planer_a', 'Planer A'),
         ('planer_b', 'Planer B'),
         ('planer_c', 'Planer C'),
         ('wholesale_a', 'Grosshandel A'),
         ('wholesale_b', 'Grosshandel B'),
         ('wholesale_c', 'Grosshandel C'),
         ('key_contact', 'Schluesselkontakt')],
        'Einfluss')

    region_id = fields.Many2one('res.partner.region', "Verkaufsgebiet")

    _sql_constraints = [
        ('res_partner_unique_ref', 'unique(ref)', 'This code already exists')
    ]

    @api.model
    def create(self, vals):
        """Define customer code"""
        if not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'res.partner'
            )

        return super(ResPartner, self).create(vals)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        result = None
        if name:
            domain = [('ref', '=ilike', name + '%')]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&'] + domain
            partners = self.search(domain + args, limit=limit)
            result = partners.name_get()
        if not result:
            result = super(ResPartner, self).name_search(
                name, args=args, operator=operator, limit=limit)
        return result

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name or ''
            if self.env.context.get('show_address') or\
                    self.env.context.get('uid'):
                if record.ref and record.city:
                    name = '{}, {}  ({})'.format(name, record.city, record.ref)
                elif record.ref:
                    name = '{} ({})'.format(name, record.ref)
                elif record.city:
                    name = '{}, {}'.format(name, record.city)
            if record.parent_id and not record.is_company:
                if not name and record.type in ['invoice',
                                                'delivery',
                                                'other']:
                    name = dict(self.fields_get()['type']
                                ['selection'])[record.type]
                name = "%s, %s" % (record.parent_name, name)
            if self.env.context.get('show_address_only'):
                name = record._display_address(without_company=True)
            if self.env.context.get('show_address'):
                name = name + "\n" + record._display_address(
                    without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self.env.context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            if self.env.context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((record.id, name))
        return res

    @api.onchange('zip_id')
    def onchange_zip_set_region_and_user(self):
        if self.zip_id:
            self.region_id = self.zip_id.region_id
            self.user_id = self.zip_id.user_id

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['ref'] = self.env['ir.sequence'].next_by_code(
            'res.partner'
        )
        return super(ResPartner, self).copy(default)

    @api.multi
    def write(self, vals):
        # Check if partner that we modify have active switch to false
        # if it's a company we will deactivate all related contacts
        if 'active' in vals and not vals['active']:
            for current_partner in self:
                if current_partner.child_ids:
                    current_partner.child_ids.write({'active': False})
        result = super(ResPartner, self).write(vals)
        return result
