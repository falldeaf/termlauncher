import json
import argparse
import windowsapps
from fuzzywuzzy import fuzz

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='search for app')
parser.add_argument('--run', help='run an application')
parser.add_argument('--num', help='how many results?', default=10, type=int)
args = parser.parse_args()

if args.search:
	installed_applications = windowsapps.get_apps()

	for key in installed_applications:
		installed_applications[key] = fuzz.ratio(key.lower(), args.search.lower())

	sorted_json = dict(sorted(installed_applications.items(), key=lambda item: item[1], reverse=True))

	#final_json = {}
	#for index, (key, value) in enumerate(sorted_json.items()):
		#print(index, key, value)
		#final_json['action'] = key
		#final_json['match'] = value
		#final_json['title'] = ke
		#if value > args.num:
			#break
	sliced_json = {key: sorted_json[key] for key in list(sorted_json.keys())[:args.num]}
	print(json.dumps(sliced_json))

if args.run:
	windowsapps.open_app(args.run)