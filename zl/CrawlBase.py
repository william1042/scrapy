from collections import defaultdict
import random,re,os
from PyQt5.QtCore import QThread
import requests
from bs4 import BeautifulSoup
import sqlite3


class CrawlBase(QThread):
	def __init__(self):
		super().__init__()
		self.user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
                   ]
		self.IPList = self.getListProxies()
		self.headers = {}
		self.proxies = {}
		self.job_infos = []													#保存信息到内存中（暂时）
		

	#生成url 队列
	def generateUrl(self):
		pass

	def processUrl(self):
		pass

	def crawl(self,url):
		pass

	#随机从列选择使用
	def getRandomUserAgent(self):
		index = random.randint(0,len(self.user_agents) - 1)
		self.headers = {
			'user-agent' : self.user_agents[index]
		}

	#随机从列表选取使用
	def getRandomIP(self):
		index = random.randint(0,len(self.IPList) - 1)
		self.proxies = self.IPList[index]

	#获取代理IP
	def getListProxies(self):  
		session = requests.session()
		self.getRandomUserAgent()  
		page = session.get("http://www.xicidaili.com/nn", headers=self.headers)  
		soup = BeautifulSoup(page.text, 'lxml')  

		proxyList = []  
		taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})  
		for trtag in taglist:  
		    tdlist = trtag.find_all('td')  
		    proxy = { 'https': tdlist[1].string + ':' + tdlist[2].string }  
		    proxyList.append(proxy)  

		return proxyList
	
	#对工资划分区间，用于绘图，原始数据未改变
	def salaryHandle(self):
		fileName = 'salary_for_image.csv'
		salarys = defaultdict(int)
		#便于绘图，划分区间
		for job_info in self.job_infos:
			salary = job_info['salary'].split('-')

			if len(salary) == 2:
				salary = (int(salary[0]) + int(salary[1])) / 2
			else:
				salary = -1

			if salary >= 0 and salary < 5000:
				salarys['0-5K'] += 1
			elif salary >= 5000 and salary < 8000:
				salarys['5K-8K'] += 1
			elif salary >= 8000 and salary <= 12000:
				salarys['8K-12K'] += 1
			elif salary >= 12000 and salary <= 15000:
				salarys['12K-15K'] += 1
			else:
				salarys['15K-~'] += 1

		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			f.write(str('薪水') + '\n')
			for salary, num in salarys.items():
				f.write(str(salary) + ',')
				f.write(str(num) + '\n')


	#对位置分类并统计
	def positionHandle(self):
		fileName = 'position_for_image.csv'
		positions = defaultdict(int)

		for job_info in self.job_infos:
				position = job_info['position'].split('-')
				if len(position) == 2:
					position = position[1]
				else:
					position = position[0]
				positions[position] += 1

		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			f.write(str('位置') + '\n')
			for position, num in positions.items():
				f.write(str(position) + ',')
				f.write(str(num) + '\n')

	#保存文件到txt
	def staffHandle(self):
		fileName = 'staff.txt'
		with open(self.file_path + fileName, 'w', encoding='utf-8') as f:
			for job_info in self.job_infos:
				f.write(str(job_info['staff']) + ',' + str(job_info['details_url'] + '\n'))


	#保存所有信息，使用sqlite3数据库存储
	def saveAll(self, tableName, db):
		cursor = db.cursor()
		cursor.execute("DELETE FROM %s" % (tableName))

		for job in self.job_infos:
			cursor.execute("INSERT INTO %s (staff, salary, position, details_url) values (?, ?, ?, ?)" % 
				(tableName) , (job['staff'], job['salary'], job['position'], job['details_url']))

		cursor.execute("UPDATE latestType SET latest_type = ? WHERE id = ?",(tableName,1))
		cursor.close()
		db.commit()

	#初始化数据库（若文件不存在，则创建数据库）
	def InitDB(self):
		if os.path.isfile(os.getcwd() + '/resource/jobs.db'):
			db = sqlite3.connect(os.getcwd() + '/resource/jobs.db')
			return db
		else:
			db = sqlite3.connect(os.getcwd() + '/resource/jobs.db')
			cursor = db.cursor()
			cursor.execute('CREATE TABLE zhilian (staff text, salary varchar(20), position varchar(20), details_url text)')
			cursor.execute('CREATE TABLE lagou (staff text, salary varchar(20), position varchar(20), details_url text)')
			cursor.execute('CREATE TABLE latestType (id INTEGER, latest_type varchar(20))')
			cursor.execute('INSERT INTO latestType (id, latest_type) values (?, ?)',(1,'zhilian'))
			cursor.close()
			db.commit()
			return db

