#! /usr/bin/env python
# encoding: utf-8
# Programa que reanomena tots els fitxers del directori actual que estan 
# marcats amb una data de la forma aaaammdd-hhmmss 
# amb la data i nom que se li passi
#
import datetime, os, re, sys
#
dirbase = "."
#
print "%s [--help] <data> <nom> [--replace] [--force]"%sys.argv[0]
print "Reanomena tots els fitxers regulars del directori actual amb data", \
      "coincident amb l'expressió regular <data> i amb el nom <nom>.", \
      "Només mostra el que faria si --force no està present"
print "Accepta dates amb format aaaammdd-hhmmss i aaaammddhhmmss"
if "--help" in sys.argv[1:]:
    print "L'opció --force és requerida per a realitzar els canvis. Altrament,",\
          "només mostra el que passaria"
    print "L'opció --replace elimina el nom actual del fitxer (excepte la data)",\
          "de manera que només queda la data, el <<nom>> i, en cas que calgui,",\
          "un número consecutiu per a desambiguar."
    print 
    sys.exit(0)
#
if len(sys.argv)<3:
    print >>sys.stderr, "Error: nombre de paràmetres incorrecte"
    sys.exit(-1)
#
redata = sys.argv[1]
nomsubst = sys.argv[2]
#
force = "--force" in sys.argv[1:]
replace =  "--replace" in sys.argv[1:]
#
d = dirbase
llista = os.listdir(d)
#
desambiguador = 0       # és un comptador per a desambiguar
#
for e in llista:
    fitxer = os.path.join(d, e)
    if not os.path.islink(fitxer):
        if os.path.isfile(fitxer):
            nom, ext = os.path.splitext(e)
            prefix, _, rest = nom.partition('_')
            if '-' in prefix:               # considera els dos tipus de format de data
                numchar = 15
            else:
                numchar = 14
            if not len(prefix) == numchar: # no hi ha prou caracters per tenir la data
                continue
            m = re.match(redata, prefix)
            if m == None:
                continue
            if replace:
                nou = "%s_%s%s"%(prefix, nomsubst, ext)
            else:
                nou = "%s_%s_%s%s"%(prefix, nomsubst, rest, ext)
            noufitxer = os.path.join(d, nou)
            if os.path.exists(noufitxer):
                nom, ext = os.path.splitext(noufitxer)
                noufitxer = "%s_%s%s"%(nom, desambiguador, ext)
                desambiguador+=1
            print "mv %s %s"%(fitxer, noufitxer)
            if force:
                try:
                    os.rename(fitxer, noufitxer)
                except Exception, exc:
                    print >>sys.stderr, "Error reanomenant el fitxer.", exc

