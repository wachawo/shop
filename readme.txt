# Store (testtask with jinja2 rendering)
# Installation
python3 -m venv venv
. venv/bin/activate
pip3 install -r shop/requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000
