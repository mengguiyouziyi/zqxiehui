# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.exceptions import CloseSpider
from amac.items import FundItem, InstItem
from amac.utils.get import get_key
from amac.settings import SQL_DATETIME_FORMAT


class ZhengquanSpider(scrapy.Spider):
	name = 'fund'
	allowed_domains = ['gs.amac.org.cn']
	url1 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/{}.html'
	url2 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/{}.html'

	def start_requests(self):
		while True:
			amac_fundId = get_key('amac_fundId')
		# amac_fundIds = [351000768734, 351000128364]
		# for amac_fundId in amac_fundIds:
			if not amac_fundId:
				raise CloseSpider()
			item = FundItem()
			item['fundId'] = amac_fundId
			url = self.url1.format(amac_fundId)
			yield scrapy.Request(url, meta={'item': item}, dont_filter=True)

	def parse(self, response):
		item = response.meta.get('item', '')
		if not item:
			return
		putOnRecordState = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[5]/td[2]/text()').extract_first()
		fundType = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[6]/td[2]/text()').extract_first()
		moneyType = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[7]/td[2]/text()').extract_first()
		investField = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[11]/td[2]/text()').extract_first()
		fundUpdate = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[13]/td[2]/text()').extract_first()
		suggestion = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[14]/td[2]/text()').extract_first()
		monthly = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[16]/td[2]/text()').extract_first()
		halfYearly = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[17]/td[2]/text()').extract_first()
		yearly = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[18]/td[2]/text()').extract_first()
		quarterly = response.xpath('//html/body/div[1]/div[2]/div/table/tbody/tr[19]/td[2]/text()').extract_first()

		item["putOnRecordState"] = putOnRecordState
		item["fundType"] = fundType
		item["moneyType"] = moneyType
		item["investField"] = investField
		item["fundUpdate"] = fundUpdate
		item["suggestion"] = suggestion
		item["monthly"] = monthly
		item["halfYearly"] = halfYearly
		item["yearly"] = yearly
		item["quarterly"] = quarterly
		item["crawlTime"] = datetime.now().strftime(SQL_DATETIME_FORMAT)
		yield item