from models import ProductModel
import uuid


class OrderService:
    def __init__(self):
        pass

    @staticmethod
    def calculate_total(product_items):
        total = 0
        for product_item in product_items:
            product = ProductModel.query.filter_by(id=product_item['id']).first()
            total += product.price * product_item['quantity']
        return total

    @classmethod
    def insert_product(cls, product_items):
        products = []
        for product_item in product_items:
            product_find = ProductModel.query.filter_by(id=product_item['id']).first()
            cls.restart_stock(product_find, product_item['quantity'])
            products.append(product_find)
        return products

    @staticmethod
    def generate_code():
        return str(uuid.uuid4())

    # restart amount in wallet of user
    @staticmethod
    def restart_amount(user_id, amount):
        from models import WalletModel
        wallet = WalletModel.query.filter_by(user_id=user_id).first()
        if wallet.balance < amount:
            raise ValueError("The balance is not enough")

        wallet.balance -= amount
        wallet.save_to_db()

    # restart stock in product
    @staticmethod
    def restart_stock(product, quantity):
        if product.stock < quantity:
            raise ValueError("The stock is not enough")
        product.stock -= quantity
        product.save_to_db()
