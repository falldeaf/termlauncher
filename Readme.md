# pytextual launch
This is an early version of a command-line based key launcher using Textual. Haven't come up with a name, yet.

![screen-gif](./keylaunch-test.gif)

## Why another key launcher?
It's still in rough shape and only has a couple working built-in plugins. But I really love the ability to hit a hot-key and quickly access features of applications through the many API's available. The problem for me was, it was overly difficult to write plugins. This application uses command-line applications as input and output. So plugins for this application are short entires in a settings.json file and a seperate command-line application that can output an array in JSON.