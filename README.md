
=============
Account application
=============

This application use REST API to work with users' accounts.

How to install
--------

* This project based on Django==1.11, Python==3.5 and Postgres==9.5 (and
database "accounts" should be created).

* Create virtual environment:

    .. code-block:: bash

        $ virtualenv env --python=python3.5
        $ mkdir accounts
        $ cd accounts

* Clone project from github:

    .. code-block:: bash

        $ git clone https://github.com/dasap89/rest_accounts.git

* Install packages from requirements.txt using pip:

    .. code-block:: bash

        $ pip install -r requirements.txt


* Run migrations:

    .. code-block:: bash

        $ python manage.py migrate

* Run application or go to "How to test":

    .. code-block:: bash

        $ python manage.py runserver

How to test
--------

* There is test.sh file for starting tests, so just call this file:

    .. code-block:: bash

        $ ./test.sh


How to use
--------

You can redefine database. In this case you need to add database
credentials in ".env" file.

There are available next endpoints:

* /api/v1/auth/register - for registrating new users, email and password are
required

    .. code-block:: bash

        $ curl -XPOST 'http://127.0.0.1:8000/api/v1/auth/register' -d '{"email":"some@email.com", "password":"1%abcdef"}' -H "Content-Type: application/json"

* /api/v1/auth/login    - for logging in with credentials; email and password
 are required; message and token are returned

    .. code-block:: bash

        $ curl -X POST 'http://127.0.0.1:8000/api/v1/auth/login' -d '{"email":"some@email.com", "password":"1%abcdef"}' -H "Content-Type: application/json"

* /api/v1/auth/info     - for getting user's info; token is required (you
can it from /api/v1/auth/login); email, is_staff, first_name, last_name are returned

    .. code-block:: bash

        $ curl -X GET 'http://127.0.0.1:8000/api/v1/auth/info' -H "Content-Type:application/json" -H "Authorization: Token 231937dc8ba21ec43c2214fa1de4dba069968cf7"

* /api/v1/auth/update   - for updating user's data; email, first_name, last_name, password are optionals; message is returned

    .. code-block:: bash

        $ curl -X PATCH 'http://127.0.0.1:8000/api/v1/auth/update' -d '{"email":"new_some@email.com", "first_name": "new_first_name", "last_name":"new_last_name", "password":"1%abcdef1111"}' -H "Content-Type:application/json" -H "Authorization: Token 231937dc8ba21ec43c2214fa1de4dba069968cf7"


* /api/v1/auth/logout   - for logging out; token is needed; message is returned

    .. code-block:: bash

        $ curl -X DELETE 'http://127.0.0.1:8000/api/v1/auth/logout' -H "Authorization: Token 231937dc8ba21ec43c2214fa1de4dba069968cf7"

