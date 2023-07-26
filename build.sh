# Install dependencies
pip install -r requirements.txt

# static build
python manage.py collectstatic --no-input

# database migration
python manage.py migrate