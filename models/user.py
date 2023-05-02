from connections.db import db

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=False)
    # Relationship with Order - one to many
    orders = db.relationship("OrderModel", back_populates="user", lazy="dynamic")
    # Relationship with Wallet - one to one
    wallet = db.relationship("WalletModel", back_populates="user", uselist=False)
    def __repr__(self):
        return f'<User {self.username}>'

