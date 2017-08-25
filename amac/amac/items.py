# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundItem(scrapy.Item):
	fundId = scrapy.Field()
	putOnRecordState = scrapy.Field()
	fundType = scrapy.Field()
	moneyType = scrapy.Field()
	investField = scrapy.Field()
	fundUpdate = scrapy.Field()
	suggestion = scrapy.Field()
	monthly = scrapy.Field()
	halfYearly = scrapy.Field()
	yearly = scrapy.Field()
	quarterly = scrapy.Field()
	crawlTime = scrapy.Field()


class InstItem(scrapy.Item):
	'''
	//html/body/div[1]/div[2]/div/table/tbody
	'''
	managerId = scrapy.Field()
	integrityInfo = scrapy.Field()
	managerNameCh = scrapy.Field()
	managerNameEn = scrapy.Field()
	registNo = scrapy.Field()
	orgInsNo = scrapy.Field()
	registDate = scrapy.Field()
	manEstablishDate = scrapy.Field()
	registAddress = scrapy.Field()
	officalAddress = scrapy.Field()
	registAmountWan = scrapy.Field()
	actualPayAmountWan = scrapy.Field()
	commProperty = scrapy.Field()
	percent = scrapy.Field()
	institutionType = scrapy.Field()
	businessType = scrapy.Field()
	employNo = scrapy.Field()
	institutionURL = scrapy.Field()
	isMember = scrapy.Field()
	memberType = scrapy.Field()
	inTime = scrapy.Field()
	legalState = scrapy.Field()
	lawOfficeName = scrapy.Field()
	lawyerName = scrapy.Field()
	legalPersonName = scrapy.Field()
	isWorkRequire = scrapy.Field()
	getRequireWay = scrapy.Field()
	legalPersonRecord = scrapy.Field()
	topManagerCase = scrapy.Field()
	beforeFund = scrapy.Field()
	laterFund = scrapy.Field()
	insInfoUpdate = scrapy.Field()
	insSuggestion = scrapy.Field()
	crawlTime = scrapy.Field()
