""" AlbumScrape
	Greg McClellan
	9/9/2013

	Program is given a link to an imgur album, takes each
	image link and downloads image.
"""
import os, sys
from bs4 import BeautifulSoup
import requests
import urllib
from datetime import datetime

import settings

dirpath = settings.dirpath
dirpath = '/'.join(dirpath.split('/')[:-1])

def open_album(url='http://imgur.com/a/qB18d'):
	"""Opens the album and returns a BeautifulSoup instance"""
	req = requests.get(url)

	if req.status_code == 404:
		return 404
	data = req.text
	return BeautifulSoup(data)

def get_image_links(soup):
	# Following code from imgur scrolling album
	# example at http://imgur.com/a/9dJJJ
	#images = soup.find_all("div", class_="image")
	links = []
	#for image in images:
		#link = image.find("div", class_="album-view-image-link")
		#link = link.a.get('href')
		#links.append(link)

	# Figure out style at imgur.com/a/dS2mE
	images = soup.find_all("img")
	for image in images:
		link = image.get("data-src")
		if link:

			if link[-5] == 's':
				link = link[:-5] + link[-4:]

			# Prevent copies as different image format
			for already_link in links:
				#import pdb; pdb.set_trace()
				if link.split('.')[-2] == already_link.split('.')[-2]:
					link = None
					break
			if link:
				links.append(link)

	return links


def image_saver(links, subreddit="all", headline=None):
	"""Creates a folder within 'subreddit' folder and stores images within"""
	date = str(datetime.now().date())
	if not headline:
		headline = str(datetime.now())
	else:
		headline = '_'.join(headline.split())
	storage_path = os.path.join(dirpath, "images/%s/%s/%s/"%(subreddit, date, headline))

	if not os.path.exists(storage_path):
		os.makedirs(storage_path)

	print "Saving %s album to... %s/%s" %(headline, subreddit, date)
	for i, link in enumerate(links):
		name = "%3d"%i
		name = '0'.join(name.split(' ')) + '-'
		name += link.split('/')[-1]
		print "  Saving... %s" %name
		urllib.urlretrieve(link, storage_path + name)


def main(url=None, subreddit=None, headline=None):
	if not url:
		url = raw_input("Enter a url: ")
		url = "http://"+url
	soup = open_album(url)
	links = get_image_links(soup)

	for link in links:
		print link
		
	image_saver(links, subreddit, headline)




if __name__ == "__main__":
	main()
