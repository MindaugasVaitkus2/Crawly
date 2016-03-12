import requests
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

def crawl_fn(url,depth):
	if (depth > 1):
		crawl_fn(url,depth-1)
		query = "select link from entries where depth = '{}';".format(depth-1)    
		cur = engine.execute(query)
		for row in cur.fetchall():
			print row[0]
			rec_fn(row[0],depth)

def rec_fn(url,depth):	
		response = requests.get(url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text,"html5lib")
			for weblink in soup.find_all('a'):		
				link = weblink.get('href') 
				if 'http' in str(link):
					engine.execute("INSERT INTO entries VALUES('{}','{}')".format(link,depth))

if __name__ == '__main__':
	# url = 'http://www.onlinejournalismblog.com'
	url = 'http://cseweb.ucsd.edu/~ppevzner/research.html'
	# exec_notes - 1:12, 2:296, 3:4469
	depth = 3
	conn_str = 'sqlite:///crawl.db'
	engine = create_engine(conn_str)
	rec_fn(url,1)
	if (depth > 1):
		crawl_fn(url,depth)

