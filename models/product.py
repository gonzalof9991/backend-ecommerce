from connections.db import db


class ProductModel(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    stock = db.Column(db.Integer, unique=False, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=False)
    new_price = db.Column(db.Float(precision=2), unique=False, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Relationship with Category - one to one
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), unique=False, nullable=False)
    category = db.relationship("CategoryModel", back_populates="products")
    # Order m a m
    orders = db.relationship("OrderModel", back_populates="products", secondary="products_orders")

    def __repr__(self):
        return f'<Product {self.name}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.deleted_at = db.func.current_timestamp()
        db.session.commit()

