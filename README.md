### Events Exercise

What is done:

* CRUD operations over Events
* Participate in event
* Withdraw from event
* Sign-in Sign-up
* Browsable API via Swagger

What is not done:

* Frontend - unfortunately I haven't worked with JS for last 4 years and need more time to check new frontend framworks. Will try to commit frontend later. 

#### Project structure

`/api` Rest Framework's stuff

`/apps` Django apps with models and services

`/tests` unit tests and API tests
 
 
#### Installation and run


Project requires python3.8

`make install` - install requirements & run migrations

`make test` - run tests

`python manage.py runserver`

#### Installation and run via Docker

`docker-compose up`

`make test-docker`

Browsable API is available by http:/127.0.0.1:8000

First need to create user using sign_up endpoint.
Just click in /auth/sign_up/ block, then click on "Try it out" button in the right corner of the block, then set username (email is expected) and password and click on button "Execute".
To login click on "Authorize", fill login and password and reload page. 

