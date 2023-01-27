import json
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument('--sites', action='store_true', help='search sites for')
parser.add_argument('--run', help='run an application')
parser.add_argument('--index', help='which search item?', default=0, type=int)
args = parser.parse_args()

sites = [
	{
		"name": "Google",
		"action": "https://www.google.com/search?q={query}",
		"confidence": 0,
		"description": "Google Search Engine"
	},
	{
		"name": "DuckDuckGo",
		"action": "https://duckduckgo.com/?q={query}",
		"confidence": 0,
		"description": "Privacy Search Engine"
	},
	{
		"name": "Rotten Tomatoes",
		"action": "https://www.rottentomatoes.com/search?search={query}",
		"confidence": 0,
		"description": "Movie and TV reviews"
	},
	{
		"name": "WikiPedia",
		"action": "https://en.wikipedia.org/w/index.php?search={query}",
		"confidence": 0,
		"description": "A free online encyclopedia"
	},
	{
		"name": "GitHub",
		"action": "https://github.com/search?q={query}/",
		"confidence": 0,
		"description": "Code repository"
	},
	{
		"name": "YouTube",
		"action": "https://www.youtube.com/results?search_query={query}",
		"confidence": 0,
		"description": "Video sharing website"
	},
	{
		"name": "Amazon",
		"action": "https://www.amazon.com/s?k={query}",
		"confidence": 0,
		"description": "Online shopping website"
	},
	{
		"name": "eBay",
		"action": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={query}&_sacat=0",
		"confidence": 0,
		"description": "Auctioning website"
	},
	{
		"name": "Reddit",
		"action": "https://www.reddit.com/search/?q={query}",
		"confidence": 0,
		"description": "Social news website"
	},
	{
		"name": "Twitter",
		"action": "https://twitter.com/search?q={query}",
		"confidence": 0,
		"description": "Social media website"
	},
	{
		"name": "Facebook",
		"action": "https://www.facebook.com/search/top/?q={query}",
		"confidence": 0,
		"description": "Social media website"
	},
	{
		"name": "Instagram",
		"action": "https://www.instagram.com/explore/tags/{query}/",
		"confidence": 0,
		"description": "Social media website"
	}]

if args.sites:
	print(json.dumps(sites))

if args.run:
	webbrowser.open(sites[args.index]['action'].format(query=args.run))