

6-26-24
Declan Borcich

Temporary Link:
https://clownfish-app-8om3z.ondigitalocean.app/dob-soda2

TO run:

0. Pull repo, make sure you have a python env running at the
root folder ("backend").
1. Install dependencies with, (or download one by one):
pip install -r requirements.txt
2. Run with (in backend folder):
gunicorn --workers=2 app:app
