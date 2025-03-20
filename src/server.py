from flask import Flask
from dotenv import load_dotenv
import os
from db import init_db
from products import products_bp
from sales import sales_bp


basedir = os.path.abspath(os.path.dirname(__file__)) # Store absolute path to current directory
load_dotenv() # Load variables from .env file into the environment
app = Flask(__name__) # Instantiate the Flask application

# Configure the db named 'catalog.db' to be stored in the base directory, and avoid SQLAlchemy from tracking modifications.
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'catalog.db')}" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app) # Initialize the db to be populated with default data

app.register_blueprint(products_bp) # Register the products blueprint with the application
app.register_blueprint(sales_bp) # Register the sales blueprint with the application

if __name__ == "__main__":
    app.run()