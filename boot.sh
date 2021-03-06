#!/bin/sh
exec gunicorn --workers=4 -b :5000 myproject:app