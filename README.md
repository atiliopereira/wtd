# wdt

WTD (what to do?) is an API designed to facilitate the creation and management of social events. This project is built using Python and Django framework.

## Requirements

Install dependencies running:
```
pip install -r requirements.txt
```

## Usage

To start using the WTD API, ensure that you have completed the installation steps. Then, run the Django server:

```
python manage.py runserver$ python manage.py grpcrunserver --dev
```

Access the API documentation by navigating to http://localhost:8000/api/schema/docs/ in your web browser.

### API Endpoints

    /admin/: Django admin panel.
    /api/schema/: API schema view.
    /api/schema/docs/: API documentation.
    /api/v1/: Endpoints for version 1 of the API.

