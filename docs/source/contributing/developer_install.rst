.. _install:

=================
Developer Install
=================

.. important::

  The following commands will install *landlab-rest* into your current environment. Although
  not necessary, we **highly recommend** you install *landlab-rest* into its own
  :ref:`virtual environment <virtual_environments>`.


If you will be modifying code or contributing new code to *landlab-rest*, you will first
need to get *landlab-rest*'s source code and then install *landlab-rest* from that code.

Source Install
--------------

*landlab-rest* is actively being developed on GitHub, where the code is freely available.
If you would like to modify or contribute code, you can either clone our
repository

.. code-block:: bash

   $ git clone git://github.com/landlab/landlab-rest.git

or download the `tarball <https://github.com/landlab/landlab-rest/tarball/master>`_
(a zip file is available for Windows users):

.. code-block:: bash

   $ curl -OL https://github.com/landlab/landlab-rest/tarball/master

Once you have a copy of the source code, you can install it into your current
Python environment,

.. tab:: mamba

  .. code-block:: bash

     $ cd landlab-rest
     $ mamba install --file=requirements.txt
     $ pip install -e .

.. tab:: conda

  .. code-block:: bash

     $ cd landlab-rest
     $ conda install --file=requirements.txt
     $ pip install -e .

.. tab:: pip

  .. code-block:: bash

     $ cd landlab-rest
     $ pip install -e .

Developer Tools
---------------

Once you start developing with *landlab-rest*, there are a number of other packages you
may find useful to install. These packages are used for, among other things,
testing *landlab-rest*, and ensuring your code complies with *landlab-rest*'s development
standards.

.. tab:: conda

  .. code-block:: bash

    $ conda install --file requirements-dev.txt --file requirements-testing.txt

.. tab:: pip

  .. code-block:: bash

    $ pip install -e ".[dev,testing]"
