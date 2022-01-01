from ma import ma
from models.product import ProductModel

class ProductSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = ProductModel
    load_instance = True
    include_fk = True