import sqlite3
from collections import OrderedDict


def connectDb(path):
	return sqlite3.connect(path)


def create_table(path):
	db = sqlite3.connect(path)
	db.execute("drop table if exists bid")
	query = "create table bid (orderId text, price int, quantity int, company text, \
			exchange text, time datetime)"
	db.execute(query)
	db.execute("drop table if exists ask")
	query = "create table ask (orderId text, price int, quantity int, company text, \
			exchange text, time datetime)"
	db.execute(query)
	db.close()


def insert(path, **kwargs):
	db = sqlite3.connect(path)
	if kwargs['bidorask'] == 1:
		query = "insert into bid (orderId, price, quantity, company, exchange, time) \
				values (?, ?, ?, ?, ?, ?)"
		db.execute(query, (kwargs['orderId'], kwargs['price'], kwargs['quantity'], 
			kwargs['company'], kwargs['exchange'], kwargs['time']))
	else:
		query = "insert into ask (orderId, price, quantity, company, exchange, time) \
				values (?, ?, ?, ?, ?, ?)"
		db.execute(query, (kwargs['orderId'], kwargs['price'], kwargs['quantity'], 
			kwargs['company'], kwargs['exchange'], kwargs['time']))
	db.commit()
	db.close()


def retrieveAll(path, tname):
	db = sqlite3.connect(path)
	cursor = db.execute("select * from {0}".format(tname))
	db.close()
	return cursor.fetchall()


def retrieve(path, company, exchange, n):
	db = sqlite3.connect(path)
	query = "select price, quantity from bid where company = ? and exchange = ?\
			order by price desc limit ?"
	cursor1 = db.execute(query, (company, exchange, n))
	query = "select price, quantity from ask where company = ? and exchange = ?\
			order by price limit ?"
	cursor2 = db.execute(query, (company, exchange, n))
	bid = OrderedDict()
	ask = OrderedDict()
	for i, v in enumerate(cursor1.fetchall()):
		bid[i] = tuple(v)
	for i, v in enumerate(cursor2.fetchall()):
		ask[i] = tuple(v)	
	db.close()
	return bid, ask


def update(db, id, **kwargs):
	db = sqlite3.connect(path)
	if kwargs['bidorask'] == 1:
		query = "update bid set price = {0}, quantity = {1} where orderId = {2}".format(kwargs['price'], 
				kwargs['quantity'], id)
	else:
		query = "update ask set price = {0}, quantity = {1} where orderId = {2}".format(kwargs['price'], 
				kwargs['quantity'], id)
	db.execute(query)
	db.commit()
	db.close()


def delete(db, tname, id):
	query = 'delete from {0} where orderId = {1}'.format(tname, id)
	db.execute(query)
	db.commit()
	db.close()
