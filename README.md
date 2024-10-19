# Blog API Service:

## Installation
#### Manual
```
git clone `https://github.com/haldaniko/Starnavi-TeskTask.git`
cd Starnavi-TeskTask

# on macOS
python3 -m venv venv
source venv/bin/activate

# on Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

(Copy .env.sample to .env and populate it with all required data.)

python manage.py migrate
python manage.py loaddata fixture.json
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`
