# © 2016 Yannick Vaucher (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    """Compute product price including a building site pricelist if defined."""

    _inherit = 'product.product'

    def _compute_product_price(self):
        """Use project pricelist if available."""
        final_prices = {}
        list_prices = {}
        # Get the project_pricelist from context.
        # This is an additional pricelist which can be defined additionaly
        # to the one on the sale order
        project_pricelist_id = self.env.context.get('project_pricelist')
        # Compute the price with the standard pricelist.
        super()._compute_product_price()
        if project_pricelist_id:
            # We want to make sure we do not write as we would get wrong
            # results and also it would slow it down.
            with self.env.do_in_draft():
                for item in self:
                    # Save the original list_price back
                    # since we need to reset it later.
                    list_prices[item.id] = item.list_price
                    # set our custom pricelist as the pricelist
                    new_item = item.with_context(
                        pricelist=project_pricelist_id
                    )
                    # We want to set the list_price of the price of the
                    # original one, so that we will chain the pricelists
                    # instead of just getting a second price based on
                    # the original list_price.
                    new_item.list_price = item.price
                    _super = super(ProductProduct, new_item)
                    # Compute the new price with the project_pricelist
                    _super._compute_product_price()
                    final_prices[new_item.id] = new_item.price
            for item in self:
                # write the price back and reset the list_price,
                # because the inverse function is called and miscalculates,
                # since it doesn't account for the two pricelists
                item.update({
                    'price': final_prices[item.id],
                    'list_price': list_prices[item.id]
                })
