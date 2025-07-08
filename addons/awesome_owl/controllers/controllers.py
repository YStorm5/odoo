from odoo import http
from odoo.http import request, route

class OwlPlayground(http.Controller):
    @http.route(['/awesome_owl'], type='http', auth='user')
    def show_playground(self):
        """
        Renders the owl playground page
        """
        data = {
            "name":"Testing"
        }
        return request.render('awesome_owl.playground',data)
