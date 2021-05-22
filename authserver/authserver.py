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
CLIENT_ERROR = 404

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/login', methods=['POST'])
def login():
	connection = mysql.connector.connect(**config)
	response = {}
	credentials = {}
	try:
		cursor = connection.cursor()
		data = request.json
		email = data['EMAIL']
		password = data['PASSWORD']

		print(email, password)
		func = "SELECT ID_USER FROM USERS WHERE EMAIL=%s AND PASSWORD=%s"
		cursor.execute(func, (email, password))
		id_user = cursor.fetchone()
		id_user = id_user[0]
		print(id_user)

		if id_user == 0:
			response['data'] = "User undefined"
			response['status'] = CLIENT_ERROR
			return json.dumps(response)

		cursor.callproc('select_user', [id_user])
		result = []
		for row in cursor.stored_results():
			result = row.fetchall()

		for _, _, _, _, _, _, _, is_adm in result:
			credentials["IS_ADMIN"] = int(is_adm)

		func = 'SELECT test_session(%s)'
		cursor.execute(func, (id_user,))
		ok = cursor.fetchone()
		ok = ok[0]
		print(ok)
		if ok == 0:
			token = randomString(10)
			print(token)
			cursor.callproc('add_session', [token, id_user])
			credentials['TOKEN'] = token
		else:
			cursor.callproc('select_session', [id_user])
			result = []
			for row in cursor.stored_results():
				result = row.fetchall()
			for _, token, _ in result:
				credentials['TOKEN'] = token
		credentials['status'] = SUCCESS
		cursor.close()
		connection.close()
	except:
		credentials["status"] = SERVER_ERROR
	return json.dumps(credentials)


@app.route('/logout/<token>', methods=['POST'])
def logout(token):
	connection = mysql.connector.connect(**config)
	response = {}
	try:
		cursor = connection.cursor()
		print("logout " + token)
		cursor.callproc('delete_session_token', [token])
		cursor.close()
		connection.close()
		response['status'] = SUCCESS
	except:
		response["status"] = SERVER_ERROR
	return json.dumps(response)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5555, debug=True)
