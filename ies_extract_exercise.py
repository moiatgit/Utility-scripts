#! /usr/bin/env python
# encoding: utf-8

# This script is taylor made for the bundles of exercises generated by
# Moodle 2.
# The script 
# TODO:
#   1. extract _STUDENT_NAME_CONVERSION to an external file (you won't
#   want to show them on github)
#   2. allow configuring the repository of downloaded bundles as a
#   different folder from the destination of the extracted contents
#   3. Allow for confirmation and improve warnings
#   4. some refactor would be nice! This is poor code and you now it!

import os, re
import zipfile
import tempfile, shutil

_MOODLE_FILE_TEMPL = "(.*?)-(.*?)-(\d+)\.zip"
_SUBMISSION_TEMPL  = "(.*?)_(.*?)_assignsubmission_file_(.*)"
_VALID_CHARS       = "[^a-zA-Z0-9]+"
_REPLACE_CHAR      = "_"

_STUDENT_NAME_CONVERSION = {
    "Alberto_Garc_a_Beato" : "agarcia1",
    "Andr_s_Gracia_Rodr_guez" : "agracia",
    "Daniel_Arredondo_Mart_nez" : "darredondo",
    "Daniel_Enrique_Salas_Su_rez" : "dsalas",
    "Daniel_Mart_Ram_rez" : "dmarti",
    "Ferran_de_San_Martin_Lagranje" : "fdesanmartin",
    "Israel_del_Toro_Mu_oz" : "ideltoro",
    "Joel_Francisco_G_mez_Garcia" : "jgomez",
    "Juan_Gimenez_Aguilar" : "jgimenez",
    "Juan_Guerra" : "jguerra",
    "Kevin_Chong_Benavides" : "kchong",
    "Laura_Mu_oz_Isidro" : "lmunoz",
    "Marc_G_mez_Aguilera" : "mgamez",
    "Miguel_Angel_Rodriguez_Fernandez" : "mrodriguez",
    "Raul_Guerrero_Carrasco" : "rguerrero",
    "Rosa_Ramon_Pedrosa" : "rramon",
    "Sandra_Mu_oz_Isidro" : "smunoz",
    "Sergio_Reinoso_Fuertes" : "sreinoso"
}

_UNCOMPRESS_COMMAND = {
        ".tar.gz" : "tar xzvf %s",
        ".tar"    : "tar xvf %s",
        ".zip"    : "unzip %s",
        ".rar"    : "unrar x %s"
        }

def normalize_name(name):
    return re.sub(_VALID_CHARS, _REPLACE_CHAR, name)

def normalize_filename(name):
    if name.endswith(".tar.gz"):
        filename, fileext = name.split(".", 1)
        fileext =".%s"%fileext
    else:
        filename, fileext = os.path.splitext(name)
    return "%s%s"%(normalize_name(filename), fileext), fileext

def create_exercise_folder_if_missing(course, exercise_name, exercise_id):
    normal_course = normalize_name(course)
    normal_exercise_name = normalize_name(exercise_name)
    path = "%s/%s-%s"%(normal_course, exercise_id, normal_exercise_name)
    if not os.path.isdir(path):
        os.makedirs(path)
        print "$ mkdir %s"%path
    return path

def create_submission_folder_if_missing(srcfilename, folder, student_name, internal_code, given_filename):
    normal_student_name = normalize_name(student_name)
    normal_filename, fileext = normalize_filename(given_filename)
    student_code = _STUDENT_NAME_CONVERSION.get(normal_student_name, normal_student_name)
    path = "%s/%s/%s"%(folder, student_code, internal_code)
    if os.path.isdir(path):
        print "already extracted %s"%path
    else:
        print "$ mkdir %s"%path
        os.makedirs(path)
        dstfilename = "%s/%s"%(path, normal_filename)
        shutil.copyfile(srcfilename, dstfilename)
        if fileext in _UNCOMPRESS_COMMAND:
            command = _UNCOMPRESS_COMMAND[fileext]
            prevpath = os.getcwd()
            os.chdir(path)
            print "%s/ $ %s"%(path, command%normal_filename)
            returnstatus = os.system(command%normal_filename)
            if returnstatus <> 0:
                print "ERROR: issuing command %s"%(command%normal_filename)
            os.remove(normal_filename)
            os.chdir(prevpath)


def process_zip(folder, zipfilename):
    tmppath = tempfile.mkdtemp()
    with zipfile.ZipFile(zipfilename, "r") as f:
        f.extractall(tmppath)
    file_content = os.listdir(tmppath)
    for c in file_content:
        m = re.match(_SUBMISSION_TEMPL, c)
        if m:
            create_submission_folder_if_missing(os.path.join(tmppath, c), folder, m.group(1), m.group(2), m.group(3))
        else:
            print "XXX NO ", c
    shutil.rmtree(tmppath)


print "Extracting Moodle exercises from this location"
lst = os.listdir('.')
for f in lst:
    m = re.match(_MOODLE_FILE_TEMPL, f)
    if m:
        folder = create_exercise_folder_if_missing(m.group(1), m.group(2), m.group(3))
        process_zip(folder, f)

