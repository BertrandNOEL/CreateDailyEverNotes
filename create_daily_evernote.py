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
import evernote.edam.notestore.NoteStore as NoteStore

# To get here:
# https://dev.evernote.com/doc/articles/dev_tokens.php
auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
title_format_date = "%Y/%m/%d %A"


def get_args():
	if len(sys.argv) < 2:
		# argparse does not handle when no subcommand is passed
		print("error, invalid choice. Choose from 'create-note', 'clear-reminders'")
		sys.exit(-1)
	
	parser = argparse.ArgumentParser(description='Create an Evernote note using template')
	subparsers = parser.add_subparsers()
	
	parser_a = subparsers.add_parser('create-note')
	parser_a.add_argument('--notebook', required=True, help='Name of the notebook where notes are stored')
	parser_a.add_argument('--template', required=True, type=argparse.FileType('r'), help='Template for the message to send')
	parser_a.add_argument('--reminder-time', required=False, help='Time to set the reminder to')
	parser_a.set_defaults(func=create_note)
	
	parser_b = subparsers.add_parser('clear-reminders')
	parser_b.add_argument('--notebook', required=True, help='Name of the notebook where notes are stored')
	parser_b.set_defaults(func=clear_reminders)
	
	return parser.parse_args()

def init(notebook_name):
	client = EvernoteClient(token=auth_token, sandbox=False)
	note_store = client.get_note_store()
	notebooks = note_store.listNotebooks()
	def findNotebook(notebooks, name):
		for notebook in notebooks:
			if notebook.name == name:
				return notebook
		return
	notebook_to_use = findNotebook(notebooks, notebook_name)
	if not notebook_to_use:
		print("Error. The notebook '%s' does not exists" % notebook_name)
		sys.exit(-1)
	
	return note_store, notebook_to_use

def create_note(args):
	note_store, notebook_to_use = init(args.notebook)
	template = args.template
	reminder_time = args.reminder_time
	
	print("Going to create the note in notebook '%s'" % notebook_to_use.name)
	note = Types.Note()
	# Link note to notebook
	note.notebookGuid = notebook_to_use.guid
	note.title = datetime.now().strftime(title_format_date)
	
	# Message
	print("Using %s as a template for the note" % template.name)
	lines = template.readlines()
	note.content = ''.join(lines)
	
	if reminder_time:
		# TODO this way of handling an hour is very bad. 99:99 or aa:bb would work
		hour, minute = reminder_time.split(":")
		if not hour or not minute:
			print("Error, could not parse reminder_time %s. Must be of form hh:mm" % reminder_time)
			sys.exit(-1)
		when = datetime.now().replace(hour=int(hour), minute=int(minute), second=00, microsecond=000)
		note.attributes = Types.NoteAttributes()
		# To define the relative order in the reminders list
		#note.attributes.reminderOrder = 1
		# time.mktime -> gives unix timestamp in seconds (considering local tz)
		# reminderTime -> is expecting milliseconds
		note.attributes.reminderTime = int(time.mktime(when.timetuple()) * 1000)
	
	createdNote = note_store.createNote(note)
	print("Successfully created note '%s'" % note.title)

def clear_reminders(args):
	note_store, notebook_to_use = init(args.notebook)
	print("Clear reminders")
	
	# We first get Note metadata of Notes from the Notebook
	# through a Filter
	filter = NoteStore.NoteFilter()
	filter.notebookGuid = notebook_to_use.guid
	
	spec = NoteStore.NotesMetadataResultSpec()
	# Get the 20 most recent
	# TODO get only the ones with reminder
	result = note_store.findNotesMetadata(filter, 0, 20, spec)
	print("Going to remove reminder for %s notes" % len(result.notes))
	for noteMetadata in result.notes:
		# Now we get the Note object, without retrieving any content along...
		wholeNote = note_store.getNote(noteMetadata.guid, False, False, False, False)
		# ... and reset the reminder attributes if they were set
		if wholeNote.attributes.reminderTime or \
				wholeNote.attributes.reminderOrder or \
				wholeNote.attributes.reminderDoneTime:
			# Updating
			wholeNote.attributes.reminderTime = None
			wholeNote.attributes.reminderOrder = None
			wholeNote.attributes.reminderDoneTime = None
			note_store.updateNote(wholeNote)
	print("Done")

def main():
	args = get_args()
	args.func(args)

if __name__ == "__main__":
	main()
