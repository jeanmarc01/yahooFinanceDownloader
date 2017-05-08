import sys
from yahoo_finance import Share
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler

def my_job():
	print(Share('YHOO').get_open())

scheduler = BlockingScheduler()
scheduler.add_job(my_job, 'interval', minutes=1)
scheduler.start()

