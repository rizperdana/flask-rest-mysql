from ma import ma
from models.image import ImageModel
from schemas.product import ProductSchema
from schemas.variant import VariantSchema

class ImageSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ImageModel
    load_instance = True
    include_fk = True
  
  products = ma.Nested(ProductSchema, many=True)
  variants = ma.Nested(VariantSchema, many=True)