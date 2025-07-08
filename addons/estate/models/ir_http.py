import re
from odoo.http import datetime, request,Response,json, timedelta
from odoo.models import AbstractModel
from odoo.exceptions import AccessDenied
from werkzeug.exceptions import HTTPException


class JsonException(HTTPException):
    def __init__(self, message="You are not authenticated",status=403, **kwargs):
        super().__init__()
        self.description = message
        self.code = status

    def get_response(self, environ=None):
        response = Response(
            status=self.code,
            content_type="application/json",
            response=json.dumps({"error": self.description})
        )
        return response

class IrHttp(AbstractModel):
    _inherit = 'ir.http'
    
    def validate_token(self):
        headers = request.httprequest.headers
        header = headers.get("Authorization")
        if request.uid != None:
            return True
        if header and (m := re.match(r"^bearer\s+(.+)$", header, re.IGNORECASE)):
            uid = request.env['res.users.apikeys']._check_credentials(scope='rpc', key=m.group(1))
            if not uid:
                raise AccessDenied("Invalid apikey")
            else:
                keys = request.env['res.users.apikeys'].sudo().search([('user_id', '=', uid)])
                for key in keys:
                    if datetime.now() >= key['create_date'] + timedelta(minutes=60): # change lifetime here 5 minutes
                        key.sudo().unlink()
                    else:
                        if key._check_credentials(scope='rpc', key=m.group(1)):
                            request.update_env(user=uid)
                            return True
                raise AccessDenied("Token is expired.")
        else:
            raise AccessDenied("User is not authenticated.")

    @classmethod
    def _auth_method_bearer(cls):
        try:
            cls.validate_token(cls)
        except AccessDenied as e:
            raise JsonException(str(e),403)