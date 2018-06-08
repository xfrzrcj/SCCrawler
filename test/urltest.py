import urllib.request
from bs4 import BeautifulSoup

url = "http://www.shjcw.gov.cn/2015jjw/n2233/index.html"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]
res_data = opener.open(urllib.request.Request(url))
# res_data = urllib.request.urlopen(url)
res = res_data.read()
soup = BeautifulSoup(res, "lxml")
print(soup)
