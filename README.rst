=======================
Template django project
=======================

Requirements
============

* Python 2.7
* virtualenv
* libxml2 with development headers;
* lixslt with development headers;
* Python development headers;
* libsqlite3 with development headers;
* libjpeg with development headers;

Creating project from template
==============================

Run::

   django-admin.py startproject --template=https://github.com/imposeren/another-django-template/zipball/master NEW_PROJECT_NAME

Deploy for developers
=====================

Short deployment::

   cp fabsettings_default.py fabsettings.py
   fab init_env init_project

If you do not have fabric::

   virtualenv .env
   source .env/bin/activate
   pip install -r requirements.txt
   cp fabsettings_default.py fabsettings.py
   fab init_project


Turn project to template
========================

You can create project from this template, modify and turn it back to template!
To do this you can run fabric command ``generate_template``::

   fab generate_template
