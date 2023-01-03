import json
import argparse
import windowsapps
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='search for app')
parser.add_argument('--run', help='run an application')
args = parser.parse_args()

if args.search:
	installed_applications = windowsapps.get_apps()
	#print(installed_applications)
	#windowsapps.open_app('Sticky Notes')

	for key in installed_applications:
		installed_applications[key] = fuzz.ratio(key.lower(), args.search.lower())
		#print(key, ":", installed_applications[key])

	#sorted_json = dict(sorted(installed_applications.items(), key=lambda item: item[1]))
	sorted_json = dict(sorted(installed_applications.items(), key=lambda item: item[1], reverse=True))

	#for key in sorted_json:
	for index, (key, value) in enumerate(sorted_json.items()):
		#print(index, "- ", key, ":", sorted_json[key])
		if index > 10:
			sorted_json.pop(key)

	print(json.dumps(sorted_json))

if args.run:
	print(args.foo)