from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = 'http://books.toscrape.com/catalogue/'
PAGE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
ORIGIN_URL = 'http://books.toscrape.com/'

def all_book():
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
	print('Your csv file have been created, you can found it as out.csv in your current directory')

def by_categorie():
	list_out=[]		
	list_url = []
	response = requests.get(ORIGIN_URL)
	data = response.text
	soup = BeautifulSoup(data, features='html.parser')
	category_post = soup.find_all('ul',{'class':'nav nav-list'})
	for k in category_post[0].find_all('a') :
		list_url.append(k.get('href'))

	#print(list_url)

	for url in list_url[1:]:
		list_category = []
		cat = ""
		url_intra = ORIGIN_URL+url
		data = requests.get(url_intra).text
		#print(data.encode('utf-8'))
		soup_intra = BeautifulSoup(data, features='html.parser')
		post_listing = soup_intra.find_all('article',{'class': 'product_pod'})
		
		post_next = soup_intra.find('li',{'class':'next'})
		#print(post_listing[0])
		while post_next != None :
			url_bis = url_intra.replace('index.html',post_next.a['href'])
			data = requests.get(url_bis).text
			soup_intra = BeautifulSoup(data, features='html.parser')
			post_listing = post_listing + soup_intra.find_all('article',{'class': 'product_pod'})
			post_next = soup_intra.find('li',{'class':'next'})

		for post in post_listing : 
			ref_link = ""
			ref_link += post.find('a').get('href')
			ref_link = ref_link.replace('../../../','')
			post_link = BASE_URL + ref_link
			#print(post_link)
			response_intra = requests.get(post_link)
			#print(response_intra)
			data_intra = response_intra.text
			#print(data_intra.encode('utf-8'))
			soup_intra = BeautifulSoup(data_intra, features='html.parser')

			title = soup_intra.find('h1')
			tds = soup_intra.find_all('td')
			#print(tds)
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
			cat = category
			list_category.append(dic_out)
		df = pd.DataFrame(list_category)
		name_df = cat+'.csv'
		df.to_csv(name_df, index=False)
	

	"""
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
		print(dic_out)
		"""
	#soup_intra = BeautifulSoup(data, features='html.parser')


#def only_images():

"""
for url in list_url:
	response2 = requests.get(ORIGIN_URL+url)
	print(response2.text)
"""