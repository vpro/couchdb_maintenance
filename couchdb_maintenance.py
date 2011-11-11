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
    try:
        server = Server(server_url)
    except:
        logging.error("Could not connect to CouchDB at %s", server_url)
        continue
    logging.info("Connected to CouchDB server at %s", server_url)

    logging.info("Getting list of databases...")
    try:
        db_names = server.all_dbs()
    except:
        logging.error("Could not get list of databases for CouchDB at %s", server_url)
        continue
    logging.info("Databases: %s", ", ".join(db_names))

    for db_name in db_names:
        if db_name == "_users":
            continue

        logging.info("Database: %s", db_name)
        db = server.get_or_create_db(db_name)
	
        logging.info("Starting compaction for database %s...", db_name)
        try:	
            db.compact()
        except :
            logging.error("Error compacting database %s", db_name)
            
        for design_doc_name in db.all_docs(startkey="_design", endkey="_design0", wrapper=lambda row: row['id'][len('_design/'):]):
	    logging.info("Starting compaction for design document %s...", design_doc_name)
	    try:
                db.compact(dname=design_doc_name)
            except:
                logging.error("Error compacting design document %s", design_doc_name)
        
        logging.info("Starting view cleanup for database %s...", db_name)
        try:
            db.view_cleanup()
        except:
            logging.error("Error cleaning up views for database %s", db_name)
        
logging.info("All maintenance tasks started.")
sys.exit()