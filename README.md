# product-aggregator-microservice

## Description
This is the source-code of a REST API JSON Python microservice which allows users to browse a product catalog and which automatically updates prices from the provided offer service.

**Microservice provides:**
  - API with CRUD operations for products
  - read-only API to get product offers (product offers are periodically updated from the provided microservice for offers with products)

The application is implemented in Python 3 and uses several Python libraries (e.g. Flask, Flask-RESTful, Flask-SQLAlchemy and pytest). All dependencies of this application are named in the requirements.txt file.

It was developed as an introductory assignment for Applifting company.

## How to run
### environment setup
Firstly, to use this application, you need a python environment with all dependencies from requirements.txt file. For example, you can use conda and easily create conda environment with the following conda command
```
conda create --name <env-name> --file requirements.txt
```
and then activate this environment with command
```
conda activate <env-name>
```
where \<env-name\> is the name of created virtual environment. 
  
### run application
In this environment you can run this microservice from the root directory with command
```
python product_aggregator/main.py
```
### run tests
You can also run tests in this environment. To run tests, use command
```
pytest -v --disable-pytest-warnings
```
in the root directory.

## JSON REST API documentation
- ### create product -> POST /products
  - Request: 

    ```
    {
      "name": "<name-of-product>", 
      "description": "<description-of-product>"
    }
    ```
  - Response:
    - `201 CREATED`

      ```
      {
        "id": <product-id>, 
        "name": "<name-of-product>", 
        "description": "<description-of-product>"
      }
      ```
    - `400 BAD REQUEST`

      ```
      {
        "code": "BAD REQUEST",
        "message": <msg>
      }
      ```
- ### read all products -> GET /products
  - Request: None
  - Response:
    - `200 OK`

      ```
      [
        {
          "id": <product-id>, 
          "name": "<name-of-product>", 
          "description": "<description-of-product>"
        }
      ]
      ```

- ### read product -> GET /products/\<id\>
  - Request: id in path
  - Response:
    - `200 OK`

      ```
      {
        "id": <product-id>, 
        "name": "<name-of-product>", 
        "description": "<description-of-product>"
      }
      ```
    - `404 NOT FOUND`

      ```
      {
        "code": "NOT FOUND",
        "message": "Product does not exist"
      }
      ```

- ### delete product -> DELETE /products/\<id\>
  - Request: id in path
  - Response:
    - `204 NO CONTENT`

      ```
      {}
      ```
    - `404 NOT FOUND`

      ```
      {
        "code": "NOT FOUND",
        "message": "Product does not exist"
      }
      ```

- ### update product -> PUT /products/\<id\>
  - Request: 
      - id in path
        
        ```
        {
          "name": "<name-of-product>", 
          "description": "<description-of-product>"
        }
        ```
  - Response:
    - `20O OK`

      ```
      {
        "id": <product-id>, 
        "name": "<name-of-product>", 
        "description": "<description-of-product>"
      }
      ```
    - `400 BAD REQUEST`

      ```
      {
        "code": "BAD REQUEST",
        "message": <msg>
      }
      ```
    - `404 NOT FOUND`

      ```
      {
        "code": "NOT FOUND",
        "message": "Product does not exist"
      }
      ```

- ### get offers of product -> GET /products/\<product_id\>/offers
  - Request: product_id in path
  - Response:
    - `200 OK`

      ```
      [
        {
          "id": <offer-id>, 
          "product_id": <product-id>,
          "price": <price>, 
          "items_in_stock": <items-in-stock>
        }
      ]
      ```
    - `404 NOT FOUND`

      ```
      {
        "code": "NOT FOUND",
        "message": "Product with id <product-id> does not exist"
      }
      ```
