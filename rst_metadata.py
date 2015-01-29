#! /usr/bin/env python
# encoding: utf-8

# This script allows to manage Pelican metadata in rst files.
# 
# Metadata should be in the form '^:(.{-}): (.{-})$' where:
#     - the first group is the metadata name
#     - the segond group contains the value
# 
# This script allows to:
# 
#     - list all metadata in a file { "name":"value" }
# 
#     - set a pair of metadata. If already exists a name, the value
#       is replaced, otherwise the new pair is added
# 
#     - remove an existing pair. On non existing pairs, it is ignored

# XXX TODO: 
#   1. consider changing args to allow multiple pairs on a single
#      call of the program instead of one pair each time the prog is call.
#
#   2. RstFile forces save_without_metadata() instead of offering a
#      replacement method

import sys
import os
import argparse
import re

class RstFile:
    """ This class encapsulates a rst file """
    def __init__(self, path):
        self.path = path
        self.metadata_pattern = re.compile( "^:(.+?): +(.+)$")
        self.title_pattern = re.compile( "^#+$")
        self.metadata = self._get_metadata_from_file()

    def get_metadata(self):
        """ returns the metadata found in the file """
        return self.metadata

    def save_without_metadata(self):
        """ saves the file without metadata information """
        with open(self.path) as f:
            lines = [ line for line in f.readlines() if not
                    self._line_has_metadata(line) ]
        with open(self.path, 'w') as f:
            f.writelines(lines)

    def save_with_metadata(self):
        """ saves the file by adding metadata information.
            It includes the metadata information just after the title
            of the file.

            If not title is found, it generates a warning and performs
            no changes on the file.

            If there are already metadata information, it will just
            add the new one before it. When replacement is required,
            save_with_metadata() should be performed first.
        """
        with open(self.path) as f:
            lines = f.readlines()
        lines = self._add_metadata_to_lines(lines)
        if not lines:
            print >> sys.stderr, "Warning: file without title (unchanged): %s"%self.path
            return
        with open(self.path, 'w') as f:
            f.writelines(lines)

    def set_metadata(self,key, val):
        """ adds/sets the pair to the metadata """
        self.metadata[key]=val

    def del_metadata(self,key):
        """ removes key from metadata """
        del(self.metadata[key])

    def _add_metadata_to_lines(self, lines):
        """ adds metadata to lines after the title """
        l = 0
        line_for_metadata_found = False
        number_of_title_bars_found = 0

        # find postion to add the metadata
        while not line_for_metadata_found:
            if number_of_title_bars_found == 2:
                line_for_metadata_found = True
                line_for_metadata = l + 1   # +1 to save the white line
            elif self.title_pattern.match(lines[l]):
                number_of_title_bars_found += 1
            l += 1

        if not line_for_metadata_found:
            return None

        # adding metadata to line
        metadata_info = self._metadata_to_string_list()
        return lines[0:line_for_metadata] + metadata_info + lines[line_for_metadata:]

    def _metadata_to_string_list(self):
        """ composes the metadata as a list of strings """
        result = []
        for k, v in self.get_metadata().iteritems():
            result += ":%s: %s%s"%(k,v, os.linesep)
        return result

    def _get_metadata_from_file(self):
        """ actually opens the file and extracts its metadata """
        with open(self.path) as f:
            return dict([self._extract_metadata_from_line(l) for l in
                    f.readlines() if self._line_has_metadata(l)])

    def _extract_metadata_from_line(self, line):
        """ returns a pair key, val extracted from line.
            If line has no metadata, it just returns None values """
        result = None
        m = self.metadata_pattern.match(line)
        if m:
            result = (m.group(1), m.group(2))
        return result

    def _line_has_metadata(self, line):
        """ returns True if the line contains metadata """
        return self.metadata_pattern.match(line)

