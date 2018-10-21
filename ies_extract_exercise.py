#! /usr/bin/env python3
# encoding: utf-8

# This script is taylor made for the bundles of exercises generated by
# Moodle 2.
#
# XXX TODO: next version should be aware of rewriting. Once downloaded and extracted, next time use
# cases are:
#   - student does not deliver again
#   - student does deliver for the first time
#   - student does overwrite previous delivery
#   - student does remove previous delivery (rare!)

import sys, os, re
import zipfile
import tempfile, shutil
import json
import subprocess
import logging


_MOODLE_FILE_TEMPL = "(.*?)-(.*?)-(\d+)\.zip$"
_SUBMISSION_TEMPL  = "(.*?)_(.*?)_assignsubmission_file_(.*)"
_VALID_CHARS       = "[^a-zA-Z0-9]+"
_REPLACE_CHAR      = "_"


# External file with mapping between expected students and its folders
# This map just eases folder naming
_EXTERNAL_CONFIGURATION_FILE = os.path.abspath("./ies_extract_params.json")

if os.path.isfile(_EXTERNAL_CONFIGURATION_FILE):
    with open(_EXTERNAL_CONFIGURATION_FILE) as f:
        _STUDENT_NAME_CONVERSION = json.loads(f.read())
else:
    _STUDENT_NAME_CONVERSION = dict()


# To allow finding the extractor script
current_folder = os.path.dirname(sys.argv[0])
extractor_script = "%s/recursive_extract.sh -I"%current_folder


def set_logging_config(filename="/tmp/%s.log"%os.path.basename(sys.argv[0]), level=logging.INFO):
    """ sets the filename as the destination of the logs """
    logging.basicConfig(filename=filename,level=level, format="%(asctime)s %(levelname)s: %(message)s")


def run_easy(cmd):
    """ runs a command and returns the standard output and the standard error """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    try:
        out = stdout.decode('utf8')
        err = stderr.decode('utf8')
    except UnicodeDecodeError as e:
        logging.warning("run_easy(cmd:%s): it wasn't possible to decode as UTF8 on command output"%cmd)
        out = stdout.decode("utf8", "replace")
        err = stderr.decode("utf8", "replace")
    logging.info("testutils.run_easy()")
    logging.info("\tcmd:%s"%cmd)
    logging.info("\tstdout:%s"%out)
    logging.info("\tstderr:%s"%err)
    return out, err


def extract_packages(folder):
    """ extracts any package from folder recursively.
        It works by executing recursive_extract.sh bash script """
    command = "/bin/bash -c 'cd %s; /bin/bash %s'"%(folder, extractor_script)
    run_easy(command)


def normalize_name(name):
    return re.sub(_VALID_CHARS, _REPLACE_CHAR, name)


def normalize_filename(name):
    if name.endswith(".tar.gz"):
        filename = name[:len(name)-len(".tar.gz")]
        fileext = ".tar.gz"
    else:
        filename, fileext = os.path.splitext(name)
    return "%s%s"%(normalize_name(filename), fileext), fileext


def create_exercise_folder_if_missing(course, exercise_name):
    normal_course = normalize_name(course)
    normal_exercise_name = normalize_name(exercise_name)
    path = "%s/%s"%(normal_course, normal_exercise_name)
    if os.path.isdir(path):
        logging.warning("Folder %s already exists (merged)"%path)
    else:
        os.makedirs(path)
        logging.info("# New folder %s"%path)
        logging.info( "$ mkdir %s"%path)
    return path


def process_student_delivery(srcfilename, folder, student_name, internal_code, given_filename):
    normal_filename, fileext = normalize_filename(given_filename)
    student_code = _STUDENT_NAME_CONVERSION.get(student_name, normalize_name(student_name))
    path = "%s/%s/%s"%(folder, student_code, internal_code)

    if os.path.isdir(path):
        logging.warning("Delivery for %s already extracted (no changes)"%student_code)
        return

    if os.path.isdir(srcfilename):
        logging.info("$ cp -r %s %s"%(srcfilename, path))
        shutil.copytree(srcfilename, path)
        return

    logging.info("$ mkdir %s"%path)
    os.makedirs(path)
    dstfilename = os.path.join(path, normal_filename)
    if os.path.isdir(srcfilename):
        shutil.copytree(srcfilename, dstfilename)
    else:
        shutil.copyfile(srcfilename, dstfilename)


def process_zip(folder, zipfilename):
    tmppath = tempfile.mkdtemp()
    with zipfile.ZipFile(zipfilename, "r") as f:
        f.extractall(tmppath)
    file_content = os.listdir(tmppath)
    for c in file_content:
        m = re.match(_SUBMISSION_TEMPL, c)
        if m:
            srcfilename = os.path.join(tmppath, c)
            student_name = m.group(1)
            internal_code = m.group(2)
            given_filename = m.group(3)
            process_student_delivery(srcfilename, folder, student_name, internal_code, given_filename)
        else:
            logging.info("# file %s doesn't match the submission template", c)
    shutil.rmtree(tmppath)


def main():
    logging.info("Extracting Moodle exercises from this location")
    lst = os.listdir('.')
    for f in lst:
        m = re.match(_MOODLE_FILE_TEMPL, f)
        if m:
            course=m.group(1)
            exercise_name=m.group(2)
            folder = create_exercise_folder_if_missing(course, exercise_name)
            if folder:
                process_zip(folder, f)
                extract_packages(folder)

if __name__ == "__main__":
    set_logging_config()
    main()
