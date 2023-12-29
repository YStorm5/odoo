from odoo import fields,models,api
import ipdb

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate proptery type"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    sequence = fields.Integer("Sequence")
    _sql_constraints = [
        ("estate_property_type_unique","unique(name)","A property type name name must be unique")
    ]
    
    # Computed action
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)