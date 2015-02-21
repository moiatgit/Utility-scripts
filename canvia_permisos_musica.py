#! /usr/bin/env python
# encoding: utf-8
import os, stat
#
_EXTENSIONS = [".mp3", ".MP3"]
_PERMIS_DIRECTORI = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP
_PERMIS_FITXER = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP
#
def canvia(d):
    """canvia els permisos del contingut musical del directori d """
    llista = os.listdir(d)
    for e in llista:
        obj = os.path.join(d, e)
        if os.path.isfile(obj):
            _, ext = os.path.splitext(e)
            if ext in _EXTENSIONS:
                os.chmod(obj, _PERMIS_FITXER)
                print "640", obj
        elif os.path.isdir(obj):
            os.chmod(obj, _PERMIS_DIRECTORI)
            print "750", obj
            canvia(obj)
#
if __name__=="__main__":
    print "Canviarà els permisos dels subdirectoris i els fitxers de música a partir de . "
    raw_input()
    canvia(".")
    
