from flask import Flask, jsonify, request , render_template
from datetime import datetime
import logging
import redis
import os
from dotenv import load_dotenv


app = Flask(__name__)

def get_connection():
	try:
		REDIS_SERVICE_SERVICE_HOST = str(os.environ.get('REDIS_SERVICE_SERVICE_HOST')) if os.environ.get("HOST_FROM")== "env" else os.environ.get("HOST_FROM")
		REDIS_SERVICE_SERVICE_PORT = int(os.environ.get('REDIS_SERVICE_SERVICE_PORT'))
		r = redis.Redis(host=REDIS_SERVICE_SERVICE_HOST, port=REDIS_SERVICE_SERVICE_PORT)
		if(r.ping()):
			return True, r
	except redis.ConnectionError:
		logging.error("Connection with DB failed\n")
		return False, None
	except:
		logging.error("Some trubles with DB\n")
		return False, None

#Установка соединения:
flag_db, r = get_connection()

@app.route("/")
def index():
	logging.info("The index page is opened!")
	try:
		return render_template('/index.html')
	except:
		data = dict(status = "Error" , datetime=str(datetime.now()), info='Some trouble with main page')
		logging.exception(data)
		return jsonify(data)

@app.route("/api/n", methods=['POST'])
def api_number():
	try:
		data = request.get_json()
		n = int(data['number'])
		return api_number_par(n)
	except:
		data = dict(status = "Error" , number=n, datetime=str(datetime.now()), info='Some trouble with request or format number')
		logging.exception(data)
		return jsonify(data)

def api_number_par(n):
	now_time = str(datetime.now())
	global flag_db,r
	#Переподключение в случае отсутсвия соединения
	if(flag_db is not None and not flag_db):
		flag_db,r = get_connection()
	if(flag_db):
		if(r.sismember("nums",str(n))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Number in DB!')
			logging.error("Number {} in DB.\n".format(n))
			return jsonify(data)
		elif(r.sismember("nums", str(n+1))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Next number in DB!')
			logging.error("Next number {} in DB.\n".format(n))
			return jsonify(data)
		else:
			#Размер БД Редис должен быть меньше 2^32-1;
			if(r.scard("nums")<2**32-1):
				#Запись числа;
				r.sadd("nums",str(n))
				logging.info("Number {} is added".format(n))
				data = dict(status = "Ok", number = n+1, datetime = now_time)
				return jsonify(data)
			else:
				data = dict(status = "Error" , number=n, datetime=now_time, info='DB is full')
				logging.warning(data)
				return jsonify(data)
	else:
		data = dict(status = "Error" , number=n, datetime=now_time, info='Could not connect to DB')
		logging.exception(data)
		return jsonify(data)

@app.route("/api/nums",methods=['GET'])
def api_nums():
	response = []
	global flag_db,r
	#Переподключение в случае отсутсвия соединения
	if(flag_db is not None and not flag_db):
		flag_db,r = get_connection()
	if(flag_db):
		try:
			#Получение всех чисел из БД и генерация list словарей
			numbers = r.smembers("nums")
			for n in numbers:
				response.append(dict(number=str(n)))
			return(jsonify(response))
		except:
			data = dict(status = "Error" , datetime=str(datetime.now()), info='Could not get data')
			logging.exception(data)
			return jsonify(data)
	else:
		data = dict(status = "Error" , datetime=str(datetime.now()), info='Could not connect to DB')
		logging.exception(data)
		return jsonify(data)



if __name__ == "__main__":
	#Определение пути к файлу с переменными среды
	dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
	#Загрузка переменных среды из файла, переменные не перезаписываются.
	if os.path.exists(dotenv_path):
		load_dotenv(dotenv_path)
	#Определение имени файла лога, формата записи, режима доступа к файлу и урованя логирования.
	logging.basicConfig(filename='rvs_app.log', filemode='w',level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S') #https://webdevblog.ru/logging-v-python/
	#logging.basicConfig(filename=os.environ.get('APP_LOG'), filemode='w', format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	#По умолчанию функция запуска берет данные хоста и порта из перменных среды.
	app.run(host= os.environ.get("FLASK_RUN_HOST"), port = os.environ.get("FLASK_RUN_PORT"))