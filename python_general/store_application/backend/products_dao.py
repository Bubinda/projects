import datetime
from sql_connection import establish_connection, close_connection

def get_all_products(connection):
    cursor = connection.cursor()

    #query = ("SELECT * FROM grocery_store.products")

    query_pull_from_products_and_unit = ("SELECT products.product_id, products.product_name, products.unit_id, products.price_per_unit, unit.unit_name "
                                        "FROM products inner join unit "
                                        "on products.unit_id= unit.unit_id;")

    #cursor.execute(query)

    cursor.execute(query_pull_from_products_and_unit)

    response = []

    for (product_id, product_name, unit_id, price_per_unit, unit_name) in cursor:
        response.append(
            {
                'product_id': product_id,
                'name': product_name,
                'uom_id': unit_id,
                'price_per_unit': price_per_unit,
                'uom_name': unit_name
            }
        )
        #print(product_id, product_name, unit_id, price_per_unit, unit_name)


    connection.close()

    return response



def insert_new_product(connection, product):
    try:
        cursor = connection.cursor()

        query = ("insert into products "
                "(product_name, unit_id, price_per_unit) "
                "values (%s, %s, %s);")

        data = (product['product_name'], product['unit_id'], product['price_per_unit'])
        cursor.execute(query,data)
        connection.commit()

        return cursor.lastrowid
    except:
        return f"failed to insert the requested product with name: {product['product_name']}"




def delete_product(connection, product_id):
    try:
        cursor = connection.cursor()
        query = (f"DELETE FROM products where product_id={str(product_id)}")
        cursor.execute(query)
        connection.commit()
        return f"deleted product with id: {product_id}"
    except:
        return f"failed to delete the requested product with id: {product_id}"




if __name__ == "__main__":
    connection = establish_connection()
    #print(get_all_products(connection=connection))

    product = {
        'product_name': 'cabbage',
        'unit_id': '1',
        'price_per_unit': '3'
    }

    #print(insert_new_product(connection=connection, product=product))

    print(delete_product(connection, 4))

    close_connection()