.. cosmocalc documentation master file, created by sphinx-quickstart on Wed Jan 28 16:02:47 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`cosmocalc`
======================

.. automodule:: cosmocalc

Examples
---------
From the unix command line::

 % cosmocalc.py --help                        # Print help
 % cosmocalc.py 2.5                           # All values for z=2.5
 % cosmocalc.py 10 --H0=50 --WM=0.2 --WV=0.5  # Arbitrary cosmology
 % cosmocalc.py --H0 75 1.25 DA_cm DL_cm      # Ang. size and lum. distance

Within Python::

 % python
 >>> from cosmocalc import cosmocalc

 >>> ccvals = cosmocalc(3.2, H0=71)
 >>> print ccvals['DL_cm'], ccvals['age_Gyr']
 8.62139764564e+28 13.6653103344

 >>> redshifts = [0.5, 1.0, 1.5]
 >>> angdists = [cosmocalc(z)['DA_Mpc'] for z in redshifts]
 >>> print angdists
 [1254.4772859453024, 1658.5477822022472, 1761.3880061524251]

Download and Installation
---------------------------
The full :mod:`cosmocalc` package is available in the `downloads`_ directory as
``cosmocalc-<version>.tar.gz``.  

The first step is to untar the package tarball and change into the source
directory::

  tar zxvf cosmocalc-<version>.tar.gz
  cd cosmocalc-<version>

There are three methods for installing.  Choose ONE of the three.

**Simple:**

The very simplest installation strategy is to just leave the module files in
the source directory and set the ``PYTHONPATH`` environment variable to point
to the source directory::

  setenv PYTHONPATH $PWD

This method is fine in the short term but you always have to make sure
``PYTHONPATH`` is set appropriately (perhaps in your ~/.cshrc file).  And if you
start doing much with Python you will have ``PYTHONPATH`` conflicts and things
will get messy.

**Better:**

If you cannot write into the system python library directory then do the following.  These
commands create a python library in your home directory and installs the
``cosmocalc`` module there.  You could of course choose another directory
instead of ``$HOME`` as the root of your python library.
::

  mkdir -p $HOME/lib/python
  python setup.py install --home=$HOME
  setenv PYTHONPATH $HOME/lib/python

Although you still have to set ``PYTHONPATH`` this method allows you to install
other Python packages to the same library path.  In this way you can make a
local repository of packages.

**Best:**

If you have write access to the system python library directory you can just 
install there::

  python setup.py install

This puts the new module straight in to the python library so it will always be available.
You do NOT need to set ``PYTHONPATH``.

.. _`downloads`: downloads/
.. _`cosmocalc.py`: downloads/cosmocalc.py

Functions
----------

.. autofunction:: cosmocalc

.. autofunction:: get_options

