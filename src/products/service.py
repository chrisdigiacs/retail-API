# from db import db, Product
from flask import jsonify

class ProductService:
    def __init__(self, db, product_model):
        self.db = db
        self.Product = product_model

    def list_products(self) -> list[dict]:
        """
        Retrieve all products from the database.

        Queries the Product model to fetch all product records and returns a list of dictionaries,
        where each dictionary contains the product's 'id', 'name', and 'price'.

        Returns:
            list[dict]: A list of dictionaries representing products.
                        Example:
                        [
                            {"id": 1, "name": "Chrome Toaster", "price": 100},
                            {"id": 2, "name": "Copper Kettle", "price": 49.99},
                            {"id": 3, "name": "Mixing Bowl", "price": 20}
                        ]
        """
        try:
            product_list = self.Product.query.all()
            self.validate_product_list(product_list)
            return jsonify(self.transform_product_list(product_list)), 200
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 404

    def transform_product_list(self, products: list) -> list[dict]:
        """
        Transform the list of Product instances into a list of dictionaries.

        Args:
            products (list[Product]): The list of Product instances to be transformed.

        Returns:
            list[dict]: A list of dictionaries representing the products.
                        Example:
                        [
                            {"id": 1, "name": "Chrome Toaster", "price": 100},
                            {"id": 2, "name": "Copper Kettle", "price": 49.99},
                            {"id": 3, "name": "Mixing Bowl", "price": 20}
                        ]
        """
        return [{"id": p.id, "name": p.name, "price": p.price} for p in products]


    def validate_product_list(self, products: list) -> None:
        """
        Validate the list of products.

        Ensures that the provided list is not empty, contains only Product instances, 
        and that each Product instance has valid 'id', 'name', and 'price' fields 
        with the correct data types.

        Raises:
            ValueError: If the list is empty or if any Product instance is missing required fields.
                    - Empty list: "No products found."
                    - Missing fields: "Product must contain: id, name, and price fields."
            TypeError: If any Product instance is not of type Product or has fields with incorrect types.
                    - Non-Product instance: "One or more of the returned products are not of type <Product>."
                    - Incorrect 'id' type: "Product id must be of type int."
                    - Incorrect 'name' type: "Product name must be of type 'str'."
                    - Incorrect 'price' type: "Product price must be of type 'float'."

        Args:
            products (list[Product]): The list of Product instances to be validated.
        """
        if not products:
            raise ValueError("No products found.")
        if not all(type(p) is self.Product for p in products):
            raise TypeError("One or more of the returned products are not of type <Product>.")
        if not all(p.id and p.name and p.price for p in products):
            raise ValueError("Product must contain: id, name, and price fields.")
        if not all(type(p.id) is int for p in products):
            raise TypeError("Product id must be of type int.")
        if not all(type(p.name) is str for p in products):
            raise TypeError("Product name must be of type 'str'.")
        if not all(type(p.price) is float for p in products):
            raise TypeError("Product price must be of type 'float'.")

    def create_product(self, data: dict) -> dict:
        """
        Create a new product using the provided data.

        This function validates the input data to ensure that it contains the required 'name' and 'price' keys 
        with proper types. On successful validation, it creates a new Product instance, adds it to the database, 
        and commits the transaction. It returns a dictionary representation of the newly created product.
        
        If the input data fails validation, a ValueError is raised and caught, and the function returns a tuple 
        containing an error dictionary and a 400 status code.

        Args:
            data (dict): A dictionary containing the product details. Must include:
                        - 'name' (str): The name of the product.
                        - 'price' (float or int): The price of the product.

        Returns:
            dict: A dictionary with the new product's details on success.
                Example: {"id": 4, "name": "Microwave", "price": 200}
            tuple: In case of a validation error, returns a tuple with an error message and HTTP status code 400.
                Example: ({"error": "Request must include name and price."}, 400)
        """
        try:
            self.validate_post_request(data)
            new_product = self.Product(name = data["name"], price=data["price"])
            self.db.session.add(new_product)
            self.db.session.commit()
            return jsonify({"id": new_product.id, "name": new_product.name, "price": new_product.price}), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error":str(e)}), 422

    def validate_post_request(self, data: dict) -> None:
        """
        Validate the input data for creating a product.

        Ensures that the provided dictionary is not empty and contains both the 'name' and 'price' keys.
        Additionally, it checks that the 'name' is a string and the 'price' is either an int or a float.
        
        Raises:
            ValueError: If the data is empty, missing required keys, or invalid.
                    - Missing keys: "Request must include name and price."
                    - Invalid value: "'price' must be > 0."
            TypeError: If the data values are not of the correct data types.
                    - Incorrect type for 'name': "'name' must be of type string."
                    - Incorrect type for 'price': "'price' must be of type float or int."
        Args:
            data (dict): The input dictionary to be validated.
        """
        if not data or not ({'name', 'price'} <= data.keys()):
            raise ValueError('Request must include name and price.')
        if len(data.keys()) > 2:
            raise ValueError("Request must only include name and price.")
        if type(data['name']) is not str:
            raise TypeError("'name' must be of type string.")
        if data["name"] == "":
            raise ValueError("'name' must not be empty.")
        if type(data['price']) not in [float, int]:
            raise TypeError("'price' must be of type float or int.")
        if data["price"] <= 0:
            raise ValueError("'price' must be > 0.")
        if type(data['price']) is float and len(str(data["price"]).split(".")[1]) > 2:
            raise ValueError("'price' must have at most 2 decimal places.")