Make a Plea
===========

A simple, user-friendly online service for citizens to submit pleas for summary motoring offences.

Dependencies
------------

- VirtualBox
- Vagrant
- Docker & Docker-compose 

NOTE: Vagrant or docker can be used to set up a local dev environment

Installation
------------

Clone the repository:

    git clone git@github.com:ministryofjustice/manchester_traffic_offences_pleas.git


Create your own local.py:

    cp manchester_traffic_offences/settings/local.py.example make_a_plea/settings/local.py


To run a dev environment with vagrant:

    vagrant up
    vagrant ssh
    
The vagrant bootstrap script will install everything you need to run the application server. All you need to do is override the relevant email settings in your local.py.

Once you're ssh'd in run:

    ./manage.py runserver 0.0.0.0:8000
    
to run the development web server, and browse to http://localhost:8000 to see the server.


To run a dev environment using docker:

copy `docker/sample-local-env` to `docker/local-env`

run: 

    docker-compose up

Navigate to: 

    {ip of docker machine}:8000

To get an interactive prompt (needed to run migrations), run:

    docker-compose run django /bin/bash

The front end build uses gulp, to watch changes and rebuild on change run:

    gulp watch
    
To rebuild everything run:

    gulp
