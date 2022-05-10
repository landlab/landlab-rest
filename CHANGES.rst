Changelog for landlab-rest
==========================

.. towncrier release notes start

0.2.0 (2019-04-26)
------------------

New Features
````````````

- Use *flask-cors* to allow API calls from other servers. (`#8 <https://github.com/landlab/landlab-rest/issues/8>`_)


0.1.1 (2019-04-18)
------------------

Bug Fixes
`````````

- Fixed a bug in the startup script. (`#7 <https://github.com/landlab/landlab-rest/issues/7>`_)


0.1.0 (2019-04-18)
------------------

New Features
````````````

- Added the ``start-sketchbook`` command to start the service. (`#6 <https://github.com/landlab/landlab-rest/issues/6>`_)


Documentation Enhancements
``````````````````````````

- Added documentation for building and running *landlab-rest* as a service within a docker
  container. (`#1 <https://github.com/landlab/landlab-rest/issues/1>`_)


Other Changes and Additions
```````````````````````````

- Added a docker file to create an image able to run the *landlab-rest* service. (`#1 <https://github.com/landlab/landlab-rest/issues/1>`_)
- Removed Python 2 compatibility. *landlab-rest* is now Python 3 only. (`#4 <https://github.com/landlab/landlab-rest/issues/4>`_)
- Set up continuous integration on Travis.org. (`#5 <https://github.com/landlab/landlab-rest/issues/5>`_)
- Added unit tests. (`#5 <https://github.com/landlab/landlab-rest/issues/5>`_)
- Added smoke tests for the command line interface, ``start-sketchbook``. (`#7 <https://github.com/landlab/landlab-rest/issues/7>`_)


