# -*- coding: utf-8 -*-

import random
import json
from odoo.http import Response,Controller,route,request

class AwesomeGallery(Controller):
    @route('/awesome_gallery/test',type="http",methods=['GET'], auth='public',cors="*")
    def get_test(self):
        data = {
            "name":"prakas",
            "email":"prakashsharmacs24@gmail.com",
            "phone":"+917123456"
        }
        return Response(json.dumps(data),content_type='application/json')

    @route('/currency',type="http",auth="public")
    def hello_world(self):
        # get all currency from db
        currencys = request.env["res.currency"].sudo().with_context(active_test=False).search([])
        list_cur = []
        for cur in currencys:
            list_cur.append({
                "name":cur.name,
                "symbol":cur.symbol,
                "fullname":cur.full_name, 
                "unit": cur.currency_unit_label
            })
        return Response(json.dumps(list_cur),content_type='application/json')
