import json
import keyring
import argparse
import openai

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', help='search sites for')
parser.add_argument('--apikey', help='Set api key (only needed once)')
parser.add_argument('--temp', help='How deterministic?', default=1, type=int)
parser.add_argument('--tokens', help='How many tokens, max?', default=256, type=int)
args = parser.parse_args()

prompt_precursor = """In responding to the following question, please respond in valid JSON only, with no white-space, or newline characters.
						It should be an array of objects that correspond to different possible actions to take based on the question.
						Each object should have a name, action, confidence, and description.
						Actions can be any valid command or powershell functions.

						Here is an example for the question \"In Python, how can I add text to the clipboard?\" (except it should all be on one line):

						[
							{
								"name": "Open Pyperclip Documentation",
								"action": "Start-Process \"https://pyperclip.readthedocs.io/en/latest/\"",
								"confidence": 90,
								"description": "Open the 'pyperclip' documenation at: https://pyperclip.readthedocs.io/en/latest/"
							},
							{
								"name": "Copy Code to Clipboard",
								"action": "Set-Clipboard -Value \"pyperclip.copy('Hello World!')\"",
								"confidence": 80,
								"description": "Copy the following code to the clipboard: pyperclip.copy(\"Hello World!\")"
							}
						]

						Question:"""

if args.apikey:
	keyring.set_password("system", "OPENAI_KEY", args.apikey)

if args.prompt:
	if keyring.get_password("system", "OPENAI_KEY") == None:
		print("Need to set openai key (python plugin_ai.py --openaikey <key>)")
		exit(1)

	openai.api_key = keyring.get_password("system", "OPENAI_KEY")

	clean_prompt = args.prompt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
	#response = openai.Completion.create(model="text-davinci-003", prompt=f"{prompt_precursor} {args.prompt}", temperature=args.temp, max_tokens=args.tokens)
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": f"{prompt_precursor} {args.prompt}"},
			]
	)
	print( response["choices"][0]["message"]["content"] )
	#print( response["choices"][0]['text'] )