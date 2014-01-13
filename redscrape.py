# -*-coding: utf-8 -*-
""" RedScrape
	Greg McClellan
	9/9/2013

	Program asks for a subreddit, then goes to the front page
	of said subreddit and scrapes for links. Generates a list 
	of class RedditPost, then prints to a a file within reddit/links.
"""



import os, sys
from bs4 import BeautifulSoup
import requests

import settings

## prepare paths
dirpath = settings.dirpath
dirpath = '/'.join(dirpath.split('/')[:-1])


class RedditPost(object):
	"""Contains info about each reddit post"""
	def __init__(self, headline, link):
		self.headline = headline
		self.link = link

	def __repr__(self):
		return self.headline + "||" + self.link

	def __str__(self):
		return self.headline + "||" + self.link


def open_subreddit(subreddit):
	"""Generates a BeautifulSoup instance of a given subreddit"""
	url = "http://www.reddit.com/r/" + subreddit

	req = requests.get(url)
	query_check = req.url.split('/')
	query_check = query_check[-1].split('?')

	if len(query_check) > 1:
		print "%s subreddit is NSFW"%subreddit
		req = requests.post(req.url, data={'over18': 'yes'})

	#import pdb; pdb.set_trace()
	if req.status_code == 404:
		return False
	data = req.text
	return BeautifulSoup(data)


def get_links(soup):
	"""Crawls the subreddit and returns all links to images, etc."""
	posts = []
	for link in soup.find_all(class_='title'):
		if not link.get('href') == None:
			posts.append(RedditPost(link.text, link.get('href')))

	return posts


def format_links(posts):
	"""Changes each link to a format more useful"""

	for index, post in enumerate(posts):
		link_split = post.link.split('/')

		# Change imgur page links to imgur image links
		try:
			if link_split[2] == 'imgur.com':
				if link_split[3] != 'a':
					link_split[2] = 'i.' + link_split[2]
					link_split[3] = link_split[3] + '.jpg'
					posts[index].link = '/'.join(link_split)
		except IndexError as e:
			print '\n\n\nIndex Error: %s\n\n\n' %post.link

		# Format links to reddit comment threads
		if link_split[0] == '' and link_split[1] == 'r':
			posts[index].link = "http://www.reddit.com" + '/'.join(link_split)


	return posts


def print_links(posts, subreddit):
	"""Prints out all links found"""

	link_path = os.path.join(dirpath, "links", "%s.txt" % subreddit)
	old_link_path = os.path.join(dirpath, "links", "old_%s.txt" % subreddit)
	with open(link_path, 'a') as link_file, \
		open(old_link_path, 'a+') as old_link_file:
		old_links = []
		for line in old_link_file:
			old_links.append(line.rstrip())
		
		link_file.write('START\n')
		for post in posts:
			print post.headline
			print "    ", post.link
			
			#import pdb; pdb.set_trace()

			if (post.link) not in old_links:
				print "Adding to file for download..."
				try:
					link_file.write(str(post) + '\n')
					old_link_file.write(post.link + '\n')
				except UnicodeEncodeError as e:
				 	print "UnicodeEncodeError on ", post.headline
				 	import unicodedata
				 	post.headline = unicodedata.normalize('NFKD', post.headline).encode("ASCII", 'ignore')
				 	link_file.write(str(post) + '\n')
					old_link_file.write(post.link + '\n')

def main(subreddit=''):
	"""Scrapes a subreddit to generate a RedditPost class for submission,
	then prints each one and saves it to two files, one representing data
	waiting to be downloaded, the other used to check against downloading copies
	"""

	# If no input given, prompt user for one
	if not subreddit:
		subreddit = raw_input("Enter a subreddit to scrape: ")
		
	# Generate BeautifulSoup instance
	soup = open_subreddit(subreddit)		

	# If page has a 404 error
	if not soup:
		print("%s subreddit does not exist") %subreddit
	# Otherwise print links and write them to files
	else:
		posts = get_links(soup)
		posts = format_links(posts)
		print '\n- - - - - - - - - - - - - - -\n'
		print_links(posts, subreddit)


if __name__ == "__main__":
	main()
