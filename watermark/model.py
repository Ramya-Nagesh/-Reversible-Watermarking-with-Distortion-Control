import MySQLdb
conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='watermark')

def delete_everything_table(conn,table_name):
	curr=conn.cursor()
	sql="TRUNCATE %s"%(table_name)
	try:
		curr.execute(sql)
		conn.commit()
		print ("data deleted sucessfully")
	except:
		conn.rollback()
		print ('data not deleted')



		
def insert_param_into_table(conn,table_name,rows):
	table_name=str(table_name)
	t_sql="INSERT INTO %s (ID,a, b, c,d) "%(table_name)
	sql=t_sql+"VALUES (%s,%s, %s, %s,%s)"
	curr=conn.cursor()
	try:
		curr.executemany(sql,rows)
		conn.commit()
		print ("inserted_sucessfully")
	except:
		conn.rollback()
		print ("data not inserted")


def insert_param_into_table1(conn,table_name,rows):
	table_name=str(table_name)
	t_sql="INSERT INTO %s (ID,a, b, c,d) "%(table_name)
	sql=t_sql+"VALUES (%s,%s, %s, %s,%s)"
	curr=conn.cursor()
	try:
		curr.executemany(sql,rows)
		conn.commit()
		print ("inserted_sucessfully")
	except:
		conn.rollback()
		print ("data not inserted")



def fetch_everything_from_table(conn,table_name):
	curr=conn.cursor()
	curr.execute("SELECT * FROM %s"%(table_name))
	rows=curr.fetchall()
	return rows

def fetch_from_table(conn,table_name):
	curr=conn.cursor()
	curr.execute("SELECT * FROM %s"%(table_name))
	rows=curr.fetchall()
	return rows


def fetch_only_from_table(conn,table_name,id,a,b):
	curr=conn.cursor()
	try:
		print("table_name",table_name)
		curr.execute("SELECT %s,%s FROM %s WHERE ID = %d"%(a,b,table_name,id))
		row=curr.fetchone()
	except:
		print ("Search not sucessfull"	)
	return row

def update_only_in_table(conn,table_name,id,a,b,aval,bval):
	curr=conn.cursor()
	table_name=str(table_name)
	print(table_name)
	id=int(id)
	aval=int(aval)
	bval=int(bval)
	try:
		curr.execute("UPDATE %s SET %s = %d,%s = %d WHERE ID = %d"%(table_name,a,aval,b,bval,id))
		conn.commit()
	except:
		print("not update")
		conn.rollback()	




	