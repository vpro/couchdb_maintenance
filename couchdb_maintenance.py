#!/usr/bin/env python
#
# Copyright (c) 2010-2011 Nils Breunese <N.Breunese@vpro.nl>, VPRO Digitaal.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# INFORMATION
# -----------
#
# This script performs maintenance on CouchDB servers by:
#
# * Compacting all databases
# * Compacting all views for all databases
# * Cleaning up all views
#
# See http://wiki.apache.org/couchdb/Compaction for more info.
#
# DEPENDENCIES
# ------------
#
# This script depends on couchdbkit. To install or upgrade to the latest
# version, run this:
# 
# $ sudo apt-get install python-setuptools
# $ sudo easy_install -U couchdbkit
#
# This script also requires a supported JSON module for Python. You can use
# cjson (or simplejson, or probably a few others if you like):
#
# $ sudo apt-get install python-cjson
#
# USAGE
# -----
#
# Provide URL's to CouchDB instances as arguments to the script:
#
# $ ./couchdb_maintenance.py http://localhost:5984 http://example.com

from couchdbkit import Server
import logging
import sys

### Configuration

# Change to logging.DEBUG to debug
log_level = logging.WARNING

# List of server to perform maintenance for
server_urls = sys.argv[1:]

### Program

logging.basicConfig(level=log_level)

if not server_urls:
    logging.error("Please supply one or more URL's to CouchDB instances to carry out maintenance for.")
    sys.exit(1)

for server_url in server_urls:
    server = Server(server_url)
    logging.info("Connected to CouchDB server at %s" % server_url)

    for db_name in server.all_dbs():
        logging.info("Database: %s" % db_name)
        db = server.get_or_create_db(db_name)
		
        logging.info("Compacting database...")
        db.compact()
	
        design_docs = db.all_docs(startkey="_design", endkey="_design/"+u"\u9999")
	design_doc_names = [ d["id"][8:] for d in design_docs ]
	for design_doc_name in design_doc_names:
	    logging.info("Compacting design document %s..." % design_doc_name)
	    db.compact(dname=design_doc_name)
        
        logging.info("Cleaning up views...")
        db.view_cleanup()

logging.info("All done.")
sys.exit()
