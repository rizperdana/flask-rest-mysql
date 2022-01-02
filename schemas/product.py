from ma import ma
from flask_restx import fields
from models.product import ProductModel
from schemas.variant import VariantSchema

class ProductSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ProductModel
    load_instance = True
    include_fk = True
  
  variants = fields.Nested(VariantSchema, many=True)