import os
import json
import datetime
import random
import string
import logging
import mysql.connector
from flask import Flask, request
from get_docker_secret import get_docker_secret

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

USER = None
PASSWORD = None

USER = get_docker_secret(os.getenv('MSUSER_FILE'), default='very_secret')
PASSWORD = get_docker_secret(os.getenv('MSPASSWORD_FILE'), default='very_secret')

logger.info(USER)
logger.info(PASSWORD)

config = {
        'user': USER,
        'password': PASSWORD,
        'host': os.getenv('MSHOST'),
        'port': os.getenv('MSPORT'),
        'database': os.getenv('MSDATABASE')
    }

SUCCESS = 200
SERVER_ERROR = 500

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		cursor.callproc('select_all_ingredients')
		ingredients = []
		result = []
		for row in cursor.stored_results():
			result = row.fetchall()
		for id, name in result:
			ingredient = {}
			ingredient['ID_INGREDIENT'] = int(id)
			ingredient['NAME'] = name
			ingredients.append(ingredient)

		response["data"] = ingredients
		cursor.close()
		connection.close()
		response["status"] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/ingredients', methods=['POST'])
def add_ingredient():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		name = data['NAME']
		cursor.callproc('add_ingredient', [name])
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response['status'] = SERVER_ERROR
	return json.dumps(response)

@app.route('/ingredients/<id>', methods=['DELETE'])
def delete_ingredient(id):
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		id_ingr = int(id)
		cursor.callproc('delete_ingredient', [id_ingr])
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response['status'] = SERVER_ERROR
	return json.dumps(response)

@app.route('/products', methods=['GET'])
def get_products():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		cursor.callproc('select_all_products')
		result = []
		products = []
		for row in cursor.stored_results():
			result = row.fetchall()
		for id, name, desc, price, unit, ingr, categ in result:
			product = {}
			product['ID_PRODUCT'] = int(id)
			product['NAME'] = name
			product['DESCRIPTION'] = desc
			product['PRICE'] = int(price)
			product['MEASURE_UNIT'] = unit
			product['CATEGORY'] = categ

			cursor.callproc('select_ingredient', [int(ingr)])
			result_1 = []
			for row in cursor.stored_results():
				result_1 = row.fetchall()
			for _, name in result_1:
				product['MAIN_INGREDIENT'] = name
			products.append(product)
		response["data"] = products
		cursor.close()
		connection.close()
		response["status"] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/products', methods=['POST'])
def add_product():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		name = data['NAME']
		desc = data['DESCRIPTION']
		price = int(data['PRICE'])
		unit = data['MEASURE_UNIT']
		id_ingr = int(data['MAIN_INGREDIENT'])
		categ = data['CATEGORY']
		cursor.callproc('add_product', [name, desc, price, unit, id_ingr, categ])
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		id_prod = int(id)
		cursor.callproc('delete_product', [id_prod])
		cursor.close()
		connection.close()
		response["status"] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/users', methods=['POST'])
def add_user():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		surname = data['SURNAME']
		forename = data['FORENAME']
		phone = data['PHONE']
		email = data['EMAIL']
		address = data['ADDRESS']
		password = data['PASSWORD']
		admin = int(data['IS_ADMIN'])
		cursor.callproc('add_user', [surname, forename, phone, email, address, password, admin])

		func = "SELECT ID_USER FROM USERS WHERE EMAIL=%s AND PASSWORD=%s"
		cursor.execute(func, (email, password))
		id_user = cursor.fetchone()
		id_user = id_user[0]
		print(id_user)
		#id_user = cursor.callproc('get_user', [email, parola])
		token = randomString(10)
		print(token)
		cursor.callproc('add_session', [token, id_user])
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
		response['TOKEN'] = token
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		id_user = int(id)
		cursor.callproc('delete_session', [id_user])
		cursor.callproc('delete_user', [id_user])
		cursor.close()
		connection.close()
		response["status"] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/orders/<token>', methods=['GET'])
def get_orders(token):
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		cursor.callproc('select_all_orders', [token])
		result = []
		for row in cursor.stored_results():
			result = row.fetchall()
		orders = []
		for id_cmd, date_cmd, price, user, quantity in result:
			total_price = 0
			order = {}
			order['ID_ORDER'] = int(id_cmd)
			order['ORDER_DATE'] = date_cmd.strftime("%Y-%m-%d %H:%M:%S")

			products = []
			cursor.callproc('select_user', [int(user)])
			result_1 = []
			for row in cursor.stored_results():
				result_1 = row.fetchall()
			for _, surname, forename, _, _, _, _, _ in result_1:
				order['USER_NAME'] = surname + " " + forename

			cursor.callproc('select_order_id_ord', [int(id_cmd)])
			result_1 = []
			for row in cursor.stored_results():
				result_1 = row.fetchall()
			for _, product, _, quantity in result_1:
				cursor.callproc('select_product_id', [int(product)])
				result_2 = []
				for row in cursor.stored_results():
					result_2 = row.fetchall()
				for _, name, _, price, _, _, categ in result_2:
					order['PRODUCT_NAME'] = name
					order['PRODUCT_CATEGORY'] = categ
					total_price = int(quantity) * int(price)
			order['PRICE'] = total_price
			orders.append(order)
		response["data"] = orders
		response["status"] = SUCCESS
		cursor.close()
		connection.close()
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/orders', methods=['POST'])
def add_order():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		now = datetime.datetime.now()
		date_cmd = now.strftime('%Y-%m-%d %H:%M:%S')
		date_cmd = datetime.datetime.strptime(date_cmd, '%Y-%m-%d %H:%M:%S')
		token = data['TOKEN']
		quantity = int(data['QUANTITY'])
		func = 'SELECT ID_USER FROM SESSIONS WHERE TOKEN=%s'
		cursor.execute(func, (token,))
		id_user = cursor.fetchone()
		id_user = id_user[0]
		cursor.callproc('add_order', [date_cmd, 0, id_user, quantity])

		id_prod = int(data['ID_PRODUCT'])
		print(id_prod)
		cursor.execute('SELECT MAX(ID) FROM ORDER_LIST')
		id_record = cursor.fetchone()
		id_record = id_record[0]
		print(id_record)
		if id_record == None:
			id_record = 1
		else:
			id_record += 1

		cursor.execute('SELECT get_current_id_cmd()')
		id_cmd = cursor.fetchone()
		id_cmd = id_cmd[0]
		print(id_cmd)
		cursor.callproc('add_order_list', [id_record, id_prod, quantity, id_cmd])

		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/orders', methods=['DELETE'])
