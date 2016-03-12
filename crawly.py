import requests, sys
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import time

class Crawl(object):
	def __init__(self,url,depth):
		self.output_url = {}
		self.iter_link = {}
		self.iter_link.update(url)
		self.depth = depth
	def crawl_fn(self,url,depth):
		keys = url.keys()
		for lnk in keys:
			response = requests.get(lnk,timeout=10)
			if response.status_code == 200:
				soup = BeautifulSoup(response.text,"html5lib")
				for weblink in soup.find_all('a'):	
					try:
						link = str(weblink.get('href'))
					except:
						continue
					if link.startswith('http') or link.startswith('https'): 
						if self.search(self.output_url,link) and self.search(self.iter_link,link):								
							self.iter_link[link] = self.depth
		self.output_url.update(self.iter_link)

	def rec_fn(self,url,depth):
		if (depth > 0):	
			self.rec_fn(self.iter_link,depth - 1)
			self.crawl_fn(self.iter_link,depth)			
			 
	def search(self,url,link):
		for each in url:
			if link.split('/')[2].split('.')[-2] in each: #each.split('/')[2].split('.')[-2]:
				return False
		return True

if __name__ == '__main__':
	ts = time.time()
	inp_lnk = str((sys.argv)[1])
	depth = int((sys.argv)[2])	
	# inp_lnk = 'http://cseweb.ucsd.edu/~ppevzner/research.html'
	# inp_lnk = 'http://gosong.net.goson.xyz/Kannada_bajane_.html'
	url = {inp_lnk: 1}
	ins = Crawl(url,depth)
	ins.rec_fn(url,depth)
	print ins.output_url
	print ins.output_url.__len__()
	te = time.time()
	# print "time taken: " + str(te-ts)
