from flask import Flask, jsonify, request , render_template
from datetime import datetime
import logging
import redis

app = Flask(__name__)
#my_redis - name of docker container
r = redis.Redis(host='my_redis', port=6379)

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
		data = dict(status = "Error" , number=n, datetime=str(datetime.now()), info='Some trouble with request or format')
		return jsonify(data)

@app.route("/api/n/<int:n>")
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
		return jsonify(data)


if __name__ == "__main__":
	logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	logging.basicConfig(level=logging.DEBUG) #https://webdevblog.ru/logging-v-python/
	app.run(host='0.0.0.0') 