def delete_order():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		id_cmd = int(data['ID_ORDER'])
		id_prod = int(data['ID_PRODUCT'])
		cursor.callproc('delete_order_list', [id_cmd, id_prod])
		cursor.callproc('delete_order', [id_cmd])
		cursor.close()
		connection.close()
		response["status"] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/filter_orders', methods=['POST'])
def filter_order_dp():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		dd = data['ORDER_DATE']
		pp = data['PRICE']
		result = []
		if dd != "" and pp != -1:
			date_cmd = datetime.datetime.strptime(dd, '%Y-%m-%d')
			cursor.callproc('select_order_date_price', [date_cmd, int(pp)])
		elif dd != "":
			date_cmd = datetime.datetime.strptime(dd, '%Y-%m-%d')
			cursor.callproc('select_order_date', [date_cmd])
		elif pp != -1:
			cursor.callproc('select_order_price', [int(pp)])


		if pp != -1 or dd != "":
			orders = []
			for row in cursor.stored_results():
				result = row.fetchall()
			for id_cmd, date_cmd, price, user, quantity in result:
				order = {}
				order['ID_ORDER'] = int(id_cmd)
				order['ORDER_DATE'] = date_cmd.strftime("%Y-%m-%d")
				products = []

				cursor.callproc('select_user', [int(user)])
				result_1 = []
				for row in cursor.stored_results():
					result_1 = row.fetchall()
				for _, surname, forename, _, _, _, _, _ in result_1:
					order['USER_NAME'] = surname + " " + forename

				cursor.callproc('select_order_id_ord', [int(id_cmd)])
				for row in cursor.stored_results():
					result_1 = row.fetchall()

				for _, prod, _, cant in result_1:
					result_2 = []
					cursor.callproc('select_product_id', [int(prod)])
					for row in cursor.stored_results():
						result_2 = row.fetchall()
					for _, name, _, price, _, _, _ in result_2:
						order['PRODUCT_NAME'] = name
						price = int(price)
						total_price = int(cant) * price
				order['PRICE'] = total_price
				orders.append(order)
				print(order)

			print(orders)
			response['data'] = orders
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)


@app.route('/filter_products', methods=['POST'])
def filter_products_ic():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		data = request.json
		categ = data['CATEGORY']
		ingr = int(data['INGREDIENT'])
		result = []
		if ingr != 0 and categ != "":
			cursor.callproc('select_product_ingr_categ', [ingr, categ])
		elif categ != "":
			cursor.callproc('select_product_categ', [categ])
		elif ingr != 0:
			cursor.callproc('select_product_ingr', [ingr])

		if ingr != 0 or categ != "":
			products = []
			for row in cursor.stored_results():
				result = row.fetchall()
			for id_prod, name, desc, price, unit, main_ingr, categ_prod in result:
				product = {}
				product['ID_PRODUCT'] = int(id_prod)
				product['NAME'] = name
				product['DESCRIPTION'] = desc
				product['PRICE'] = int(price)
				product['MEASURE_UNIT'] = unit
				product['CATEGORY'] = categ_prod

				cursor.callproc('select_ingredient', [int(main_ingr)])
				result_1 = []
				for row in cursor.stored_results():
					result_1 = row.fetchall()

				for _, name_ingr in result_1:
					product['MAIN_INGREDIENT'] = name_ingr
				products.append(product)
			response["data"] = products
		response['status'] = SUCCESS
		cursor.close()
		connection.close()
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/group_products_ingr', methods=['GET'])
def group_products_ingr():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		cursor.callproc('group_products_ingr')
		res = []
		results = []
		for row in cursor.stored_results():
			res = row.fetchall()
		for name, nr_prod in res:
			result = {}
			result['NAME'] = name
			result['NR_PROD'] = int(nr_prod)
			results.append(result)
		cursor.close()
		connection.close()
		response["data"] = results
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

@app.route('/group_products_categ', methods=['GET'])
def group_products_categ():
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		cursor.callproc('group_products_categ')
		res = []
		results = []
		for row in cursor.stored_results():
			res = row.fetchall()
		for categ, nr_prod in res:
			result = {}
			result['CATEGORY'] = categ
			result['NR_PROD'] = int(nr_prod)
			results.append(result)
		cursor.close()
		connection.close()
		response["data"] = results
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
