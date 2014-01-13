""" ReddBot
	Greg McClellan
	9/10/2013

	Umbrella for various reddit scraping and image downloading
	bots
"""
import redscrape
import redsaver
import settings
print settings.dirpath


def main():
	for subreddit in settings.subreddits:
		redscrape.main(subreddit)
		redsaver.main(subreddit)


if __name__ == "__main__":
	main()