from requests.compat import quote_plus
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request

BASE_URL = 'http://books.toscrape.com/catalogue/'
PAGE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'
ORIGIN_URL = 'http://books.toscrape.com/'

def all_book():
	list_out = []

	#Get every pages to scrape
	for i in range(1,50):
		final_url = PAGE_URL.format(quote_plus(str(i)))
		response = requests.get(final_url)
		data = response.text
		soup = BeautifulSoup(data, features='html.parser')
		post_listing = soup.find_all('article',{'class': 'product_pod'})

	#Get every link for every book to scrape
		for post in post_listing :
			post_link = BASE_URL + post.find('a').get('href')
			response_intra = requests.get(post_link)
			data_intra = response_intra.text
			soup_intra = BeautifulSoup(data_intra, features='html.parser')

			#Get every infos that we want
			title = soup_intra.find('h1')
			tds = soup_intra.find_all('td')
			upc = tds[0]
			product_description = soup_intra.find("meta", {'name' : "description"})["content"]
			product_description = product_description.replace("\n", "")
			category = soup_intra.find_all('li')[2].text.replace("\n", "")
			review_rating = soup_intra.find('p', class_="star-rating")
			review_rating = review_rating['class'][1]+" / Five"
			image_url = ORIGIN_URL + soup_intra.find('img')['src'].replace("../../", "")

			#Put everything into a list of dictionnary
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

	#Transform list of dict into pandas Dataframe to export into .csv easily
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

	for url in list_url[1:]:
		list_category = []
		cat = ""
		url_intra = ORIGIN_URL+url
		data = requests.get(url_intra).text
		
		soup_intra = BeautifulSoup(data, features='html.parser')
		post_listing = soup_intra.find_all('article',{'class': 'product_pod'})
		
		post_next = soup_intra.find('li',{'class':'next'})
		
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
	
def only_images():
	for i in range(1,50):
		final_url = PAGE_URL.format(quote_plus(str(i)))
		response = requests.get(final_url)
		data = response.text
		soup = BeautifulSoup(data, features='html.parser')
		post_listing = soup.find_all('article',{'class': 'product_pod'})

	#Get every link for every book to scrape
		for post in post_listing :
			post_link = BASE_URL + post.find('a').get('href')
			response_intra = requests.get(post_link)
			data_intra = response_intra.text
			soup_intra = BeautifulSoup(data_intra, features='html.parser')

			tds = soup_intra.find_all('td')
			upc = tds[0]
			image_url = ORIGIN_URL + soup_intra.find('img')['src'].replace("../../", "")
			urllib.request.urlretrieve(str(image_url), str(upc.text)+'.jpg')


def main():
    print('Hey we are going to download all the books by categorie in different .csv file for each categorie')
    by_categorie()
    print('Ok we finished the first download, now we\'re going to download the images')
    only_images()
    print('We finished all the downloads, you can find images and .csv into the current directory')

if __name__ == "__main__":
    main()


"""		
for url in list_url:
	response2 = requests.get(ORIGIN_URL+url)
	print(response2.text)
"""