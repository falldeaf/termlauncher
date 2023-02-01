# TermLauncher
This is an early version of a command-line based key launcher using Textual. I'm using it together with the quake mode in Windows Terminal to quickly access it and close it.

![](./keylaunch-test.gif)

## Why another key launcher?
I really love the ability to hit a hot-key and quickly access local applications, web-based API's and more. The problem for me was, it was overly difficult to write plugins. I wanted to be able to think of a quick use-case and have something working right away. This application uses command-line applications as input and output. So plugins for this application are short entries in a settings.json file that access a seperate command-line application that can output an array in JSON. Or even just a simple entry in the settings.json alone can create an entire plugin!

## Install and start
To install, use pip;
```
pip install termlauncher
```

And to start the launcher
```
py -m termlauncher
```

## Settings
Your settings.json file is stored in your local appdata folder

An example file:
```
{
	"terminal": "windowsterminal",
	"darktheme": true,
	"pluginfolder": "plugins/",
	"plugins": []
}
```

## Plugins
Plugins are entries in settings.json under the plugins array. And are accessed through termlauncher with keywords. A command will look like:
```
kw This is a query
```
Where 'kw' is a keyword that activates a plugin, and 'This is a query' is a query string that gets passed to a plugin.

Below is an example with two plugin entries. The first will call out to a python commandline application, that returns a json array with applications matching a search. termlauncher will replace {query} with any and all words after the keyword
```
{
	"plugins": 
	[
		{
			"name": "applauncher",
			"icon": "1F4F1",
			"description": "Launch applications!",
			"keyword": "a",
			"realtime": true,
			"search": "py plugin_apps.py --search \"{query}\"",
			"type": "listing",
			"listitem": "({index}) {name}",
			"run": "py plugin_apps.py --run \"{action}\""
		},
		{
			"name": "file search",
			"icon": "1F4C1",
			"platform": "windows",
			"description": "Search for files on your computer!",
			"keyword": "f",
			"realtime": true,
			"search": "powershell.exe -Command \"Get-ChildItem -Path c:\\project\\* -Include {query} -Recurse -ErrorAction SilentlyContinue | Select-Object -First 10 @{Name='name';Expression={$_.Name}}, @{Name='action';Expression={'start explorer /select, \"' + $_.FullName + '\"'}}, @{Name='description';Expression={'Open the folder in explorer'}} | ConvertTo-Json -Compress\"",
			"type": "listing",
			"listitem": "({index}) {name}",
			"run": "{action}"
		}
	]
}
```

## Roadmap

There's lots of features that are critical for everday use and some nice to haves that I'd like to get to, particularly if anyone else ends up liking and using termlauncher.

- Showing Errors from misbehaving or unconfigured plugins
- Alternate 'run' options for the output (For instance, if a search program finds files and lists them, the automatic option is to open the containing folder, but an alternate option might be opening the file in a text editor)
- Faster opening, I'll probably create some pre-compiled binaries so it can open faster
- For now, a keyword must be specified to access a plugin, but allowing * as a keyword so that it can draw from multiple plugins would be good
- Return types other than 'List'. List is a list of items that allows the user to select one option from and execute the appriate action, which should work for most things. Another possible type might be a word-box that you can scroll through and select/copy from, or a table if the data that you'd be back is tabular.
- A companion hotkey app that could open termlauncher
