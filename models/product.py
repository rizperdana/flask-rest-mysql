from datetime import datetime
from db import db

class ProductModel(db.Model):
  __tablename__ = "products"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(200))
  description = db.Column(db.String(1000))
  images = db.Column(db.Integer, db.ForeignKey("images.id"))
  image = db.relationship("ImageModel", backref="image_products", foreign_keys=[images])
  logo_id = db.Column(db.Integer, db.ForeignKey("images.id"))
  logo = db.relationship("ImageModel", backref="logo_products", foreign_keys=[logo_id])
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  def __init__(self, **kwargs):
    super(ProductModel, self).__init__(**kwargs)
  
  def __repr__(self):
    return 'ProductModel data:(%s)' % self.name

  @classmethod
  def find_by_name(cls, name) -> "ProductModel":
    return cls.query.filter_by(name=name).first()
  
  @classmethod
  def find_by_id(cls, _id) -> "ProductModel":
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
