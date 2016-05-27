#!/usr/bin/env python

import argparse
import sys
import os
import time
from datetime import datetime
# To get here:
# https://github.com/evernote/evernote-sdk-python
# https://github.com/evernote/evernote-sdk-python3
# > sudo python setup.py install
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

# To get here:
# https://dev.evernote.com/doc/articles/dev_tokens.php
auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
title_format_date = "%Y/%m/%d %A"


def get_args():
	parser = argparse.ArgumentParser(description='Create an Evernote note using template')
	parser.add_argument('--notebook', required=True, help='Name of the notebook where notes will be created')
	parser.add_argument('--template', required=True, type=argparse.FileType('r'), help='Template for the message to send')
	parser.add_argument('--reminder-time', required=False, help='Time to set the reminder to')
	return parser.parse_args()

def main():
	args = get_args()
	
	client = EvernoteClient(token=auth_token, sandbox=False)
	note_store = client.get_note_store()
	notebooks = note_store.listNotebooks()
	def findNotebook(notebooks, name):
		for notebook in notebooks:
			if notebook.name == name:
				return notebook
		return
	notebook_to_use = findNotebook(notebooks, args.notebook)
	if not notebook_to_use:
		print("Error. The notebook '%s' does not exists" % args.notebook)
		sys.exit(-1)
	
	print("Going to create the note in notebook '%s'" % notebook_to_use.name)
	note = Types.Note()
	# Link note to notebook
	note.notebookGuid = notebook_to_use.guid
	note.title = datetime.now().strftime(title_format_date)
	
	# Message
	print("Using %s as a template for the note" % args.template.name)
	lines = args.template.readlines()
	note.content = ''.join(lines)
	
	if(args.reminder_time):
		hour, minute = args.reminder_time.split(":")
		when = datetime.now().replace(hour=int(hour), minute=int(minute), second=00)
		note.attributes = Types.NoteAttributes()
		# To define the relative order in the reminders list
		#note.attributes.reminderOrder = 1
		# time.mktime -> gives unix timestamp in seconds (considering local tz)
		# reminderTime -> is expecting milliseconds
		note.attributes.reminderTime = time.mktime(when.timetuple()) * 1000
	
	createdNote = note_store.createNote(note)
	print("Successfully created note '%s'" % note.title)

if __name__ == "__main__":
	main()
