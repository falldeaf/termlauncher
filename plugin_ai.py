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
						It should be an array of objects. Each object should have . 
						
						Here is an example for the question \"In Python, how can I add text to the clipboard?\":
						
						[
							{
								"name": "Open Pyperclip Documentation",
								"action": "open:https://pyperclip.readthedocs.io/en/latest/",
								"confidence": 90,
								"description": "You could use the 'pyperclip' module to copy text to the clipboard."
							},
							{
								"name": "Copy Code to Clipboard",
								"action": "copy:pyperclip.copy(\"Hello World!\")",
								"confidence": 80,
								"description": "Copy the following code to the clipboard: pyperclip.copy(\"Hello World!\")"
							}
							{
								"name": "Run Code",
								"action": "run:pyperclip.copy(\"Hello World!\")",
								"confidence": 70,
								"description": "Run the following code: pyperclip.copy(\"Hello World!\")"
							}
						]
						
						Question:"""

if args.prompt:
		openai.api_key = os.getenv("OPENAI_KEY")
		response = openai.Completion.create(model="text-davinci-003", prompt=f"{prompt_precursor} {args.prompt}", temperature=args.temp, max_tokens=args.tokens)
		print(response["choices"][0]['text'])

if args.run:
	pyperclip.copy(args.run)