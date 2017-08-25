import requests
import json
import re
import pymysql
import time


def fmat_stamp(t):
	ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t / 1000)) if t else time.strftime("%Y-%m-%d %H:%M:%S",
	                                                                                          time.localtime(0 / 1000))
	return ti


def inser(page):
	mysql = pymysql.connect(host='etl2.innotree.org', port=3308, user='spider', password='spider', db='spider',
	                        charset='utf8', cursorclass=pymysql.cursors.DictCursor)
	cursor = mysql.cursor()

	url = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund"

	querystring = {"rand": "0.32345230476650366", "page": "{}".format(page), "size": "10000"}

	payload = "{}"

	headers = {
		'host': "gs.amac.org.cn",
		'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
		'accept': "application/json, text/javascript, */*; q=0.01",
		'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		'accept-encoding': "gzip, deflate",
		'content-type': "application/json",
		'x-requested-with': "XMLHttpRequest",
		'referer': "http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html",
		'content-length': "2",
		'connection': "keep-alive",
		'cache-control': "no-cache",
		'postman-token': "7e72d1ab-b8d0-ba6a-bfe2-a29ecc52e886"
	}
	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

	j = json.loads(response.text)
	content = j.get('content', [])

	try:
		li = []
		for c in content:
			fundId = int(c.get('id', 0))
			fundName = c.get('fundName', "")
			fundNo = c.get('fundNo', "")
			establishDate = fmat_stamp(c.get('establishDate', ""))
			putOnRecordDate = fmat_stamp(c.get('putOnRecordDate', ""))
			managerName = c.get('managerName', "")

			managerUrl = c.get('managerUrl', "")
			managerId = re.search(r'\d+', managerUrl).group()
			managerType = c.get('managerType', "")
			mandatorName = c.get('mandatorName', "")
			workingState = c.get('workingState', "")
			sql = """replace into amac_fund_copy (fundId, fundName, fundNo, establishDate, putOnRecordDate, managerName, managerId, managerType, mandatorName, workingState) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = (fundId, fundName, fundNo, establishDate, putOnRecordDate, managerName, managerId, managerType,
			        mandatorName, workingState)
			li.append(args)
			# print(fundName)
		cursor.executemany(sql, li)
		mysql.commit()
	except Exception as e:
		print(e)
	finally:
		mysql.close()


if __name__ == '__main__':
	for page in range(8):
		print(page)
		inser(page)
