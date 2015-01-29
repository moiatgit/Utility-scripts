#! /bin/bash

# This script sets the metadata :status: draft to the given rst files

rst_metadata.py -s -p 'status:draft' $*
