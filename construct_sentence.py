# -*- coding: utf-8 -*-	

import json
import requests

API_KEY = 'b5dbbf86f55404cce80010117ce00871841f84f3fadf0b17b'
WOTD_URL = 'http://api.wordnik.com/v4/words.json/wordOfTheDay?api_key='
COMPLETE_URL = '%s%s' % (WOTD_URL, API_KEY)
MAX_MESSAGE_LEN = 140

def get_word(data):
	word = data.get('word')
	return word

def get_definition(data):
	definitions = data.get('definitions')[0]
	definition = definitions.get('text')
	function = definitions.get('partOfSpeech')

	return definition, function

def get_example(examples):
	examples_text = []
	
	[examples_text.append(example.get('text')) for example in examples]

	return examples_text

def parse_json_data(json_data):
	word = get_word(json_data)
	definition, function = get_definition(json_data)
	examples = get_example(json_data.get('examples'))
	note = json_data.get('note')

	parsed_data = (
		word,
		definition,
		function,
		min(examples, key=len),
		note
	)

	return parsed_data

def construct_message(info_list):
	message = '[%s] [%s] [%s] [%s] [%s]' % (info_list)

	max = 0
	variables = 5
	while len(message) > MAX_MESSAGE_LEN:
		variables -= 1
		max -= 1
		message_format = r'[%s]' * variables
		message = message_format % info_list[:max]

	return message


def main():
	data = requests.get(COMPLETE_URL)
	json_data = json.loads(data.text)

	info_list = parse_json_data(json_data)

	message = construct_message(info_list)

	print message

if '__main__' == __name__:
	main()