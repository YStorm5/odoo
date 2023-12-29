from odoo import fields,models,api
import ipdb
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate proptery offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(copy=False,selection=[("accepted","Accepted"),("refused","Refused")])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("estate.property",required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id",store=True)
    validity = fields.Integer(default=7,string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_validity",inverse="_compute_date_deadline")
    _sql_constraints = [
        ("check_price_positive","CHECK(price > 0)","An offer price must be strictly positive"),
    ]
    
    # Compute method
    @api.depends("validity")
    def _compute_validity(self):
        for rec in self:
            create_date = fields.Date.today() if rec.create_date == False else rec.create_date
            rec.date_deadline = create_date + relativedelta(days=rec.validity)
            
    def _compute_date_deadline(self):
        for rec in self:
            valid = rec.date_deadline - fields.Date.to_date(rec.create_date)
            rec.validity = valid.days
    
    # Action
    def accepted_offer(self):
        for rec in self:
            if not rec.property_id.selling_price > 0:
                rec.status = "accepted"
                rec.property_id.selling_price = rec.price
                rec.property_id.buyer = rec.partner_id
                rec.property_id.state = 'offer accepted'
            else:
                raise UserError("One offer has already been accepted.")
        return True
    
    def refused_offer(self):
        for rec in self:
            rec.status = "refused"
        return True
    
    # Overriding CRUD
    
    @api.model
    def create(self,vals):
        prop = self.env['estate.property'].browse(vals['property_id'])
        if prop.state == 'new':
            prop.state = "offer received"
        if vals["price"] < prop.best_price:
            raise UserError(f"The offer must be higher than {prop.best_price}")
        return super().create(vals)