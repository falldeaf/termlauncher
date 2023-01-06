import os
import json
import pyperclip
import argparse
import openai
from dotenv import load_dotenv
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', help='search sites for')
parser.add_argument('--run', help='run an application')
parser.add_argument('--temp', help='How deterministic?', default=1, type=int)
parser.add_argument('--tokens', help='How many tokens, max?', default=256, type=int)
args = parser.parse_args()

prompt_precursor = """In responding to the following question, please respond in valid JSON only.
						It should be a list of key/value pairs where the key is the type of action 
						to take and the value is your response. 
						
						Here is an example for the question \"In Python, how can I add text to the clipboard?\":
						
						{"copy": "You could use the pyperclip module to copy text to the clipboard.",
						 "open": "Open the documentation for [Pyperclip](https://pyperclip.readthedocs.io/en/latest/)", 
						 "copy": "Copy the following code to the clipboard: pyperclip.copy(\"Hello World!\")",
						 "run": "Run the following code: pyperclip.copy(\"Hello World!\")",
						}"""

if args.prompt:
		openai.api_key = os.getenv("OPENAI_KEY")
		response = openai.Completion.create(model="text-davinci-003", prompt=prompt_precursor + args.prompt, temperature=args.temp, max_tokens=args.tokens)
		print(response["choices"][0]['text'])

if args.run:
	pyperclip.copy(args.run)