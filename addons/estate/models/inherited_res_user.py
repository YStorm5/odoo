from odoo import models,fields

class InheritedResUser(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many("estate.property","salesperson",domain="property_ids.state == 'new' or property_ids.state == 'offer received'")