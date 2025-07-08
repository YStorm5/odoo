from odoo import models, fields

class ProductUomPrice(models.Model):
    _name = 'product.uom.price'
    _description = 'Product UOM Price'

    product_tmpl_id = fields.Many2one('product.template', required=True)
    uom_id = fields.Many2one('uom.uom', required=True)
    price = fields.Float(string="Price", required=True)