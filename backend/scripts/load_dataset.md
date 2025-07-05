# Steps to load the dataset

1. Activate the virtual python env.
2. Run `python manage.py makemigrations` in the terminal to generate relevant migration files.
3. Run `python manage.py migrate` to apply the migrations into the database.
4. Run `python manage.py load_json_file` to load the raw data into relevant tables.

