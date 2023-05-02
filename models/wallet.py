from connections.db import db


class WalletModel(db.Model):
    __tablename__ = "wallet"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float(precision=2), unique=False, nullable=True)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    status = db.Column(db.Boolean, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Relationship with User - one to one
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    user = db.relationship("UserModel", back_populates="wallet")

    def __repr__(self):
        return f'<Wallet {self.id}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.deleted_at = db.func.current_timestamp()
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, _user_id):
        return cls.query.filter_by(user_id=_user_id).first()
