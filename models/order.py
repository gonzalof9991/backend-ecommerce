from connections.db import db
import uuid

class OrderModel(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False , default=str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="orders")
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    total = db.Column(db.Float(precision=2), unique=False, nullable=False)
    direction = db.Column(db.String(200), nullable=True)
    method_payment = db.Column(db.String(200), nullable=True)
    tracking_number = db.Column(db.String(200), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Status
    is_active = db.Column(db.Boolean, nullable=True , default=True)
    status = db.Column(db.Boolean,nullable=True, default=True)
    # Products m a m
    products = db.relationship("ProductModel", back_populates="orders", secondary="products_orders")

    def __repr__(self):
        return f'<Order {self.products}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.deleted_at = db.func.current_timestamp()
        db.session.commit()


