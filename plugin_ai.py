import os
import json
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

if args.prompt:
		openai.api_key = os.getenv("OPENAI_KEY")
		response = openai.Completion.create(model="text-davinci-003", prompt=args.prompt, temperature=args.temp, max_tokens=args.tokens)
		print(response["choices"][0]['text'])