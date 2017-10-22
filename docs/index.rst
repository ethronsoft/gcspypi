.. GCSPyPI documentation master file, created by
   sphinx-quickstart on Sun Apr 09 17:23:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GCSPyPI
========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

[G]oogle [C]loud [S]torage PyPI, is a private PyPI repository backed
by Google Cloud Storage. 

Features
========

- Easily control who has access the repository from Google Cloud Console ACL dashboard
- Upload packages built with setuptools to the repository
- Remove packages from the repository
- Search for packages in the repository using syntax similar to pip search
- Install and uninstall packages


Install
=======

.. note::
        At the time of writing (June 2017), the google python dependencies
        gcspypi uses are working only on python2.7. 
        If you are a python3 user, install gcspypi in a virtualenv built on
        python2.7 and use it whenever interfacing with gcspypi.

Install with pip
----------------

::

    pip install gcspypi

Install from source
-------------------

Grab a copy of the code from github::

    git clone https://github.com/ethronsoft/gcspypi.git

Change directory inside the cloned repository::

    cd gcspypi-master

Install the package::

    python setup.py install

Getting Started
===============

Setting up Google Storage
-------------------------

GCSPyPI uses the Google cloud infrastructure to provide a 
secure, redundant easy to control storage space to host your packages.

Cool you say. It means you need to have a Google cloud account for yourself
or your organization. 

There usually is a trial period that let's you open an account for free for a certain period, check out:
    
	https://cloud.google.com/getting-started

Once you have your account, you need to create a Project, such as "Super PyPI Repository" and a bucket. Instructions at:

    https://cloud.google.com/storage/docs/quickstart-console

The bucket name is important, as it identifies your repository. So a bucket named `my-org-pypi` will give you a repository `my-org-pypi`. You will use this name to interact with the repository from the gcspypi client, as we will see later.

Managing access to the repository
---------------------------------

You get to levarage the authentication mechanisms put in place by Google. This is really the sweetspot: 

- No Auth server to manage 
- No SSL certificates to buy to encrypt communication from pip to your private server
- Simple ACL system

You can either set permissions on the whole project from the IAM dashboard (OK if the project only contains the google cloud storage resource) or give more fined grained control on the bucket itself. Read more about this here:

    https://cloud.google.com/storage/docs/access-control/lists

and here:

    https://cloud.google.com/iam/docs/granting-changing-revoking-access

**TL;DR**
If you created the project, you are the owner. You have full create/modify/delete control over the bucket. This is enough to get you started.

Authenticating
--------------

GCSPyPI uses the `Application Default Credentials` to authenticate and grant access to the repository. Setting them is very easy.

Install Google Cloud SDK:

    https://cloud.google.com/sdk

Initialize the SDK and follow the instructions::

    gcloud init

.. note::

	This will allow you to set your "default" configuration, as well as switch between differnet configurations for the various projects you have. You can also use `gcloud config` for this. Check out the following link for more info:
	
	    https://cloud.google.com/sdk/gcloud/reference/config
	
Login in your "default" config::

    gcloud auth application-default login

Done.
You don't have to do this everytime, the settings will be stored in your local machine. 

How to use GCSPyPI
==================

Whenenver you are stuck, use this command in your terminal::

    gcspypi --help

It will show you general guidance as well as providing you with the list of supported commands and accepted parameters. Then use the `--help` on each subcommand for further help.

Since you are here though, we'll summarize it for you. Such gallantry!

Define the repository
---------------------

In any command that produces an interaction with the repository, you will have to specify the repository name. 

You can either do so in the command itself::

    gcspypi --repository my-org-pypi

Or create a file `.gcspypirc` in your home and write the following::

    repository: my-org-pypi


Upload a package
----------------

Write a `setup.py` for your project using the `setuptools` package as you usually do.

Generate a source distribution::

    python setup.py sdist

Or a WHEEL distribution::

    python setup.py bdist_wheel

The resulted file should be placed in a `dist/` folder.

Upload the package::

    gcspypi --repository my-org-pypi upload dist/name_of_distribution

.. note::

    If you wish to upload a package with a version that already
    exists in the repository, you will have to use the `--overwrite` (`-o`)
    parameter. This will require the issuer to have delete permission on the 
    bucket.

 
Delete packages
---------------

