import json
from urllib.request import urlopen,urlretrieve
import pathlib
from appdirs import *
import argparse
from fuzzywuzzy import fuzz, process

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='plugins to search for')
parser.add_argument('--install', help='Install a plugin from a gist')
parser.add_argument('--num', help='how many results?', default=10, type=int)
args = parser.parse_args()

if args.search:
	#Plugins Gist: 00834b4eaf74d6a6bae8b670d36a0fb1
	url = "https://api.github.com/gists/00834b4eaf74d6a6bae8b670d36a0fb1"
	response = urlopen(url)
	data = json.loads(response.read())
	#print(data['files']['plugin_list.json']['raw_url'])
	response = urlopen(data['files']['plugin_list.json']['raw_url'])

	if response.getcode() == 200:
		data = json.loads(response.read().decode("utf-8"))

		data.sort(key=lambda x: fuzz.token_sort_ratio(x, args.search), reverse=True)

		#results = process.extract(args.search, data, limit=args.num)

		searched_plugins = []
		for result in data:
			obj = {}
			obj['name'] = result['name']
			obj['action'] = result['uid']
			obj['confidence'] = 0
			obj['description'] = ""
			searched_plugins.append(obj)
		
		print( json.dumps(searched_plugins) )

		#print(data)
	else:
		print("Failed to retrieve data")


if args.install:
	gist_id = args.install
	appname = "termlauncher"

	print(user_data_dir(appname, ''))
	folder = user_data_dir(appname, '')

	# Get metadata for Gist
	url = f"https://api.github.com/gists/{gist_id}"
	response = urlopen(url)
	data = json.loads(response.read())

	#create folder if not exists
	pathlib.Path(f"{folder}/plugins/{gist_id}").mkdir(parents=True, exist_ok=True)

	# Download files
	for filename, props in data["files"].items():
		url = props["raw_url"]
		print(f"{folder}/plugins/{gist_id}/{filename}")
		urlretrieve(url, f"{folder}/plugins/{gist_id}/{filename}")

	# read the first .json file
	with open(f"{folder}/plugins/{gist_id}/settings.json") as f1:
		file1 = json.load(f1)

	# get the first object from the 'plugins' array
	first_obj = file1['plugins'][0]

	# read the second .json file
	with open(f"{folder}/settings.json") as f2:
		file2 = json.load(f2)

	# add the first object to the second file's 'plugins' array
	# or overwrite if the object has the same 'uid' key
	found = False
	for plugin in file2['plugins']:
		if plugin['uid'] == first_obj['uid']:
			plugin.update(first_obj)
			found = True
			break
	if not found:
		file2['plugins'].append(first_obj)

	# write the updated second .json file
	with open(f"{folder}/settings.json", "w") as f2:
		json.dump(file2, f2)