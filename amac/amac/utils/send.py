# coding:utf-8

import os
import sys
import time
from datetime import datetime
from os.path import dirname

import pymysql
from my_redis import QueueRedis

# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

father_path = os.path.abspath(dirname(__file__))
sys.path.append(father_path)


def send_key(key1, key2):
	"""
		本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
		"""
	mysql = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	try:
		with mysql.cursor() as cursor:
			sql = """select fundId, managerId from amac_fund"""
			print('execute begain')
			cursor.execute(sql)
			results = cursor.fetchall()
			fundIds = [result['fundId'] for result in results]
			managerIds = [result['managerId'] for result in results]
			managerIdSet = set(managerIds)

	finally:
		mysql.close()

	red = QueueRedis()

	if fundIds and managerIdSet:
		for fundId, managerId in zip(fundIds, managerIdSet):
			red.send_to_queue(key1, fundId)
			red.send_to_queue(key2, managerId)


if __name__ == '__main__':
	send_key(key1='amac_fundId', key2='amac_managerId')
