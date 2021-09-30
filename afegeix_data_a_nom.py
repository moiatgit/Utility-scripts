#! /usr/bin/env python
# encoding: utf-8
# Programa que reanomena tots els fitxers del directori actual per 
# la data aaaammdd-hhmmss seguida del nom del fitxer
#
import datetime, os, sys
#
dirbase = "."
#
print "%s [--help] [--force] [--recursive] [--move]"%sys.argv[0]
print "Reanomena tots els fitxers regulars del directori actual per",\
      "la data aaaammdd-hhmmss seguida del nom del fitxer"
if "--help" in sys.argv[1:]:
    print "L'opció --force és requerida per a realitzar els canvis. Altrament,",\
          "només mostra el que passaria"
    print "L'opció --recursive permet realitzar els canvis en subdirectoris",\
          "(No considera enllaços)"
    print "L'opció --move permet moure els fitxers al directori actual i si",\
          "queda buit, elimina el subdirectori"
    print 
    sys.exit(0)
#
force = "--force" in sys.argv[1:]
recursive =  "--recursive" in sys.argv[1:]
move = "--move" in sys.argv[1:]
directoris = [dirbase]
while len(directoris)>0:
    d = directoris.pop(0)
    llista = os.listdir(d)
    for e in llista:
        fitxer = os.path.join(d, e)
        if not os.path.islink(fitxer):
            if os.path.isfile(fitxer):
                mtime = os.path.getmtime(fitxer)
                prefix = datetime.datetime.fromtimestamp(mtime).strftime("%Y%m%d-%H%M%S")
                if e.startswith(prefix):    # ja està formatat amb la data
                    print "Ignorat", fitxer
                else:
                    if move:
                        noufitxer = os.path.join(dirbase, "%s_%s"%(prefix, e))
                    else:
                        noufitxer = os.path.join(d, "%s_%s"%(prefix, e))
                    print "mv %s %s"%(fitxer, noufitxer)
                    if force:
                        try:
                            os.rename(fitxer, noufitxer)
                        except Exception, exc:
                            print >>sys.stderr, "Error reanomenant el fitxer.", exc
            elif recursive and os.path.isdir(fitxer):
                directoris.append(fitxer)
    # intenta eliminar el directori si no està buit
    if move and not d == dirbase:
        try:
            os.rmdir(d)
        except:
            pass


