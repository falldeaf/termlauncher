import os
import pathlib
from appdirs import *

def addDefaultSettings(self):
	appname = "termlauncher"
	folder = user_data_dir(appname, '')
	pathlib.Path(f"{folder}/plugins").mkdir(parents=True, exist_ok=True)

	# create default settings file
	if not os.path.exists(f"{folder}/settings.json"):
		with open(f"{folder}/settings.json", "w") as f:
			f.write('{"darktheme": true, "plugins": []}')

def addPlugin(self, gist_id: str):
	appname = "termlauncher"

	print(user_data_dir(appname, ''))

	import json
	from urllib.request import urlopen,urlretrieve

	#gist_id = "2da918563456b6dcde6592ec7d6d148d"
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

addDefaultSettings(None)
addPlugin(None, "83e239c358e87be89f178b60fe466991")