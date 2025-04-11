from flask import Flask
from dotenv import load_dotenv
import os
from db import init_db, db, Product
from products import products_bp, ProductService
from sales import sales_bp, SalesService

class AppFactory:
    # Constructor that initializes the Flask application, connects to the db, initializes services, and registers blueprints
    def __init__(self, basedir: str = None):
        # Sets basedir to be the absolute path of the directory containing this file, IF not provided
        basedir = basedir if basedir else os.path.abspath(os.path.dirname(__file__))
        self.app = Flask(__name__)# Instantiate the Flask application
        self.__connect_db(basedir)# Calls the class function to connect to the db, with the basedir
        self.__init_services()# Calls the class function to initialize the services
        self.__register_blueprints()# Calls the class function to register the blueprints

    # Function to connect to the db
    def __connect_db(self, basedir):
        # Configure the db named 'catalog.db' to be stored in the base directory, and avoid SQLAlchemy from tracking modifications.
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'catalog.db')}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        init_db(self.app)# Initialize the db to be populated with default data
        self.db = db # Store the db instance in the app

    # Function to initialize the services
    def __init_services(self):
        self.app.products_service = ProductService(db, Product)# Initialize the products service
        self.app.sales_service = SalesService(db, Product)# Initialize the sales service
    
    # Function to register the blueprints
    def __register_blueprints(self):
        self.app.register_blueprint(products_bp)# Register the products blueprint with the application
        self.app.register_blueprint(sales_bp)# Register the sales blueprint with the application

# Function to create the app using the AppFactory, and return it
def create_app():
    return AppFactory().app

if __name__ == "__main__":
    load_dotenv() # Load variables from .env file into the environment
    app = create_app()# Create the app
    app.run()# Run the app