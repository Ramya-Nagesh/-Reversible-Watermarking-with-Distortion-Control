import MySQLdb
import sys
import csv
import model
import gaFeatureSelection as ga
from hashlib import blake2b
from hmac import compare_digest

import MySQLdb
from random import randint


QUERY='SELECT a,b,c,d FROM data;'
conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='watermark')

SECRET_KEY = b'secret key'
AUTH_SIZE = 8

def copy_data_from_src_to_dest(src,dest):
	model.delete_everything_table(conn,dest)
	param=model.fetch_from_table(conn,src)
	model.insert_param_into_table(conn,dest,param)

def copy_data_from_src_to_dest1(src,dest):
	model.delete_everything_table(conn,dest)
	param=model.fetch_from_table(conn,src)
	print("param",param)
	param1=[]
	for m in param:
		print(m[1],m[2])
		param1.append([m[0],m[1]+10,m[2]+20,m[3]+30,m[4]+40])
		
	model.insert_param_into_table1(conn,dest,param1)


def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')
    
    
def verify(cookie, sig):
     good_sig = sign(cookie)
     return compare_digest(good_sig, sig)


def selectKey():
	value = randint(1, 9)
	print(value)
	curr=conn.cursor()
	curr.execute("SELECT * FROM keyvalue where id=%d"%(value,))
	rows=curr.fetchall()
	print(rows[0][0])
	print(rows[0][1])
	b=rows[0][1]
	return b

def selectKeyValue(key1):
	key=["10","20","30","40","50","60","70","80","90","100"]
	keys=""
	for pubkey in key:
		res = bytes(pubkey, 'utf-8')
		sig = sign(res)
		f=sig.decode('utf-8')
		print(f)
		if f==key1:
			print("equal")
			print(pubkey)
			keys=pubkey
	
	return keys


def DataProcess():
	cur=conn.cursor()
	cur.execute(QUERY)
	rows=cur.fetchall()
	fullheader=[]
	# Continue only if there are rows returned.
	if rows:
	    # New empty list called 'result'. This will be written to a file.
	    result = list()
	
	    # The row name is the first entry for each entity in the description tuple.
	    column_names = list()
	    for i in cur.description:
	        column_names.append(i[0])
	    fullheader.append(column_names)
	    result.append(column_names)
	    for row in rows:
	        result.append(row)
	        
	    i=0

	    # Write result to file.
	    with open("dataset.csv", 'w', newline='') as csvfile:
	        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	        for row in result:
	            if i<5000:	
	            	csvwriter.writerow(row)
	            	i=i+1
	else:
	    sys.exit("No rows found for query: {}".format(sql))
	
	try:    
		header=ga.gafeature('dataset.csv')
		print("erere")
		print(header)
	except:
		header=[]
		pass
	print("len",len(header))
	print("Full Header",fullheader)
	print("Header",header)
	feature=[]

	if len(header)==0:
		feature=[fullheader[0][0],fullheader[0][1]]	
	if len(header)==1:
		f=fullheader[0]
		d=header[0]
		f.remove(d)
		feature=[header[0],f[0]]
	if len(header)==2:
		feature=[header[0],header[1]]
	if len(header)>2:
		feature=[header[0],header[1]]	
	print(feature)	

	
	return feature[0],feature[1]


	
def KeyProcess():
	key=["10","20","30","40","50","60","70","80","90","100"]
	i=0
	curr=conn.cursor()
	curr.execute("delete from keyvalue")
	conn.commit()
	
	for pubkey in key:
		#pubkey = b'10'
		print(pubkey)
		res = bytes(pubkey, 'utf-8')
		print(res)
		sig = sign(res)
		print(sig)
		print("{0},{1}".format(res.decode('utf-8'), sig))
		print(res.decode('utf-8'))
		print(sig.decode('utf-8'))
		print(verify(res, sig))
		i=i+1
		print(i)
		#sql="INSERT INTO keyvalue VALUES (%d,%s)"%(i,i)"
		
		dd=sig.decode('utf-8')
		print(dd)
		curr.execute("INSERT INTO keyvalue VALUES (%s,%s)",(i,dd,))
		conn.commit()
		print ("inserted_sucessfully")
	copy_data_from_src_to_dest('data','data2')		

#f=DataProcess()
#print("f value",f)