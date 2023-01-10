import json

json_test = "[  {   \"name\": \"Copy Regex to Clipboard\",   \"action\": \"copy:\",   \"confidence\": 95,   \"description\": \"Copy the regular expression to the clipboard:\"  },  {   \"name\": \"Open Regex Documentation\",   \"action\": \"open:https://www.regular-expressions.info/email.html\",   \"confidence\": 80,   \"description\": \"Open the regex documentation at: https://www.regular-expressions.info/email.html\"  } ]"

print(json_test)

print(json.loads(json_test))