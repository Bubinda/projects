from datetime import datetime
from sql_connection import establish_connection, close_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(date, customer_id, total_cost)"
             "VALUES (%s, %s, %s)")
    order_data = (datetime.now(),order['customer_id'], order['total_cost'], )

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, quantity, product_id, total_price)"
                           "VALUES (%s, %s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['quantity']),
            float(order_detail_record['product_id']),
            float(order_detail_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from order_details where order_id = %s"

    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, "\
            "products.product_name, products.price_per_unit FROM order_details LEFT JOIN products on " \
            "order_details.product_id = products.product_id where order_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []
    for (order_id,date, customer_id, total_cost) in cursor:
        response.append({
            'order_id': order_id,
            'date': date,
            'customer_id': customer_id,
            'total_cost': total_cost,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = establish_connection()
    #print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'date': datetime.now(),
    #     'customer_id': '1',
    #     'total_cost': '6',

    #      'order_details': [
    #          {
    #              'product_id': 1,
    #              'quantity': 2,
    #              'total_price': 4
    #          },
    #          {
    #              'product_id': 3,
    #              'quantity': 1,
    #              'total_price': 2.5
    #          }
    #      ]
    #  }))

    #close_connection()