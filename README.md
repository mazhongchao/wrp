# wrp

A system for work recording and planning.

## Installation
```bash
pip install -r requirements.txt
```

## Start
In Linux:
```bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser

# development or test environment
./manage.py runserver 
```

## External dependencies
* Nginx (for production environment)
* uWSGI（for production environment）
* SQLite3 or MySQL8
* google-chrome
* chromedriver

The charts generated by `pyecharts` cannot be displayed as a image in the PDF file generated by `wkhtmltopdf` from HTML, so use `snapshot_selenium` to generate a image of the charts, and then use the image in HTML file, and `snapshot_selenium` requires `google-chrome` binary files and `chromedriver`.

Install `google-chrome` and `chromedriver`:
```bash
# for AlmaLinux 9
# google-chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo dnf install google-chrome-stable_current_x86_64.rpm

# chromedriver
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
upzip chromedriver_linux64.zip
```
