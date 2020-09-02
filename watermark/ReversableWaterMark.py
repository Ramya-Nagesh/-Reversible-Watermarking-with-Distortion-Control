import MySQLdb
import sys
import csv
import model
import gaFeatureSelection as ga
import CreateDatabase as cd

def connect():
	conn = MySQLdb.connect(host='localhost',user='root',passwd='root',db='watermark')
	return conn

def close(conn):
	conn.close()

conn=connect()
feature=['a','b']

def process(feature1,feature2,key1,key2):
	table_name="data2"
	conn=connect()
	count=0
	params=[]
	k1=int(cd.selectKeyValue(key1))
	k2=int(cd.selectKeyValue(key2))
	print("K1",k1)
	print("K2",k2)

	print ("Reverse Watermarked Tuples")
	for i in range(1,10):
		if True:
			row = model.fetch_only_from_table(conn,table_name,i,feature1,feature2)
			print(row)
			a_old,b_old=row[0],row[1]
			a_new=a_old-k1
			b_new=b_old-k2
			print (i,a_new,b_new)
			params.append((a_new,b_new,i))
			count+=1
			model.update_only_in_table(conn,table_name,i,feature1,feature2,a_new,b_new)			
	print ("Total rows Updated %d"%count)
	close(conn)
	

