from . import db

class Pin(db.Model):
   __tablename__ = 'pins'

   id = db.Column('pin_id', db.Integer, primary_key = True)
   digit = db.Column(db.String(100))
   is_active = db.Column(db.Boolean, server_default='f', default=False)

   def __init__(self, digit):
      self.digit = digit