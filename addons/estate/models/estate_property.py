from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_is_zero

import ipdb

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate proptery"
    _order = "id desc"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=lambda x: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price",required=True)
    selling_price = fields.Float("Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(string="Garden Orientation", \
        selection=[('north','North'),('south','South'),('east','East'),('west','West')]
        )
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new','New'),('offer received','Offer Received')\
        ,('offer accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],default='new')
    
    property_type_id = fields.Many2one("estate.property.type",string="Type")
    salesperson = fields.Many2one("res.users",default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner",copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer","property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    _sql_constraints = [
        ("check_expected_price_positive","CHECK(expected_price > 0)","A property expected price must be strictly positive"),
        ("check_selling_price_positive","CHECK(selling_price >= 0)","A property selling price must be positive"),
    ]
    
    # Compute Method
    
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
       for line in self:
            line.best_price = max(line.offer_ids.mapped("price")) if len(line.offer_ids.mapped("price")) != 0 else 0
            # if line.state != "sold" and line.state != 'canceled' and line.state != 'offer accepted':
            #     if not float_is_zero(line.best_price,2):
            #         line.state = "offer received"
            
    # Onchange Method
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_orientation = "north"
            self.garden_area = "10"
        elif self.garden == False:
            self.garden_area = ""
            self.garden_orientation = ""
            return {'warning': {
                'title': "Warning",
                'message': 'Garden is set back to False'
                ,'type':'notification'}}

    # Action
    
    def sold_property(self):
        for rec in self:
            if rec.state != "canceled":
                rec.state = "sold"
            else:
                raise UserError("Canceled Properties can't be sold.")
        return True
        
    def cancel_property(self):
        for rec in self:
            if rec.state != "sold":
                rec.state = "canceled"
            else:
                raise UserError("Sold Properties can't be canceled.")
        return True
    
    # Constrain
    
    @api.constrains('selling_price','expected_price')
    def check_ninety_percent(self):
        for rec in self:
            if not float_is_zero(rec.selling_price,2):
                if rec.selling_price < (rec.expected_price * 0.9):
                    raise ValidationError("Selling price cannot be lower than 90 percent of the expected price")
                
    # Override CRUD
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_cancel(self):
        for rec in self:
            if rec.state != "new" and rec.state != "canceled":
                raise UserError("Can only delete new or canceled property!")