from ma import ma
from models.variant import VariantModel

class VariantSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = VariantModel
    load_instance = True
    include_fk = True