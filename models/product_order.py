from connections.db import db


products_orders = db.Table(
    "products_orders",
    db.metadata,
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
)
