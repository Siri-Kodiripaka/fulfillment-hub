from database import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(30), unique=True)
    customer = db.Column(db.String(100))
    product = db.Column(db.String(100))
    variant = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    priority = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(30))
    deadline = db.Column(db.String(50))
    courier = db.Column(db.String(50))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100))
    variant = db.Column(db.String(100))
    warehouse = db.Column(db.String(30))
    available = db.Column(db.Integer)
    required = db.Column(db.Integer)
    location = db.Column(db.String(30))

    def to_dict(self):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        d["shortage"] = max(0, self.required - self.available)
        return d

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_type = db.Column(db.String(100))
    order_no = db.Column(db.String(30))
    priority = db.Column(db.String(20))
    status = db.Column(db.String(30))
    notes = db.Column(db.Text)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