class Operation:
    """ This class encapsulates the operation to be performed on a
    file """
    Set, Del, List = range(3)    # all supported operations
    def __init__(self, operation, key=None, val=None):
        self.operation = operation
        self.key = key
        self.val = val
    def key_required(self):
        """ returns true if the operation requires a key name """
        return self.operation in (Operation.Set, Operation.Del)
    def val_required(self):
        """ returns true if the operation requires a val """
        return self.operation == Operation.Set
    def key_missing(self):
        """ returns true if the key is missing but required """
        return (not self.key and self.key_required())
    def val_missing(self):
        """ returns true if the val is missing but required """
        return (not self.val and self.val_required())
    def key_unrequired(self):
        """ returns true if the key is present but not required """
        return False    # currently all options accept key espec
    def val_unnecessary(self):
        """ returns true if the val is present but not required """
        return (self.val and not self.val_required())
    def is_well_formed(self):
        """ returns true if the operation has the required args and no
        more """
        return not (self.key_missing() or self.val_missing() or
                self.key_unrequired() or self.val_unnecessary())
    def __str__(self):
        return "Operation(%s, %s, %s)"%(self.operation, self.key, self.val)
    def perform(self, path):
        """ selects and performs the operation on path """
        if self.operation == Operation.Set:
            self._perform_set(path)
        elif self.operation == Operation.Del:
            self._perform_del(path)
        elif self.operation == Operation.List:
            self._perform_list(path)

    def _perform_set(self, path):
        """ sets the new pair on path """
        assert self.key
        assert self.val
        rst = RstFile(path)
        rst.set_metadata(self.key, self.val)
        rst.save_without_metadata()
        rst.save_with_metadata()
        print "%s: set %s:%s. Now: %s"%(path, self.key, self.val, rst.get_metadata())

    def _perform_del(self, path):
        """ sets the new pair on path """
        assert self.key
        rst = RstFile(path)
        if not self.key in rst.get_metadata():
            print >> sys.stderr, "Warning: key '%s' not found in file %s (ignored)"%(self.key, path)
            return
        rst.del_metadata(self.key)
        rst.save_without_metadata()
        rst.save_with_metadata()
        print "%s: removed '%s'. Now: %s"%(path, self.key, rst.get_metadata())

    def _perform_list(self, path):
        """ shows the metadata of the file """
        rst = RstFile(path)
        metadata = rst.get_metadata()
        if not self.key or self.key in metadata:
            print "%s: %s"%(path, metadata)

#
def is_rst_file(path):
    """ returns true if the path corresponds to an existing rst file """
    _, ext = os.path.splitext(path)
    if ext != ".rst":
        print >> sys.stderr, "Warning: .rst extension expected in %s (ignored)"%path
        return False
    #
    if not os.path.exists(path):
        print >> sys.stderr, "Warning: file not found: %s (ignored)"%path
        return False
    #
    return True

#
def filter_paths(paths):
    """ checks each path and returns the list of paths corresponding
    to existing rst files """
    return [p for p in paths if is_rst_file(p)]

def parse_keyval(options):
    """ parses key and val from options. In case (key or val) and
    keyval conflict, it shows a warning and the selected val """
    key = options.key
    val = options.val
    if options.keyval:
        if key or val:
            print >> sys.stderr, "Warning: conflict with key and val. Selected %s:%s"%(key, val)
        else:
            key, val = options.keyval.split(":")
    return key, val

def checkParams():
    """ checks that the arguments of the program call are as expected. 
    In case something's wrong, an error missage is issued and 
    finishes execution with an error code.
    When everything is ok, it returns the configuration information
    in a tuple: filelist, operation """

    p = argparse.ArgumentParser(description="Manages Pelican metadata information of ReStructuredText files", version="1.0")
    p.add_argument('paths', metavar='path', nargs='+', help="Source file path with .rst extension")
    p.add_argument("-a", "--add", action="store_true", help="Adds/modify a metadata value", dest="option_set")
    p.add_argument("-s", "--set", action="store_true", help="Adds/modify a metadata value", dest="option_set")
    p.add_argument("-d", "--delete", action="store_true", help="Delete an existing key", dest="option_del")
    p.add_argument("-l", "--list", action="store_true", help="List all metadata", dest="option_ls")
    p.add_argument("--key", action="store", help="Key name", dest="key")
    p.add_argument("--val", action="store", help="Value", dest="val")
    p.add_argument("-p", "--pair", action="store", help="Pair key:value", dest="keyval")
    #
    options = p.parse_args()
    #
    sourcelist = filter_paths(options.paths)
    if len(sourcelist) == 0:
        print >> sys.stderr, "Error: no files to act on"
        sys.exit(2)
    #
    if not (options.option_set ^ options.option_del ^ options.option_ls):
        print >> sys.stderr, "Error: Please, select one and just one option (set/del/list)"
        sys.exit(4)
    #

    if options.option_set:
        op = Operation.Set
    elif options.option_del:
        op = Operation.Del
    elif options.option_ls:
        op = Operation.List

    key, val = parse_keyval(options)

    operation = Operation(op, key, val)
    if not operation.is_well_formed():
        if operation.key_missing():
            print >> sys.stderr, "Error: key name required for this operation"
            sys.exit(6)
        elif operation.val_missing():
            print >> sys.stderr, "Error: value required for this operation"
            sys.exit(6)
        elif operation.key_unrequired():
            print >> sys.stderr, "Warning: key name not required for this operation (ignored)"
        elif operation.val_unnecessary():
            print >> sys.stderr, "Warning: value not required for this operation (ignored)"
    #
    return sourcelist, operation
#
def main():
    # get configuration information
    filelist, operation = checkParams()
    for entry in filelist:
        operation.perform(entry)

    return 0

#
if __name__=="__main__":
    sys.exit(main())



