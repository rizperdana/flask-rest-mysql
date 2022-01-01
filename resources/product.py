from flask import request
from flask_restx import Resource, fields, Namespace
from models.product import ProductModel
from schemas.product import ProductSchema
import datetime

PRODUCT_NOT_FOUND = "Product not found."
PRODUCT_ALREADY_EXISTS = "Product '{}' Already exits"

product_ns = Namespace('product', description = 'Product related operations')
products_ns = Namespace('products', description = 'Products related operations')
product_schema = ProductSchema()
product_list_schema = ProductSchema(many = True)

product = products_ns.model('Product', {
  'id' : fields.Integer('ID of the product e.g: 1'),
  'name' : fields.String('Product name e.g: Potato'),
  'description' : fields.String('Product description e.g: "This potato with extra step"'),
  'images' : fields.Integer('Image id used on product e.g: 1'),
  'logo_id' : fields.Integer('Logo used on product e.g" 2'),
  'created_at' : fields.DateTime(datetime.datetime.now()),
  'updated_at' : fields.DateTime(datetime.datetime.now())
})

class Product(Resource):
  @product_ns.doc('Get product by id')
  def get(self, id):
    product_data = ProductModel.find_by_id(id)
    if product_data:
      return product_schema.dump(product_data)
    return {'message': PRODUCT_NOT_FOUND}, 404

  @product_ns.doc('Delete product by id')
  def delete(self, id):
    product_data = ProductModel.find_by_id(id)
    if product_data:
      product_data.delete_from_db()
      return {'message': "Product deleted successfully"}, 201
    return {'message': PRODUCT_NOT_FOUND}, 404

class ProductList(Resource):
  @products_ns.doc('Get all Products')
  def get(self):
    return product_list_schema.dump(ProductModel.find_all()), 200
  
  @products_ns.expect(product)
  @products_ns.doc('Create a Product')
  def post(self):
    data = request.get_json()
    if ProductModel.find_by_name(data['name']):
      return {'message': PRODUCT_ALREADY_EXISTS.format(data['name'])}, 400
    product_data = product_schema.load(data)
    product_data.save_to_db()

    return product_schema.dump(product_data), 200