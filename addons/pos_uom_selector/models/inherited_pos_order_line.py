from odoo import models, fields, api

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_uom2_id = fields.Many2one('uom.uom', string='Product UoM')
    product_uom_effective_id = fields.Many2one(
        'uom.uom',
        string='UoM',
        compute='_compute_uom_effective',
        store=False  # Set to True if you want to filter/sort in backend views
    )

    @api.depends('product_uom2_id', 'product_uom_id')
    def _compute_uom_effective(self):
        for line in self:
            line.product_uom_effective_id = line.product_uom2_id or line.product_uom_id