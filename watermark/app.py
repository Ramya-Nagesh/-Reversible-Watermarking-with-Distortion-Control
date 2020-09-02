from flask import Flask
from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
import re
import sqlite3
import pandas as pd
import numpy as np
import requests
from flask_table import Table, Col
import model
import MySQLdb
import sys
import csv
import model
import gaFeatureSelection as ga
import CreateDatabase as cd
import WaterMark as WM
import ReversableWaterMark as RW
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

f1="f1"
f2="f2"
key1="key1"
key2="key2"
def connect():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='watermark')
	return conn


def close(conn):
	conn.close()

@app.route('/list')
def list():
	return controller.list()

@app.route('/update')
def update():
	return controller.update()

@app.route('/')
def index():
	table_name="data"
	message="Welcome"
	conn=connect()
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data=[]
	i=0
	for f in row:
		if i<50:
			data.append(f)
			i=i+1
	print(data)		
	return render_template('index.html',message=message,data=data)
	
@app.route('/createdatabase')
def createdatabase():
	table_name="data"
	message="Welcome"
	conn=connect()
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data=[]
	i=0
	for f in row:
		if i<50:
			data.append(f)
			i=i+1
	print(data)
	close(conn)
	conn=connect()
	cd.KeyProcess()
	table_name="keyvalue"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	keydata=[]
	for f in row:
		print(f)
		keydata.append(f)
	close(conn)
	conn=connect()
		
	table_name="data2"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data2=[]
	i=0
	for f in row:
		if i<50:
			data2.append(f)
			i=i+1
	print(data2)		
	close(conn)
	
	return render_template('createdatabase.html',message=message,data=data,data2=data2,keydata=keydata)

@app.route('/watermark')
def watermark():
	global f1,f2,key1,key2
	table_name="data"
	message="Welcome"
	conn=connect()
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data=[]
	i=0
	for f in row:
		if i<50:
			data.append(f)
			i=i+1
	print(data)
	
	close(conn)
	cd.KeyProcess()

	conn=connect()
	table_name="keyvalue"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	keydata=[]
	for f in row:
		print(f)
		keydata.append(f)
	close(conn)
	print("feature1",f1)
	print("feature1",f2)
	print("key1",key1)
	print("key2",key2)

	f1,f2=cd.DataProcess()
	print("feature1",f1)
	print("feature1",f2)
	key1=cd.selectKey()
	key2=cd.selectKey()
	print("key1",key1)
	print("key2",key2)
	WM.process(f1,f2,key1,key2)
	conn=connect()
		
	table_name="data2"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data2=[]
	i=0
	for f in row:
		if i<50:
			data2.append(f)
			i=i+1
	print(data2)		
	close(conn)

	return render_template('watermark.html',message=message,data=data,data2=data2,keydata=keydata,f1=f1,f2=f2,key1=key1,key2=key2)

@app.route('/reversablewatermarket')
def reversablewatermarket():
	global f1,f2,key1,key2
	table_name="data"
	message="Welcome"
	conn=connect()
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data=[]
	i=0
	for f in row:
		if i<50:
			data.append(f)
			i=i+1
	print(data)
	close(conn)
	conn=connect()
	table_name="keyvalue"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	keydata=[]
	for f in row:
		print(f)
		keydata.append(f)
	close(conn)
	print("feature1",f1)
	print("feature1",f2)
	print("key1",key1)
	print("key2",key2)
	RW.process(f1,f2,key1,key2)
	conn=connect()
		
	table_name="data2"
	row = model.fetch_from_table(conn,table_name)
	print(row)
	data2=[]
	i=0
	for f in row:
		if i<50:
			data2.append(f)
			i=i+1
	close(conn)

	return render_template('Reversablewatermark.html',message=message,data=data,data2=data2,keydata=keydata,f1=f1,f2=f2,key1=key1,key2=key2)


if __name__ == '__main__':
	app.run(debug = True)

