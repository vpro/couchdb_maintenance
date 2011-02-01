CouchDB Maintenance
===================

This is a Python script for CouchDB maintenance.

INFORMATION
-----------

This script performs maintenance on CouchDB servers by:

* Compacting all databases
* Compacting all views for all databases
* Cleaning up all views

See http://wiki.apache.org/couchdb/Compaction for more info.

DEPENDENCIES
------------

This script depends on couchdbkit. To install or upgrade to the latest
version, run this:

  $ sudo apt-get install python-setuptools
  $ sudo easy_install -U couchdbkit

This script also requires a supported JSON module for Python. You can use
cjson (or simplejson, or probably a few others if you like):

$ sudo apt-get install python-cjson

USAGE
-----

Provide URL's to CouchDB instances as arguments to the script:

  $ ./couchdb_maintenance.py http://localhost:5984 http://example.com
