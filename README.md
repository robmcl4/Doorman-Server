# Doorman Server

A server for the Doorman project. The web site generates friendly graphs using d3.js and data from the MySQL server.

## Requirements

* `cherrypy` - a python web server framework
* `chameleon` - templating engine
* `mysql-connector-python` - Oracle's Python DBAPI connection to a MySQL server

## Configuration

The module `config.py` expects a configuration file `config.cfg` like this:

    [mysql]
    user = door
    pass = password
    host = 127.0.0.1
    port = 3306
    database = door
    ssl = False

If `ssl` is set to `True`, then the database connector expects to find certain files within /door/db/ssl/:

* `ca-cert.pem`
* `client-cert.pem`
* `client-key.pem`
