from flask import Flask, jsonify, request , render_template
import bd
import os
from datetime import datetime

app = Flask(__name__)

list_num = []
list_log = []

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/api/n", methods=['POST'])
def api_number():
	try:
		data = request.get_json()
		number = int(data['number'])
		if number<0:
			raise Exception("Number less 0")
		return api_number_par(number)
	except:
		return jsonify({'status': "Error"})

@app.route("/api/n/<int:n>")
def api_number_par(n):
	now_time = str(datetime.now())
	try:
		# if(bd.number_in(n)):
		if(len(list(filter(lambda x: x[1]==n or x[1]==n+1, list_num)))):
			# bd.add_log(n, 'Number or next number in db')
			list_log.append([0,n,now_time,'Number or next number in db'])
			data = dict(status = "Error" , number=n, datetime=now_time, info='Number or next number in db')
			return jsonify(data)
		else:
			# bd.add_number(n)
			list_num.append([0,n,now_time])
			data = dict(status = "Ok", number = n+1, datetime = now_time)
			return jsonify(data)
	except:
		return jsonify({'status': "Error"})

@app.route("/api/log",methods=['GET'])
def api_log():
    #list_log = bd.logs()
	response = []
	try:
		for l in list_log:
			response.append(dict(id = 0, number=l[1], datetime=l[2], info=l[3]))
		return(jsonify(response))
	except:
		return jsonify({'status': "Error"})

@app.route("/api/nums",methods=['GET'])
def api_nums():
    #list_num = bd.numbers()
	response = []
	try:
		for l in list_num:
			response.append(dict(id = 0, number=l[1], datetime=l[2]))
		return(jsonify(response))
	except:
		return jsonify({'status': "Error"})

@app.route("/api/delete")
def api_delete():
	try:
		#bd.delete()
		return jsonify({'status': "OK"})
	except:
		return jsonify({'status': "Error"})

if __name__ == "__main__":
	#bd.connection = bd.create_connection("app.db")
	#bd.create_tables()
	app.run(host='0.0.0.0')