""" Redsaver
	Greg McClellan
	9/9/2013

	Reads files produced by Redscrape, follows the links and
	downloads files/generates savable copies of reddit comment
	threads
"""
import os, sys
from datetime import datetime
import urllib

from redscrape import RedditPost
import albumscrape
import settings

dirpath = settings.dirpath
dirpath = '/'.join(dirpath.split('/')[:-1])
unnamed_count = 0


def read_file(subreddit):
	"""Opens up the file saved by Redscrape"""
	file_path = os.path.join(dirpath, "links", "%s.txt" % subreddit)
	if os.path.isfile(file_path):
		posts = []
		with open(file_path, 'r') as f:
			lines = f.readlines()

		with open(file_path, 'w+') as f:
			check = False

			for line in lines:

				# Only want those lines that haven't been saved already
				if line[:5] == 'START':
					check = True

				else:
					f.write(line)
					if check:
						line = line.split('||')
						headline = "-".join(line[0].split('/'))
						#import pdb; pdb.set_trace()
						link  = line[1].rstrip()
						posts.append(RedditPost(headline, link))

		return posts
	else:
		print "%s subreddit data is current" %subreddit
		return False


def save_images(posts, subreddit):
	"""Saves any image or album of images to a dir"""
	global unnamed_count
	date = str(datetime.now().date())
	storage_path = os.path.join(dirpath, "images/%s/%s/"%(subreddit, date))

	if not os.path.exists(storage_path):
		os.makedirs(storage_path)

	accepted_image_types = ['jpg', 'png', 'gif']

	for post in posts:
		#Handle unnamed headline
		if not post.headline:
			post.headline = 'unnamed' + str(unnamed_count)
			unnamed_count += 1
		# Direct image links
		if post.link.split('.')[-1] in accepted_image_types:
			print "saving %s to... %s/%s" %(post.link, subreddit, date)
			urllib.urlretrieve(post.link,
				storage_path + '_'.join(post.headline.split()))

		elif post.link.split('/')[-2] == 'a':
			albumscrape.main(post.link, subreddit, post.headline)



def main(subreddit=''):
	# If no input, prompt user for a subreddit name
	if not subreddit:
		subreddit = raw_input("Enter a subreddit to download: ")
	
	# Read from file to generate RedditPost class instances
	posts = read_file(subreddit)

	# If data to download exists, print to screen and save files
	if posts:
		for post in posts:
			print post

		save_images(posts, subreddit)
	else:
		print "No Posts"


if __name__ == '__main__':
	main()