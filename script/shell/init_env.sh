#!/usr/bin/env bash
# desc: sync tables, install dependencies, collect static files.
# author: Elvin Zeng
# date: 2017-5-29

cd $(cd $(dirname $0) && pwd -P)
cd ../../

./manage.py migrate
pip install -r requirements.txt
python manage.py collectstatic -c -l --no-input