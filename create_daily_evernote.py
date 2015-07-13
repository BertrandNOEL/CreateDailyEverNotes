
from datetime import datetime
# To get here:
# https://github.com/evernote/evernote-sdk-python3
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

# To get here:
# https://dev.evernote.com/doc/articles/dev_tokens.php
auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Name of the notebook where notes will be created
notebook_name = "Journal de Rorschach"
# https://docs.python.org/3.5/library/datetime.html#strftime-strptime-behavior
title_format_date = "%Y/%m/%d %A"


client = EvernoteClient(token=auth_token, sandbox=False)
note_store = client.get_note_store()
notebooks = note_store.listNotebooks()
def findNotebook(notebooks):
    for notebook in notebooks:
        if notebook.name == notebook_name:
        return notebook
    return None
notebook_to_use = findNotebook(notebooks)
if not notebook_to_use:
    print("Error. The notebook '%s' does not exists" % notebook_name)

print("Going to create the note in notebook '%s'" % notebook_name)
note = Types.Note()
# Link note to notebook
note.notebookGuid = notebook_to_use.guid
note.title = datetime.now().strftime(title_format_date)
# Empty message
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>'
note.content += '</en-note>'

created_note = note_store.createNote(note)
print("Successfully created note '%s'" % note.title)
