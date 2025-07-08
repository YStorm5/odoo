from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.template'

    uom_price_ids = fields.One2many('product.uom.price', 'product_tmpl_id', string='UOM Prices')
    multi_uom_ok = fields.Boolean(string='Multiple UOMs',default=False)