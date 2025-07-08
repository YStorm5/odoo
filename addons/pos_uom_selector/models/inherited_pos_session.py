from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_uom_price(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['product_tmpl_id', 'uom_id', 'price'],
            }
        }

    def _get_pos_ui_product_uom_price(self, params):
        return self.env['product.uom.price'].search_read(**params['search_params'])

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('product.uom.price')
        return result