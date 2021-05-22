import json
import mysql.connector
import logging
import os
import time
from influxdb import InfluxDBClient
from get_docker_secret import get_docker_secret


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

USER = None
PASSWORD = None

USER = get_docker_secret(os.getenv('MSUSER_FILE'), default='very_secret')
PASSWORD = get_docker_secret(os.getenv('MSPASSWORD_FILE'), default='very_secret')

logger.info(USER)
logger.info(PASSWORD)

mysql_config = {
        'user': USER,
        'password': PASSWORD,
        'host': os.getenv('MSHOST'),
        'port': os.getenv('MSPORT'),
        'database': os.getenv('MSDATABASE')
    }

db_client = None

def select_orders(id):
	connection = mysql.connector.connect(**mysql_config)
	cursor = connection.cursor()
	querry = 'SELECT * FROM ORDERS WHERE ID_ORDER > %s'
	cursor.execute(querry, (id,))
	result = cursor.fetchall()
	orders = []
	response = {}
	for _, order_date, _, user, quantity in result:
		order = {}
		order['ORDER_DATE'] = order_date.strftime("%Y-%m-%dT%H:%M:%SZ")

		cursor.callproc('select_user', [int(user)])
		result_1 = []
		for row in cursor.stored_results():
			result_1 = row.fetchall()
		for _, surname, forename, _, _, _, _, _ in result_1:
			order['USER'] = surname + "_" + forename

		order['QUANTITY'] = int(quantity)
		orders.append(order)
	response["data"] = orders
	cursor.close()
	connection.close()
	return json.dumps(response)

def select_last_order():
	connection = mysql.connector.connect(**mysql_config)
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM MESSAGES')
	result = cursor.fetchall()
	id_cmd = 0
	for message in result:
		mess = str(message)
		mess = mess[:-3]
		mess = mess[2:]
		mess = mess.split(":")
		if '-' not in mess[1].strip():
			id_cmd = int(mess[1].strip())
	return id_cmd

def influxDB_connection():
	time.sleep(10)
	db_client = InfluxDBClient(host=os.getenv('IDBHOST'), port=int(os.getenv('IDBPORT')))
	db_client.create_database(os.getenv('IDBDATABASE'))
	db_client.switch_database(os.getenv('IDBDATABASE'))
	return db_client


if __name__ == '__main__':
	time.sleep(10)
	db_client = influxDB_connection()
	prev_order = 0
	while True:
		current_order = select_last_order()
		if current_order != 0 and current_order != prev_order:
			js_orders = select_orders(prev_order)
			prev_order = current_order
			orders = json.loads(js_orders)
			logger.info("Show orders")
			for order in orders["data"]:
				logger.info(order)
			for i in range(0, len(orders["data"])):
				point = {}
				point["measurement"] = "orders"
				tags = {}
				order = orders["data"][i]
				tags["user"] = order["USER"]
				point["tags"] = tags
				point["time"] = order["ORDER_DATE"]
				fields = {}
				fields["quantity"] = int(order["QUANTITY"])
				point["fields"] = fields
				db_client.write_points([point])
				logger.info(point)
