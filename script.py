from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = 'http://books.toscrape.com/catalogue/'
PAGE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
ORIGIN_URL = 'http://books.toscrape.com/'


list_out = []
for i in range(1,50):
	final_url = PAGE_URL.format(quote_plus(str(i)))
	#final_url = PAGE_URL
	response = requests.get(final_url)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')
	post_listing = soup.find_all('article',{'class': 'product_pod'})

	for post in post_listing :
		post_link = BASE_URL + post.find('a').get('href')
		response_intra = requests.get(post_link)
		data_intra = response_intra.text
		soup_intra = BeautifulSoup(data_intra, features='html.parser')
		title = soup_intra.find('h1')
		tds = soup_intra.find_all('td')
		upc = tds[0]
		product_description = soup_intra.find("meta", {'name' : "description"})["content"]
		product_description = product_description.replace("\n", "")
		category = soup_intra.find_all('li')[2].text.replace("\n", "")
		review_rating = soup_intra.find('p', class_="star-rating")
		review_rating = review_rating['class'][1]+" / Five"
		image_url = ORIGIN_URL + soup_intra.find('img')['src'].replace("../../", "")
		#print(repr(soup_intra.find('td')))
		#print(info)
		#print(tds[3])
		#print(product_description["content"].encode('unicode-escape').decode('utf-8'))
		dic_out = {
			'product_page_url' : post_link,
			'upc' : upc.text,
			'title' : title.text,
			'price_including_tax' : tds[3].text.replace('Â', ''),
			'price_excluding_tax' : tds[2].text.replace('Â', ''),
			'number_available' : tds[5].text,
			'product_description' : product_description,
			'category' : category,
			'review_rating' : review_rating,
			'image_url' : image_url,
		}
		list_out.append(dic_out)
df = pd.DataFrame(list_out)
df.to_csv('out.csv',index=False)