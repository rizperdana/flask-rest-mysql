from datetime import datetime
from sqlalchemy.orm import backref
from db import db

class VariantModel(db.Model):
  __tablename__ = "variants"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(200))
  size = db.Column(db.String(200))
  color = db.Column(db.String(200))
  images = db.Column(db.Integer)
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)
  product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
  product = db.relationship("ProductModel", backref="variants")

  def __init__(self, **kwargs):
    super(VariantModel, self).__init__(**kwargs)
  
  def __repr__(self):
    return 'VariantModel data:(%s)' % self.name

  @classmethod
  def find_by_name(cls, name) -> "VariantModel":
    return cls.query.filter_by(name=name).first()
  
  @classmethod
  def find_by_id(cls, _id) -> "VariantModel":
    return cls.query.filter_by(id=_id).first()
  
  def post_to_db(self) -> None:
    self.updated_at = datetime.now()
    self.created_at = datetime.now()
    db.session.add(self)
    db.session.commit()
  
  def put_to_db(self) -> None:
    self.updated_at = datetime.now()
    db.session.add(self)
    db.session.commit()
  
  def delete_from_db(self) -> None:
    db.session.delete(self)
    db.session.commit()
