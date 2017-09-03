import enum

from . import db


class Client(enum.Enum):
    A = "client A"
    B = "client B"
    C = "client C"


class ProductArea(enum.Enum):
    POLICIES = "policies"
    BILLING = "billing"
    CLAIMS = "claims"
    REPORTS = "reports"


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    client = db.Column(db.Enum(Client))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    product_area = db.column(db.Enum(ProductArea))
