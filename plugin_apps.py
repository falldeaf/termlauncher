import json
import argparse
import windowsapps
from fuzzywuzzy import fuzz, process

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='search for app')
parser.add_argument('--run', help='run an application')
parser.add_argument('--num', help='how many results?', default=10, type=int)
args = parser.parse_args()

if args.search:
	installed_applications = windowsapps.get_apps()

	searched_apps = []
	results = process.extract(args.search, installed_applications.keys(), limit=args.num)

	for result in results:
		obj = {}
		obj['name'] = result[0]
		obj['action'] = result[0]
		obj['confidence'] = result[1]
		obj['description'] = ""
		searched_apps.append(obj)
	
	print( json.dumps(searched_apps) )

if args.run:
	windowsapps.open_app(args.run)