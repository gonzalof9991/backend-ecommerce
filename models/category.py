from connections.db import db

class CategoryModel(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean, unique=False, nullable=False)
    # Relationship with Product - one to many
    products = db.relationship("ProductModel", back_populates="category", lazy="dynamic")
    def __repr__(self):
        return f'<Category {self.name}>'
