import mysql.connector as mariadb
import time
import json
import datetime
from yahoo_finance import Share
from apscheduler.schedulers.blocking import BlockingScheduler

def yahooDownloader():
	mariadb_connection=mariadb.connect(user='root', password='xxx', database='Bourse', host='192.168.1.51')
	cursor = mariadb_connection.cursor()

	sql="SELECT ISIN, SYMBOL_YAHOO_FINANCE FROM titre"

	yahooFinanceDataFile=open('yahooFinanceData', 'w')
	symbolErrorFile=open('symbolError', 'w')

	dateFrom = datetime.date.today() + datetime.timedelta(days=-7)
	dateFromStr = dateFrom.strftime('%Y-%m-%d')
	dateTo = datetime.date.today()
	dateToStr = dateTo.strftime('%Y-%m-%d')

	try:
		cursor.execute(sql)
		results=cursor.fetchall()
	except:
		print "Error: unable to fecth data"

	for row in results:
		isin = str(row[0])
		symbolYahoo = str(row[1])
		print symbolYahoo
		try:
			historical_json_list = json.loads(json.dumps(Share(symbolYahoo).get_historical(dateFromStr, dateToStr)))
		except:
			symbolErrorFile.write(isin + ' ' + symbolYahoo + '\n')

		for i, elt in enumerate(historical_json_list):
				sql_insert="REPLACE INTO cotations (ISIN, DATE_COTATION, OUVERTURE, HAUT, BAS, CLOTURE, VOLUME) VALUES (%s,%s,%s,%s,%s,%s,%s)"
				data = (isin, elt['Date'],elt['Open'],elt['High'],elt['Low'], elt['Close'],elt['Volume'])
				yahooFinanceDataFile.write(str(data) + '\n')
				cursor.execute(sql_insert, data)

	mariadb_connection.close()

scheduler = BlockingScheduler()
scheduler.add_job(yahooDownloader, 'interval', hours=2)
scheduler.start()
