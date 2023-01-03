import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='search for app')
parser.add_argument('--run', help='run an application')
args = parser.parse_args()

if args.search:
    print('blah')

if args.run:
    print(args.foo)