Let's assume we have a package "test_package" distributed with version 1.0.0 and 1.0.1.
We can delete it from the repository as follows::

    gcspypi --repository my-org-pypi test_package

.. note::

    This requires the issuer to have delete permission on the bucket

Install packages
----------------

To install package "test_package" with version "1.0.0"::

    gcspypi --repository my-org-pypi install test_package==1.0.0

To install the latest package, omit the version::

    gcspypi --repository my-org-pypi install test_package

To install dependencies from a requirements.txt file::

    gcspypi --repository my-org-pypi install -r /path/to/requirements.txt

.. note:: 

    You can also use ranged versions, such as `>1.0.0,<2.0.0` to install the first version greater than 1.0.0 but smaller than 2.0.0. 

    To see all the possible way to refer to a package, issue command::

        gcspypi syntax

.. note::

    By default, `install` will first try to resolve a package by looking it up
    in the repository. If no match is found, it proceeds looking in the default
    location your `pip install` would look into. If you want to prevent this, use the `--no-mirror` argument 

    By default, `install` will give precedence to SOURCE packages. If you want to give priority to WHEEL packages, use the `--type WHEEL` argument

.. note::
    
    When defining the dependencies for your package, either in `setup.py` or `requirements.txt`, you can freely mix your private packages hosted in a GCSPyPI repository with public ones.
    GCSPyPI will take care of resolving which one is which, recursively installing all dependencies with names and versions matching those available in the repository and then trying to install the remaining ones from the public site used by the default `pip install`.

.. note::

    You are free to activate a `virtualenv` to control where these packages are getting installed

.. note::

    Installation dependencies are first resolved against your gcspypi repository. If a match is not found and mirroring is enabled, the public pypi repository, as defined by your environement, is then queried via pip. 

Uninstall packages
------------------

For convenience, an `uninstall` command is provided. It effectively calls `pip uninstall`. This is done so that you don't have to switch between `pip` and `gcspypi` commands::

    gcspypi --repository my-org-pypi uninstall test_package

List packages
-------------

To list all available packages in the `my-org-pypi` repository::

    gcspypi --repository my-org-pypi list

To list all available packages for a package with a name including "`test_`"

    gcspypi --repository my-org-pypi list `test_`

To enable a tree view, use the `--pretty` parameter

Search packages
---------------

To search for the existence of version "1.0.0" for package "test_package"::

    gcspypi --repository my-org-pypi search test_package==1.0.0

To search for the first version greater than "2.0.0"::

    gcspypi --repository my-org-pypi search test_package>2.0.0

Or simply::

    gcspypi --repository my-org-pypi search test_package>2

To view more examples of how to refer to a package version, use::

    gcspypi syntax

Backup a repository
---------------

To get a full copy of the `my-org-pypi` repository localy, for backup, migration or other purpose, do::

    gcspypi --repository my-org-pypi pull /path/where/to/download

You will get a zipped file containing your repository

Restore a repository
---------------

To push a local .zip copy of the `my-org-pypi`, previously obtained with `pull`, onto a new repository `my-new-org-pypi`::

    gcspypi --repository my-new-org-pypi push /path/to/zipped/repo/*.zip

FAQ
==========

* I am getting error **OSError: Project was not passed and coud not be determined from the environment"**.
  
  When you used `gcloud init`, you have setup a default configuration and selected an active project. This error is about gcloud not being able to infer that project from the environment "variable" that you have made available with `gcloud auth application-default login`. We have noticed this error when running gcspypi in a Python 3.6 virtual environment. 
  
  **Solution**: set process environment variable `GCLOUD_PROJECT` to the desired project id. You can look up your project id in your google cloud dashboard. 
  


* I am getting error **Cannot perform a '--user' install. User site-packages are not visible in this virtualenv**.

  **Solution**: install with option '--no-user'

Contribute
==========

If you find something that doesn't work or want to propose changes, make use of the `issues` space

https://github.com/ethronsoft/gcspypi/issues

to let us know what's broken. 

You may also issue a pull request on your branch with your proposed solution. Include tests proving the fix and notes describing what has been done. We use the `unittest` framework.

Conclusion
==========

That's it folks. We hope you'll enjoy using GCSPyPI.



..
	Indices and tables
	==================
	
	* :ref:`genindex`
	* :ref:`modindex`
	* :ref:`search`
