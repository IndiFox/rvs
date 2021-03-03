from flask import Flask, jsonify, request , render_template
from datetime import datetime
import logging
import redis
import os
from dotenv import load_dotenv


app = Flask(__name__)


#my_redis - name of docker container
try:
	r = redis.Redis(host=str(os.environ.get('REDIS_SERVICE_SERVICE_HOST')) if os.environ.get("HOST_FROM")== "env" else os.environ.get("HOST_FROM"), port=os.environ.get('REDIS_SERVICE_SERVICE_PORT'))
except redis.ConnectionError:
	logging.error("Connection with DB failed\n")
	

@app.route("/")
def index():
	logging.info("The index page is opened!")
	try:
		return render_template('/index.html')
	except:
		data = dict(status = "Error" , datetime=str(datetime.now()), info='Some trouble with main page')
		return jsonify(data)

@app.route("/api/n", methods=['POST'])
def api_number():
	try:
		data = request.get_json()
		n = int(data['number'])
		return api_number_par(n)
	except:
		data = dict(status = "Error" , number=0, datetime=str(datetime.now()), info='Some trouble with request or format')
		logging.exception(data)
		return jsonify(data)

@app.route("/api/n/<int:n>", methods=['POST'])
def api_number_par(n):
	now_time = str(datetime.now())
	try:
		if(r.sismember("nums",str(n))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Number in DB')
			logging.error("Number {} in DB.\n".format(n))
			return jsonify(data)
		elif(r.sismember("nums", str(n+1))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Next number in DB')
			logging.error("Next number {} in DB.\n".format(n))
			return jsonify(data)
		else:
			r.sadd("nums",str(n))
			logging.info("Number {} is added".format(n))
			data = dict(status = "Ok", number = n+1, datetime = now_time)
			return jsonify(data)
	except:
		data = dict(status = "Error" , number=n, datetime=now_time, info='Somethings happens with writing to BD or exceptions.')
		logging.exception(data)
		return jsonify(data)

@app.route("/api/nums",methods=['GET'])
def api_nums():
	response = []
	try:
		#Размер базы должен быть меньше 2^32-1;
		len_n = r.scard("nums")  	#CHECK
		numbers = r.smembers("nums")
		for n in numbers:
			response.append(dict(number=str(n)))
		return(jsonify(response))
	except:
		data = dict(status = "Error" , datetime=str(datetime.now()), info='Some trouble with BD or sending response.')
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

	#docker exec  -it  f40e61efd9b7 sh
