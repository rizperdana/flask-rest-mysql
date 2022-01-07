from flask import request
from flask_restx import Resource, fields, Namespace
from models.image import ImageModel
from schemas.image import ImageSchema

IMAGE_NOT_FOUND = "Image not found."
IMAGE_ALREADY_EXIST = "Image URL '{}' Already exits"

api = Namespace('image', description = 'Image related operations')
image_schema = ImageSchema()
image_list_schema = ImageSchema(many = True)

image = api.model('Image', {
  'url' : fields.String(required = True, description = 'Insert image url here')
})

@api.route('/')
class ImageList(Resource):
  @api.doc('Get all images')
  def get(self):
    return { 'data': image_list_schema.dump(ImageModel.query.all())}, 200
  
  @api.doc('Store image')
  @api.expect(image)
  def post(self):
    data = request.get_json()
    if ImageModel.find_by_url(data['url']):
      return {'message': IMAGE_ALREADY_EXIST.format(data['url'])}, 400
    image_data = image_schema.load(data)
    image_data.post_to_db()

    return { 'data': image_schema.dump(image_data) }, 200

@api.route('/<int:id>')
@api.response(404, 'Image not found')
@api.param('id', 'Image identifier')
class Image(Resource):
  @api.doc('Get image by id')
  def get(self, id):
    image_data = ImageModel.query.get(id)
    if image_data:
      return { 'data': image_schema.dump(image_data) }, 200
    return {'message': IMAGE_NOT_FOUND}, 404

  @api.doc('Update image url')
  @api.expect(image)
  def put(self, id):
    data = request.get_json()
    if ImageModel.find_by_url(data['url']):
      return {'message': IMAGE_ALREADY_EXIST.format(data['url'])}, 400
    query = ImageModel.query.get(id)

    query.url = data['url']
    query.put_to_db()

    return { 'data': image_schema.dump(query) }, 200

  @api.doc('Delete image')
  def delete(self, id):
    image_data = ImageModel.query.get(id)
    if image_data:
      image_data.delete_from_db()
      return {'message': "Product deleted successfully"}, 201
