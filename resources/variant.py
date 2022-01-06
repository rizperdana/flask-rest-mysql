from flask import request
from flask_restx import Resource, fields, Namespace
from models.variant import VariantModel
from models.product import ProductModel
from models.image import ImageModel
from schemas.variant import VariantSchema

VARIANT_NOT_FOUND = "Variant not found."
IMAGE_NOT_FOUND = "Image not found."
PRODUCT_ID_NOT_FOUND = "Product id not found."

api = Namespace('variant', description = 'Variant related operations')
variant_schema = VariantSchema()
variant_list_schema = VariantSchema(many = True)

variant = api.model('Variant', {
  'product_id' : fields.Integer(required = True, description = 'Insert product id'),
  'name' : fields.String(required = True, description = 'Variant name e.g: Red Potatoes'),
  'color' : fields.String(description = 'Variant color'),
  'size' : fields.String(description = 'Specify variant size'),
  'images': fields.Integer(description = 'Images used on variant')
})

@api.route('/')
class VariantList(Resource):
  @api.doc('Get all Variants')
  def get(self):
    return variant_list_schema.dump(VariantModel.query.all()), 200
  
  @api.doc('Create a Variant')
  @api.expect(variant)
  def post(self):
    data = request.get_json()
    if not (ImageModel.find_by_id(data['images'])):
      return {'message': IMAGE_NOT_FOUND}, 404
    if not (ProductModel.query.get(data['product_id'])):
      return {'message': PRODUCT_ID_NOT_FOUND}, 404
    variant_data = variant_schema.load(data)
    variant_data.post_to_db()

    return variant_schema.dump(variant_data), 200

@api.route('/<int:id>')
@api.response(404, 'Variant not found')
@api.param('id', 'Variant identifier')
class Variant(Resource):
  @api.doc('Get Variants by id')
  def get(self, id):
    variant_data = VariantModel.find_by_id(id)
    if variant_data:
      return variant_schema.dump(variant_data)
    return {'message': VARIANT_NOT_FOUND}, 404

  @api.doc('Update variant')
  @api.expect(variant)
  def put(self, id):
    data = request.get_json()
    if not (ProductModel.query.get(data['product_id'])):
      return {'message': PRODUCT_ID_NOT_FOUND}, 404
    if not (ImageModel.find_by_id(data['images'])):
      return {'message': IMAGE_NOT_FOUND}, 404
    query = VariantModel.query.get_or_404(id)

    if (data['product_id'])  : query.product_id = data['product_id']
    if (data['name'])        : query.name = data['name']
    if (data['color'])       : query.color = data['color']
    if (data['size'])        : query.size = data['size']
    if (data['images'])      : query.images = data['images']
    query.put_to_db()

    return variant_schema.dump(query), 200

  @api.doc('Delete Variants by id')
  def delete(self, id):
    variant_data = VariantModel.find_by_id(id)
    if variant_data:
      variant_data.delete_from_db()
      return {'message': "Variant deleted successfully"}, 201
    return {'message': VARIANT_NOT_FOUND}, 404