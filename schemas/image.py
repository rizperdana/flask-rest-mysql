from ma import ma
from flask_restx import fields
from models.image import ImageModel
from schemas.product import ProductSchema
from schemas.variant import VariantSchema

class ImageSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ImageModel
    load_instance = True
    include_fk = True
  
  products = fields.Nested(ProductSchema, many=True)
  variants = fields.Nested(VariantSchema, many=True)