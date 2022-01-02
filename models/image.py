from datetime import datetime
from sqlalchemy.orm import backref
from db import db

class ImageModel(db.Model):
  __tablename__ = "images"
  id = db.Column(db.Integer, primary_key = True)
  url = db.Column(db.String(1000))
  created_at = db.Column(db.DateTime)
  updated_at = db.Column(db.DateTime)

  def __init__(self, **kwargs):
    super(ImageModel, self).__init__(**kwargs)
  
  def __repr__(self):
    return 'ImageModel data:(%s)' % self.url

  @classmethod
  def find_by_url(cls, url) -> "ImageModel":
    return cls.query.filter_by(url=url).first()
  
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
