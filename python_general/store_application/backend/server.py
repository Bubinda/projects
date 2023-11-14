from flask import Flask, request, jsonify
from sql_connection import establish_connection, close_connection
import mysql.connector
import json

import products_dao
import orders_dao
import unit_dao

app = Flask(__name__)

connection = establish_connection()


@app.route('/getUNIT', methods=['GET'])
def get_unit():
    try:
        response = unit_dao.get_unit(connection)
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except mysql.connector.Error as query_error:
        print(f"Query Error: {query_error}")

@app.route('/getProducts', methods=['GET'])
def get_products():
    try:
        response = products_dao.get_all_products(connection)
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except mysql.connector.Error as query_error:
        print(f"Query Error: {query_error}")

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    try:
        response = orders_dao.get_all_orders(connection)
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except mysql.connector.Error as query_error:
        print(f"Query Error: {query_error}")

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    try:
        request_payload = json.loads(request.form['data'])
        order_id = orders_dao.insert_order(connection, request_payload)
        response = jsonify({
            'order_id': order_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except mysql.connector.Error as query_error:
        print(f"Query Error: {query_error}")

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    try:
        return_id = products_dao.delete_product(connection, request.form['product_id'])
        response = jsonify({
            'product_id': return_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except mysql.connector.Error as query_error:
        print(f"Query Error: {query_error}")

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)

