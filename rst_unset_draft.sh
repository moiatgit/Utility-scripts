#! /bin/bash

# This script removes the metadata :status: draft to the given rst files

rst_metadata.py -d --key status $*
