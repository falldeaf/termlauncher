import json
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument('--sites', action='store_true', help='search sites for')
parser.add_argument('--run', help='run an application')
parser.add_argument('--index', help='which search item?', default=0, type=int)
args = parser.parse_args()

sites = {
	"Google": "https://www.google.com/search?q={query}",
	"DuckDuckGo": "https://duckduckgo.com/?q={query}",
	"Rotten Tomatoes": "https://www.rottentomatoes.com/search?search={query}",
	"Yahoo": "https://search.yahoo.com/search?p={query}",
	"YouTube": "https://www.youtube.com/results?search_query={query}",
	"Wikipedia": "https://en.wikipedia.org/w/index.php?search={query}",
	"Amazon": "https://www.amazon.com/s?k={query}",
	"eBay": "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={query}&_sacat=0",
	"Reddit": "https://www.reddit.com/search/?q={query}",
	"Twitter": "https://twitter.com/search?q={query}",
	"Facebook": "https://www.facebook.com/search/top/?q={query}",
	"Instagram": "https://www.instagram.com/explore/tags/{query}/",
	"GitHub": "https://github.com/search?q={query}/",
}

if args.sites:
	print(json.dumps(sites))

if args.run:
	webbrowser.open(list(sites.items())[args.index][1].format(query=args.run))