from datetime import datetime
import enum
import json

from . import db


DATE_FORMAT = "%Y-%m-%d"


class Client(enum.Enum):
    A = "A"
    B = "B"
    C = "C"


class ProductArea(enum.Enum):
    POLICIES = "policies"
    BILLING = "billing"
    CLAIMS = "claims"
    REPORTS = "reports"


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.Text)
    client = db.Column(db.Enum(Client))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    product_area = db.Column(db.Enum(ProductArea))

    @classmethod
    def update_priorities(cls, client, new_feature=None):
        query = Feature.query.filter_by(client=client)
        features = query.all()

        if new_feature:
            # check if there is an existing feature request with the same priority
            if query.filter_by(priority=new_feature.priority).scalar():
                # if so, give the new one a lower priority value
                new_feature.priority -= 0.5

            features.append(new_feature)

        # renumber priorities from 1 to fix any gaps or fractional values
        sorted_features = sorted(features, key=lambda feature: feature.priority)
        for i, feature in enumerate(sorted_features, start=1):
            feature.priority = i

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
