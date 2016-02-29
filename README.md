# CreateDailyEverNotes
Create an empty note in the specified Evernote notebook.


With the following cron job, it can be used to ease keeping a daily journal or worklog.
```bash
# At 05:00 every workday
0 5 * * Mon-Fri python /home/user/CreateDailyEverNotes/create_daily_evernote.py
```

# TODO
- export template of the note to an external file
