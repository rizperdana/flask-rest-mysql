from ma import ma
from models.product import ProductModel
from schemas.variant import VariantSchema

class ProductSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = ProductModel
    load_instance = True
    include_fk = True
  
  variants = ma.Nested(VariantSchema, many=True)