import urllib.request as request
import urllib.error as error
from html.parser import HTMLParser

FILE_NAME = './crawl.txt'
url = 'https://github.com'

class Parser(HTMLParser):
	def __init__(self, output=None):
		HTMLParser.__init__(self)
		if output is None:
			self.output = []
		else:
			self.output = output
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			self.output.append(dict(attrs).get('href'))

def read_web(l):
	try:
		fp = request.urlopen(l)
		ret = fp.read().decode('utf8')
		fp.close()
		return ret
	except KeyboardInterrupt:
		return 1
	except:
		return 2

def relative2abs(l):
	li = []
	for i in l:
		if i is None:
			pass
		elif i=='':
			pass
		elif i[0]=='#':
			pass
		elif i[0]=='/' or i[0]=='?' or i[0]=='@':
			li.append(url+i)
		else:
			li.append(i)
	return li

P = Parser()
crawl_res = [url]

def crawl(u):
	try:
		try:
			site = read_web(u)
			if site==2:
				return 0
			elif site==1:
				return 1
		except error.HTTPError:
			return 0
		try:
			P.feed(site)
		except:
			return 0
		links = relative2abs(P.output)
		if links==[]:
			pass
		else:
			for s in links:
				if s==u or s in crawl_res:
					pass
				else:
					print('\33[32mFound@'+str(len(crawl_res))+': \33[37m'+s)
					crawl_res.append(s)
	except KeyboardInterrupt:
		return 1

while True:
	for w in crawl_res:
		res = crawl(w)
		if res==1:
			break
	if res==1:
		break

file = open(FILE_NAME, 'w')
for c in crawl_res:
	file.write(c+'\n')
file.close()