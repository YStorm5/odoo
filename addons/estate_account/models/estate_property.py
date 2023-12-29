from odoo import models,fields,api,Command

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def sold_property(self):
        self.env["account.move"].create({
            "partner_id":self.buyer.id,
            "move_type":"out_invoice",
            "invoice_line_ids":[
                Command.create({
                    "name":self.name,
                    "quantity":"1",
                    "price_unit":self.selling_price * 0.06,
                }),
                Command.create({
                    "name":"administrative fees",
                    "quantity":"1",
                    "price_unit":"100"
                })
            ]
        })
        return super(EstateProperty,self).sold_property()