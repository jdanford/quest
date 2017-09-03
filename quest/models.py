from datetime import datetime
import enum
import json

from . import db


class Client(enum.Enum):
    A = "A"
    B = "B"
    C = "C"


class ProductArea(enum.Enum):
    POLICIES = "policies"
    BILLING = "billing"
    CLAIMS = "claims"
    REPORTS = "reports"


DATE_FORMAT = "%Y-%m-%d"


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    client = db.Column(db.Enum(Client))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    product_area = db.Column(db.Enum(ProductArea))

    @classmethod
    def from_json(cls, data):
        client = Client[data["client"].upper()]
        priority = int(data["priority"])
        target_date = datetime.strptime(data["target_date"], DATE_FORMAT)
        product_area = ProductArea[data["product_area"].upper()]
        return cls(id=data.get("id"), title=data["title"], description=data["description"], client=client,
                   priority=priority, target_date=target_date, product_area=product_area)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "client": self.client.value,
            "priority": self.priority,
            "target_date": self.target_date.strftime(DATE_FORMAT),
            "product_area": self.product_area.value
        }


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, Feature):
            return obj.to_json()

        return super().default(obj)
