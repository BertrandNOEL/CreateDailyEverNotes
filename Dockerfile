FROM python:2

COPY evernote-sdk-python /tmp/evernote-sdk-python
WORKDIR /tmp/evernote-sdk-python/
RUN python setup.py install

COPY create_daily_evernote.py /tmp/
CMD [ "python", "/tmp/create_daily_evernote.py" ]
