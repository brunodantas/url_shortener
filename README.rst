URL Shortener
=============

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: GPLv3

URL shortener made with Django.

The project requirements can be found at ``requirements.pdf``.

Features
--------

API endpoints
^^^^^^^^^^^^^

Obs: the domain name is currently set as ``0.0.0.0:8000``

Create URL::

    Path: /
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "name": "Create Url",
        "description": "Endpoint for creating short URLs.

            Parameters:
                original (str): original url
                code (str): desired url code (optional)
                expires (str): desired expiry date (ISO 8601) (optional)

            Returns:
                (str): code of the short URL
                (str): expiration date",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ]
    }

Retrieve URL::

    Path: /<short_code>
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "name": "Retrieve Url Instance",
        "description": "Endpoint for retrieving a URL from its short code.

            Parameters:
                code (str): short code

            Returns:
                (str): url redirect, if it exists",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ]
    }


Admin page
^^^^^^^^^^

The admin page is accessible at ``/adm/``

URL Storage and expiration
^^^^^^^^^^^^^^^^^^^^^^^^^^

URL storage is done with a Postgres container.

Expired URLs are removed from the database when requested via either API endpoint.



Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy url_shortener

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Dev environment deployment::

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up
