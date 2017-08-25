# -*- coding: utf-8 -*-
import re
import scrapy
from datetime import datetime
from scrapy.exceptions import CloseSpider
from amac.items import FundItem, InstItem
from amac.utils.get import get_key
from amac.settings import SQL_DATETIME_FORMAT


class ZhengquanSpider(scrapy.Spider):
	name = 'inst'
	allowed_domains = ['gs.amac.org.cn']
	url1 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/{}.html'
	url2 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/{}.html'

	def start_requests(self):
		while True:
			amac_managerId = get_key('amac_managerId')
		# amac_managerIds = [101000000224, 101000000213, 101000003335, 101000000308]
		# for amac_managerId in amac_managerIds:
			if not amac_managerId:
				raise CloseSpider()
			item = InstItem()
			item['managerId'] = amac_managerId
			url = self.url2.format(amac_managerId)
			yield scrapy.Request(url, meta={'item': item}, dont_filter=True)

	def parse(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		res = response.xpath('//html/body/div[1]/div[2]/div/table/tbody')
		integrityInfo = res.xpath('./tr[1]/td[2]//text()').extract_first()
		managerNameCh = response.xpath('.//*[@id="complaint2"]/text()').extract_first()
		managerNameEn = res.xpath('./tr[4]/td[2]/text()').extract_first()
		registNo = res.xpath('./tr[5]/td[2]/text()').extract_first()
		orgInsNo = res.xpath('./tr[6]/td[2]/text()').extract_first()
		registDate = res.xpath('./tr[7]/td[2]/text()').extract_first()
		manEstablishDate = res.xpath('./tr[7]/td[4]/text()').extract_first()
		registAddress = res.xpath('./tr[8]/td[2]/text()').extract_first()
		officalAddress = res.xpath('./tr[9]/td[2]/text()').extract_first()
		registAmountWan = res.xpath('./tr[10]/td[2]/text()').extract_first()
		actualPayAmountWan = res.xpath('./tr[10]/td[4]/text()').extract_first()

		commProperty = res.xpath('./tr[11]/td[2]/text()').extract_first()
		percent = res.xpath('./tr[11]/td[4]/text()').extract_first()
		institutionType = res.xpath('./tr[12]/td[2]/text()').extract_first()
		businessType = res.xpath('./tr[12]/td[4]/text()').extract_first()
		employNo = res.xpath('./tr[13]/td[2]/text()').extract_first()
		institutionURL = res.xpath('./tr[13]/td[4]/a/text()').extract_first()
		isMember = res.xpath('./tr[15]/td[2]/text()').extract_first()
		if '当前会员类型' not in response.text and '律师事务所名称' not in response.text:
			memberType = ''
			inTime = ''

			legalState = res.xpath('./tr[17]/td[2]//text()').extract_first()
			lawOfficeName = ''
			lawyerName = ''

			legalPersonName = res.xpath('./tr[19]/td[2]/text()').extract_first()
			isWorkRequire = res.xpath('./tr[20]/td[2]/text()').extract_first()
			getRequireWay = res.xpath('./tr[20]/td[4]/text()').extract_first()

			legalPersonRecord_tags = res.xpath('./tr[21]/td[2]/table[1]/tbody/tr')
			legalPersonRecord = []
			for tag in legalPersonRecord_tags:
				officeTime = tag.xpath('./td[1]/text()').extract_first()
				officeComm = tag.xpath('./td[2]/text()').extract_first()
				officeDuty = tag.xpath('./td[3]/text()').extract_first()
				legalPersonRecord.append(
					{'officeTime': self.strp(officeTime), 'officeComm': self.strp(officeComm),
					 'officeDuty': self.strp(officeDuty)})
			legalPersonRecord = str(legalPersonRecord)

			topManagerCase_tags = res.xpath('./tr[22]/td[2]/table[1]/tbody/tr')
			topManagerCase = []
			for ta in topManagerCase_tags:
				topName = ta.xpath('./td[1]/text()').extract_first()
				topDuty = ta.xpath('./td[2]/text()').extract_first()
				topIsHave = ta.xpath('./td[3]/text()').extract_first()
				topManagerCase.append(
					{'topName': self.strp(topName), 'topDuty': self.strp(topDuty), 'topIsHave': self.strp(topIsHave)})
			topManagerCase = str(topManagerCase)

			beforeFund_tags = res.xpath('./tr[24]/td[2]/p[position() mod 2 != 0]')
			beforeFund = []
			for t in beforeFund_tags:
				beforeFundId_url = t.xpath('./a/@href').extract_first()
				beforeFundId = re.search(r'\d+', beforeFundId_url).group() if beforeFundId_url else ''
				beforeFundName = t.xpath('./a/text()').extract_first()
				beforeFund.append(
					{'beforeFundId': self.strp(beforeFundId), 'beforeFundName': self.strp(beforeFundName)})
			beforeFund = str(beforeFund)

			laterFund_tags = res.xpath('./tr[25]/td[2]/p[position() mod 2 != 0]')
			laterFund = []
			for t in laterFund_tags:
				laterFundId_url = t.xpath('./a/@href').extract_first()
				laterFundId = re.search(r'\d+', laterFundId_url).group() if laterFundId_url else ''
				laterFundName = t.xpath('./a/text()').extract_first()
				laterFund.append({'laterFundId': self.strp(laterFundId), 'laterFundName': self.strp(laterFundName)})
			laterFund = str(laterFund)

			insInfoUpdate = res.xpath('./tr[27]/td[2]/text()').extract_first()
		elif '当前会员类型' in response.text and '律师事务所名称' not in response.text:
			"""有会员，无律师，向后错一位"""
			memberType = res.xpath('./tr[16]/td[2]/text()').extract_first()
			inTime = res.xpath('./tr[16]/td[4]/text()').extract_first()

			legalState = res.xpath('./tr[18]/td[2]//text()').extract_first()
			lawOfficeName = ''
			lawyerName = ''

			legalPersonName = res.xpath('./tr[20]/td[2]/text()').extract_first()
			isWorkRequire = res.xpath('./tr[21]/td[2]/text()').extract_first()
			getRequireWay = res.xpath('./tr[21]/td[4]/text()').extract_first()

			legalPersonRecord_tags = res.xpath('./tr[22]/td[2]/table[1]/tbody/tr')
			legalPersonRecord = []
			for tag in legalPersonRecord_tags:
				officeTime = tag.xpath('./td[1]/text()').extract_first()
				officeComm = tag.xpath('./td[2]/text()').extract_first()
				officeDuty = tag.xpath('./td[3]/text()').extract_first()
				legalPersonRecord.append(
					{'officeTime': self.strp(officeTime), 'officeComm': self.strp(officeComm),
					 'officeDuty': self.strp(officeDuty)})
			legalPersonRecord = str(legalPersonRecord)
			topManagerCase_tags = res.xpath('./tr[23]/td[2]/table[1]/tbody/tr')
			topManagerCase = []
			for ta in topManagerCase_tags:
				topName = ta.xpath('./td[1]/text()').extract_first()
				topDuty = ta.xpath('./td[2]/text()').extract_first()
				topIsHave = ta.xpath('./td[3]/text()').extract_first()
				topManagerCase.append(
					{'topName': self.strp(topName), 'topDuty': self.strp(topDuty), 'topIsHave': self.strp(topIsHave)})
			topManagerCase = str(topManagerCase)

			beforeFund_tags = res.xpath('./tr[25]/td[2]/p[position() mod 2 != 0]')
			beforeFund = []
			for t in beforeFund_tags:
				beforeFundId_url = t.xpath('./a/@href').extract_first()
				beforeFundId = re.search(r'\d+', beforeFundId_url).group() if beforeFundId_url else ''
				beforeFundName = t.xpath('./a/text()').extract_first()
				beforeFund.append(
					{'beforeFundId': self.strp(beforeFundId), 'beforeFundName': self.strp(beforeFundName)})
			beforeFund = str(beforeFund)

			laterFund_tags = res.xpath('./tr[26]/td[2]/p[position() mod 2 != 0]')
			laterFund = []
			for t in laterFund_tags:
				laterFundId_url = t.xpath('./a/@href').extract_first()
				laterFundId = re.search(r'\d+', laterFundId_url).group() if laterFundId_url else ''
				laterFundName = t.xpath('./a/text()').extract_first()
				laterFund.append({'laterFundId': self.strp(laterFundId), 'laterFundName': self.strp(laterFundName)})
			laterFund = str(laterFund)

			insInfoUpdate = res.xpath('./tr[28]/td[2]/text()').extract_first()
		elif '当前会员类型' not in response.text and '律师事务所名称' in response.text:
			"""无会员，有律师，向后错两位"""
			memberType = ''
			inTime = ''

			legalState = res.xpath('./tr[17]/td[2]//text()').extract_first()
			lawOfficeName = res.xpath('./tr[18]/td[2]//text()').extract_first()
			lawyerName = res.xpath('./tr[19]/td[2]//text()').extract_first()

			legalPersonName = res.xpath('./tr[21]/td[2]/text()').extract_first()
			isWorkRequire = res.xpath('./tr[22]/td[2]/text()').extract_first()
			getRequireWay = res.xpath('./tr[22]/td[4]/text()').extract_first()

			legalPersonRecord_tags = res.xpath('./tr[23]/td[2]/table[1]/tbody/tr')
			legalPersonRecord = []
			for tag in legalPersonRecord_tags:
				officeTime = tag.xpath('./td[1]/text()').extract_first()
				officeComm = tag.xpath('./td[2]/text()').extract_first()
				officeDuty = tag.xpath('./td[3]/text()').extract_first()
				legalPersonRecord.append(
					{'officeTime': self.strp(officeTime), 'officeComm': self.strp(officeComm),
					 'officeDuty': self.strp(officeDuty)})
			legalPersonRecord = str(legalPersonRecord)
			topManagerCase_tags = res.xpath('./tr[24]/td[2]/table[1]/tbody/tr')
			topManagerCase = []
			for ta in topManagerCase_tags:
				topName = ta.xpath('./td[1]/text()').extract_first()
				topDuty = ta.xpath('./td[2]/text()').extract_first()
				topIsHave = ta.xpath('./td[3]/text()').extract_first()
				topManagerCase.append(
					{'topName': self.strp(topName), 'topDuty': self.strp(topDuty), 'topIsHave': self.strp(topIsHave)})
			topManagerCase = str(topManagerCase)

			beforeFund_tags = res.xpath('./tr[26]/td[2]/p[position() mod 2 != 0]')
			beforeFund = []
			for t in beforeFund_tags:
				beforeFundId_url = t.xpath('./a/@href').extract_first()
				beforeFundId = re.search(r'\d+', beforeFundId_url).group() if beforeFundId_url else ''
				beforeFundName = t.xpath('./a/text()').extract_first()
				beforeFund.append(
					{'beforeFundId': self.strp(beforeFundId), 'beforeFundName': self.strp(beforeFundName)})
			beforeFund = str(beforeFund)

			laterFund_tags = res.xpath('./tr[27]/td[2]/p[position() mod 2 != 0]')
			laterFund = []
			for t in laterFund_tags:
				laterFundId_url = t.xpath('./a/@href').extract_first()
				laterFundId = re.search(r'\d+', laterFundId_url).group() if laterFundId_url else ''
				laterFundName = t.xpath('./a/text()').extract_first()
				laterFund.append({'laterFundId': self.strp(laterFundId), 'laterFundName': self.strp(laterFundName)})
			laterFund = str(laterFund)

			insInfoUpdate = res.xpath('./tr[29]/td[2]/text()').extract_first()
		else:
			"""有会员，有律师，向后错三位"""
			memberType = res.xpath('./tr[16]/td[2]/text()').extract_first()
			inTime = res.xpath('./tr[16]/td[4]/text()').extract_first()

			legalState = res.xpath('./tr[18]/td[2]//text()').extract_first()
			lawOfficeName = res.xpath('./tr[19]/td[2]//text()').extract_first()
			lawyerName = res.xpath('./tr[20]/td[2]//text()').extract_first()

			legalPersonName = res.xpath('./tr[22]/td[2]/text()').extract_first()
			isWorkRequire = res.xpath('./tr[23]/td[2]/text()').extract_first()
			getRequireWay = res.xpath('./tr[23]/td[4]/text()').extract_first()

			legalPersonRecord_tags = res.xpath('./tr[24]/td[2]/table[1]/tbody/tr')
			legalPersonRecord = []
			for tag in legalPersonRecord_tags:
				officeTime = tag.xpath('./td[1]/text()').extract_first()
				officeComm = tag.xpath('./td[2]/text()').extract_first()
				officeDuty = tag.xpath('./td[3]/text()').extract_first()
				legalPersonRecord.append(
					{'officeTime': self.strp(officeTime), 'officeComm': self.strp(officeComm),
					 'officeDuty': self.strp(officeDuty)})
			legalPersonRecord = str(legalPersonRecord)
			topManagerCase_tags = res.xpath('./tr[25]/td[2]/table[1]/tbody/tr')
			topManagerCase = []
			for ta in topManagerCase_tags:
				topName = ta.xpath('./td[1]/text()').extract_first()
				topDuty = ta.xpath('./td[2]/text()').extract_first()
				topIsHave = ta.xpath('./td[3]/text()').extract_first()
				topManagerCase.append(
					{'topName': self.strp(topName), 'topDuty': self.strp(topDuty), 'topIsHave': self.strp(topIsHave)})
			topManagerCase = str(topManagerCase)

			beforeFund_tags = res.xpath('./tr[27]/td[2]/p[position() mod 2 != 0]')
			beforeFund = []
			for t in beforeFund_tags:
				beforeFundId_url = t.xpath('./a/@href').extract_first()
				beforeFundId = re.search(r'\d+', beforeFundId_url).group() if beforeFundId_url else ''
				beforeFundName = t.xpath('./a/text()').extract_first()
				beforeFund.append(
					{'beforeFundId': self.strp(beforeFundId), 'beforeFundName': self.strp(beforeFundName)})
			beforeFund = str(beforeFund)

			laterFund_tags = res.xpath('./tr[28]/td[2]/p[position() mod 2 != 0]')
			laterFund = []
			for t in laterFund_tags:
				laterFundId_url = t.xpath('./a/@href').extract_first()
				laterFundId = re.search(r'\d+', laterFundId_url).group() if laterFundId_url else ''
				laterFundName = t.xpath('./a/text()').extract_first()
				laterFund.append({'laterFundId': self.strp(laterFundId), 'laterFundName': self.strp(laterFundName)})
			laterFund = str(laterFund)

			insInfoUpdate = res.xpath('./tr[30]/td[2]/text()').extract_first()
		insSuggestion = response.xpath('.//*[@id="specialInfos"]/text()').extract_first()







		item["integrityInfo"] = self.strp(integrityInfo)
		item["managerNameCh"] = self.strp(managerNameCh)
		item["managerNameEn"] = self.strp(managerNameEn)
		item["registNo"] = self.strp(registNo)
		item["orgInsNo"] = self.strp(orgInsNo)
		item["registDate"] = self.strp(registDate)
		item["manEstablishDate"] = self.strp(manEstablishDate)
		item["registAddress"] = self.strp(registAddress)
		item["officalAddress"] = self.strp(officalAddress)
		item["registAmountWan"] = self.strp(registAmountWan)
		item["actualPayAmountWan"] = self.strp(actualPayAmountWan)
		item["commProperty"] = self.strp(commProperty)
		item["percent"] = self.strp(percent)
		item["institutionType"] = self.strp(institutionType)
		item["businessType"] = self.strp(businessType)
		item["employNo"] = self.strp(employNo)
		item["institutionURL"] = self.strp(institutionURL)

		item["isMember"] = self.strp(isMember)
		item["memberType"] = self.strp(memberType)
		item["inTime"] = self.strp(inTime)

		item["legalState"] = self.strp(legalState)
		item["lawOfficeName"] = self.strp(lawOfficeName)
		item["lawyerName"] = self.strp(lawyerName)

		item["legalPersonName"] = self.strp(legalPersonName)
		item["isWorkRequire"] = self.strp(isWorkRequire)
		item["getRequireWay"] = self.strp(getRequireWay)
		item["legalPersonRecord"] = self.strp(legalPersonRecord)
		item["topManagerCase"] = self.strp(topManagerCase)
		item["beforeFund"] = self.strp(beforeFund)
		item["laterFund"] = self.strp(laterFund)
		item["insInfoUpdate"] = self.strp(insInfoUpdate)
		item["insSuggestion"] = self.strp(insSuggestion)
		item["crawlTime"] = datetime.now().strftime(SQL_DATETIME_FORMAT)
		yield item

	def strp(self, s):
		x = s.strip() if s else ''
		return x
