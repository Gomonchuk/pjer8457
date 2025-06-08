from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from config import *
from sqlalchemy.dialects.postgresql import JSONB #cтранно почему flask_sqlalchemy не умеет работать с JSONB
import json
import re

def is_valid_name(name):
	pattern = r'^[a-zA-Zа-яА-ЯёЁ\s-]+$'
	return bool(re.match(pattern, name))


app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app1)

@app1.route("/")
def show_index():
	return render_template('index.html')


@app1.route("/handler", methods=['POST'])
def handler():
	try:
		inputs = request.get_json()['inputs'] 
		temp = json.loads(inputs)
		for item in temp: 
			if not is_valid_name(item): # для серьезных проектов я бы использовал Pydantic для валидации
				raise InvalidName() 
		names = Names(array_of_names=inputs)
		db.session.add(names) 
		db.session.commit()
		return "ok"
	except Exception as e:
		abort(500)


@app1.route("/display")
def display_names():
	all_names = Names.query.all()
	temp = []
	for names in all_names:
		for name in json.loads(names.array_of_names):
			temp.append(name) 
	return render_template('display.html',all_names=temp)


@app1.errorhandler(404)
def page_not_found(error):
	return render_template('index.html')
