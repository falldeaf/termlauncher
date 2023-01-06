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

	searched_apps = {}
	results = process.extract(args.search, installed_applications.keys(), limit=args.num)
	for result in results:
		searched_apps[result[0]] = str(installed_applications[result[0]])
	
	print( json.dumps(searched_apps) )

	#for key in installed_applications:
	#	installed_applications[key] = fuzz.ratio(key.lower(), args.search.lower())

	#sorted_json = dict(sorted(installed_applications.items(), key=lambda item: item[1], reverse=True))

	#sliced_json = {key: sorted_json[key] for key in list(sorted_json.keys())[:args.num]}
	#print(json.dumps(sliced_json))

if args.run:
	windowsapps.open_app(args.run)