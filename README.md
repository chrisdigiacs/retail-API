# Retail-API
By: Christopher Di Giacomo

## Environment Setup
After cloning the repository, you should set up your development environment by following these steps. 

### 1-Setting up your Virtual Environment
Use the following command to create your virtual environment:  
`python3 -m venv venv`  

Use the following command to start up your virtual environment:  
`source venv/bin/activate`  

NOTE: If you ever wish to deactivate your virtual environment, use the following command:  
`deactivate`  

### 2-Installing dependencies
Use the following command to install the necessary dependencies for this project:  
`pip install -r requirements.txt`

## Running the application
To run the application you need to run the following command in terminal, from the root directory:
`flask run`

## Testing the application
To test the endpoints, you should run the following command in terminal, from the root directory:
`pytest`

## Project Layout
```bash
/root
    /src
        /products
            __init__.py
            routes.py
            service.py
        /sales
            __init__.py
            routes.py
            service.py
        db.py
        server.py
        test_server.py
    .env
    .gitignore
    README.md
```

### /products and /sales
These directories are packages containing all routes and service functions pertinent to the /products and /sales endpoints respectively.

## API Endpoints

### GET /products
_Returns a list of products._

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Chrome Toaster",
    "price": 100
  },
  {
    "id": 2,
    "name": "Copper Kettle",
    "price": 49.99
  },
  {
    "id": 3,
    "name": "Mixing Bowl",
    "price": 20
  }
]
```

### POST /products
_Accepts a JSON payload to create a new product, adds it to the database, and returns the created product with an assigned ID._

**Request example**
```json
{
  "name": "Microwave",
  "price": 200
}
```

**Response example**
```json
{
  "id": 4,
  "name": "Microwave",
  "price": 200
}
```

### POST /sales
_Processes a sale by calculating total prices and applying a flat discount evenly across line items. The sample response shows each line item with a calculated discount, as well as the overall total sale price._

**Request example**
```json
{
  "line_items": [
    {"id": 1, "quantity": 2},
    {"id": 2, "quantity": 1}
  ],
  "discount": 10
}
```

**Response example**
```json
{
  "line_items": [
    {"id": 1, "quantity": 2, "price": 200, "discount": 5},
    {"id": 2, "quantity": 1, "price": 49.99, "discount": 5}
  ],
  "total_sale_price": 249.99
}
```

# Contributions
_If you find bugs or have suggestions, please open an issue or submit a pull request._
