# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from amac.items import FundItem, InstItem


class MysqlPipeline(object):
	"""
	本机 localhost；公司 etl2.innotree.org；服务器 etl1.innotree.org
	"""

	def __init__(self):
		self.conn = pymysql.connect(host='etl1.innotree.org', port=3308, user='spider', password='spider', db='spider',
		                            charset='utf8', cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if isinstance(item, FundItem):
			# sql = """insert into kuchuan_all(id, app_package, down, trend) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE app_package=VALUES(app_package), down=VALUES(down), down=VALUES(trend)"""
			sql = """replace into amac_fund_copy(fundId, putOnRecordState, fundType, moneyType, investField,
 					fundUpdate, suggestion, monthly, halfYearly, yearly, quarterly, crawlTime)
 					VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = (
				item["fundId"], item["putOnRecordState"], item["fundType"], item["moneyType"], item["investField"],
				item["fundUpdate"],
				item["suggestion"], item["monthly"], item["halfYearly"], item["yearly"], item["quarterly"],
				item["crawlTime"])
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			print(str(item['fundId']))
		elif isinstance(item, InstItem):
			"""
			managerId, integrityInfo, managerNameCh, managerNameEn, registNo, orgInsNo, registDate, manEstablishDate, registAddress, officalAddress, registAmountWan, actualPayAmountWan, commProperty, percent, institutionType, businessType, employNo, institutionURL, isMember, memberType, inTime, legalState, legalPersonName, isWorkRequire, getRequireWay, legalPersonRecord, topManagerCase, beforeFund, laterFund, insInfoUpdate, insSuggestion, crawl_time"""
			sql = """replace into amac_institution(
									managerId, integrityInfo, managerNameCh, managerNameEn, registNo, 
									orgInsNo, registDate, manEstablishDate, registAddress, officalAddress, 
									registAmountWan, actualPayAmountWan, commProperty, percent, institutionType, 
									businessType, employNo, institutionURL, isMember, memberType, 
									inTime, legalState, legalPersonName, isWorkRequire, getRequireWay, 
									legalPersonRecord, topManagerCase, beforeFund, laterFund, insInfoUpdate, 
									insSuggestion, crawlTime
			 					)
			 					VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			args = (
				item["managerId"], item["integrityInfo"], item["managerNameCh"], item["managerNameEn"], item["registNo"],
				item["orgInsNo"], item["registDate"], item["manEstablishDate"], item["registAddress"], item["officalAddress"],
				item["registAmountWan"], item["actualPayAmountWan"], item["commProperty"], item["percent"], item["institutionType"],
				item["businessType"], item["employNo"], item["institutionURL"], item["isMember"], item["memberType"],
				item["inTime"], item["legalState"], item["legalPersonName"], item["isWorkRequire"], item["getRequireWay"],
				item["legalPersonRecord"], item["topManagerCase"], item["beforeFund"], item["laterFund"], item["insInfoUpdate"],
				item["insSuggestion"], item["crawlTime"]
			)
			self.cursor.execute(sql, args=args)
			self.conn.commit()
			print(str(item['managerId']))
