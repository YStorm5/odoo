from odoo.http import AccessDenied,AccessError, Controller, UserError,route,Response,request,json

class EstateController(Controller):
    
    @route('/login', type='http', auth='public', methods=['POST'], csrf=False)
    def generate_token(self):
        try: 
            req = dict(request.httprequest.json)
            username = req.get("username")
            password = req.get("password")
            db = request.env.cr.dbname
            uid = request.session.authenticate(db, username, password)
            if not uid:
                raise AccessDenied("Invalid username or password")
            env = request.env(user=request.env.user.browse(uid))
            env['res.users.apikeys.description'].check_access_make_key()
            token = env['res.users.apikeys']._generate("rpc", username)
            return request.make_json_response(data={"message":"Login successfully","token": token},status=200)
        except Exception as e:
            return Response(json.dumps({"status":"error","message":str(e).replace('"','')}), status=400,content_type="application/json")
    
    @route(["/estate","/estate/<int:route_id>"],type="http",methods=['GET','POST','PUT','DELETE'], auth='bearer',csrf=False)
    def get_estate(self,route_id=None):
        try: 
            
            # Get all Estate
            if request.httprequest.method == 'GET':
                list_estate = []
                params = dict(request.params)
                rec_id = params.get('id') if params.get('id') != None else route_id
                estates = request.env['estate.property'].search([]) if rec_id == None else request.env['estate.property'].browse(int(rec_id))
                for estate in estates:
                    list_estate.append({
                        "id":estate.id,
                        "name":estate.name,
                        "description":estate.description,
                        "bedrooms":estate.bedrooms,
                        "price":estate.expected_price,
                    })
                return request.make_json_response(data=list_estate if len(list_estate) > 1 else list_estate[0],status=200)
                # return Response(json.dumps(list_estate if len(list_estate) > 1 else list_estate[0]),content_type="application/json") 
            
            # Create Estate or Update Estate
            else:
                req = dict(request.httprequest.json)
                name = req.get('name')
                description = req.get('description')
                expected_price = req.get('price')
                bedrooms = req.get("bedroom")
                id = req.get("id")
                
                if request.httprequest.method == "POST":
                    if not name or not expected_price:
                        message = f"The field {'name' if name == None else 'price'} is required."
                        raise UserError(message)                 
                    request.env['estate.property'].create({
                        'name': name,
                        'description': description,
                        'expected_price': expected_price,
                        'selling_price': (expected_price * 0.5),
                        'bedrooms' : bedrooms
                    })
                    return request.make_json_response(data={"message":"Successfully create an estate."},status=200)
                
                if id != None:
                    estate = request.env["estate.property"].browse(id)
                    if not estate.exists():
                        return Response(json.dumps({'status': 'error', 'message': f'Estate with id={id} not found.'}), status=404,content_type="application/json")
                    if request.httprequest.method == "PUT":
                        req['selling_price'] = req['price'] * 0.5
                        req['expected_price'] = req.pop('price')
                        req.pop('id')
                        estate.update(req)
                        return request.make_json_response(data={"message": "Estate has been updated."},status=200)
                    if request.httprequest.method == "DELETE":
                        estate.unlink()
                        return request.make_json_response(data={"message": "Estate has been deleted."},status=200)
                return request.make_json_response(data={"message":"The field 'id' is required."},status=400)
        except Exception as e:
            return Response(json.dumps({"status":"error","message":str(e).replace('"','')}), status=401 if isinstance(e,AccessError) else 400,content_type="application/json")