#response = requests.get('https://gist.github.com/1089951.git')
import json
from urllib.request import urlopen,urlretrieve

gist_id = "2c987a05d4bd3d2027477ffe81fcb92f"
folder = ".\\"

# Get metadata for Gist
url = f"https://api.github.com/gists/{gist_id}"
response = urlopen(url)
data = json.loads(response.read())

# Download files
for filename, props in data["files"].items():
	url = props["raw_url"]
	urlretrieve(url, f"{folder}/{filename}")