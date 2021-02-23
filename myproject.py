from flask import Flask, jsonify, request , render_template
from datetime import datetime
import logging
import redis
import time 

app = Flask(__name__)
r = redis.Redis(host='172.17.0.2', port=6379)

@app.route("/")
def index():
	"""logging.debug('This is a debug message')
	logging.info('This is an info message')
	logging.warning('This is a warning message')
	logging.error('This is an error message')
	logging.critical('This is a critical message')

	return render_template("/index.html")"""
	#Размер базы должен быть меньше 2^32-1;
	print(r.sadd("nums", "1","2"))
	#print(r.sismember("nums", "1"))
	#print(r.scard("nums"))
	#print(r.sadd("nums", "4"))
	#print(r.smembers("nums"))
	return 'Hello World! I have been seen {} times.\n'.format(r.smembers("nums"))

@app.route("/api/n", methods=['POST'])
def api_number():
	try:
		data = request.get_json()
		n = int(data['number'])
		return api_number_par(n)
	except:
		data = dict(status = "Error" , number=n, datetime=str(datetime.now()), info='Some trouble with request')
		return jsonify(data)

@app.route("/api/n/<int:n>")
def api_number_par(n):
	now_time = str(datetime.now())
	print("HIIII")
	try:
		if n<0:
			raise ValueError()
		if(r.sismember("nums",str(n))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Number in DB')
			#logging.error("Number {} in DB.\n".format(n))
			return jsonify(data)
		elif(r.sismember("nums", str(n+1))):
			data = dict(status = "Error" , number=n, datetime=now_time, info='Next number in DB')
			#logging.error("Next number {} in DB.\n".format(n))
			return jsonify(data)
		else:
			r.sadd("nums",str(n))
			#logging.info("Number {} is added".format(n))
			data = dict(status = "Ok", number = n+1, datetime = now_time)
			return jsonify(data)
	except ValueError:
		data = dict(status = "Error" , number=n, datetime=str(datetime.now()), info='The input number less then 0')
		return jsonify(data)
	except:
		return jsonify({'status': "Error"})

@app.route("/api/log",methods=['GET'])
def api_log():
	"""
	response = []
	try:
		for l in list_log:
			response.append(dict(id = 0, number=l[1], datetime=l[2], info=l[3]))
		return(jsonify(response))
	except:
		return jsonify({'status': "Error"})"""
	return "Logs"

@app.route("/api/nums",methods=['GET'])
def api_nums():
	"""#list_num = bd.numbers()
	response = []
	try:
		for l in list_num:
			response.append(dict(id = 0, number=l[1], datetime=l[2]))
		return(jsonify(response))
	except:
		return jsonify({'status': "Error"})"""
	return "Nums"

@app.route("/api/delete")
def api_delete():
	try:
		#bd.delete()
		return jsonify({'status': "OK"})
	except:
		return jsonify({'status': "Error"})

if __name__ == "__main__":
	"""logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	logging.basicConfig(level=logging.DEBUG)
	#https://webdevblog.ru/logging-v-python/"""
	app.run(host='0.0.0.0') 