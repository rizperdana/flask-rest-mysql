from flask import request
from flask_restx import Resource, fields, Namespace
from models.product import ProductModel
from schemas.product import ProductSchema
from datetime import datetime

PRODUCT_NOT_FOUND = "Product not found."
PRODUCT_ALREADY_EXISTS = "Product '{}' Already exits"

api = Namespace('product', description = 'Product related operations')
product_schema = ProductSchema()
product_list_schema = ProductSchema(many = True)

product = api.model('Product', {
  'name' : fields.String(required = True, description = 'Product name e.g: Potato'),
  'description' : fields.String(description = 'Product description e.g: "This potato with extra step"'),
  'images' : fields.Integer(description = 'Image id used on product e.g: 1'),
  'logo_id' : fields.Integer(description = 'Logo used on product e.g" 2'),
})

@api.route('/')
class ProductList(Resource):
  @api.doc('Get all Products')
  def get(self):
    return product_list_schema.dump(ProductModel.query.all()), 200
  
  @api.doc('Create a Product')
  @api.expect(product)
  def post(self):
    data = request.get_json()
    if ProductModel.find_by_name(data['name']):
      return {'message': PRODUCT_ALREADY_EXISTS.format(data['name'])}, 400
    product_data = product_schema.load(data)
    product_data.post_to_db()

    return product_schema.dump(product_data), 200

@api.route('/<int:id>')
@api.response(404, 'Product not found')
@api.param('id', 'Product identifier')
class Product(Resource):
  @api.doc('Get Products by id')
  def get(self, id):
    product_data = ProductModel.find_by_id(id)
    if product_data:
      return product_schema.dump(product_data)
    return {'message': PRODUCT_NOT_FOUND}, 404

  @api.doc('Update product')
  @api.expect(product)
  def put(self, id):
    data = request.get_json()
    query = ProductModel.query.get_or_404(id)

    if (data['name'])         : query.name = data['name']
    if (data['description'])  : query.description = data['description']
    if (data['images'])       : query.images = data['images']
    if (data['logo_id'])      : query.logo_id = data['logo_id']
    query.put_to_db()

    return product_schema.dump(query), 200

  @api.doc('Delete Products by id')
  def delete(self, id):
    product_data = ProductModel.find_by_id(id)
    if product_data:
      product_data.delete_from_db()
      return {'message': "Product deleted successfully"}, 201
    return {'message': PRODUCT_NOT_FOUND}, 404
