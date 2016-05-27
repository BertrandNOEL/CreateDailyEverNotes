# CreateDailyEverNotes

Script to create an Evernote note based on a template. It can be used to ease keeping a daily worklog, or to create daily todo list. A reminder can be defined.


For example, use the following cron job to create an empty note on every week days, and a reminder to fill it at 09:00.

```bash
# At 05:00 every workday
0 5 * * Mon-Fri python /home/user/CreateDailyEverNotes/create_daily_evernote.py --notebook "Worklog" --template work.html --reminder-time 09:00
```

# TODO
* [x] export template of the note to an external file
* [x] ability to set reminders to notes
* [ ] ability to create weekly and monthly note
* [ ] clean previous reminders
* [ ] remove empty notes
* [ ] put code on Google App Engine or Google Apps script?
