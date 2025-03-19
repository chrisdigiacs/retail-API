from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Product(db.Model):
    """
    Model for Product table in db, configuring it with id, name and price columns.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

def init_db(app):
    """
    Initializes the database and populates it with initial products if empty.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # If the products table is empty, insert the initial catalog
        if Product.query.count() == 0:
            initial_products = [
                Product(id=1, name="Chrome Toaster", price=100),
                Product(id=2, name="Copper Kettle", price=49.99),
                Product(id=3, name="Mixing Bowl", price=20),
            ]
            db.session.add_all(initial_products)
            db.session.commit()