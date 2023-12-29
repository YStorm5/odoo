from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property tag"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer("Color")
    _sql_constraints = [
        ("estate_property_tag_unique","unique(name)","A property tag name name must be unique")
    ]