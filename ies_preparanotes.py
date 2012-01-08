#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  ies_preparanotes.py
# Autor:    moises
# Fecha:    20120107
# Descr:    Prepara les notes a partir d'un csv al format requerit per
#           ies_posanotes.py.
#
import sys, os
import optparse
import csv
#
DESCR_FUNCIONAMENT=u"""
Prepara les notes a partir d'un csv al format requerit per
ies_posanotes.py."""
#
DELIMITADOR_DEFECTE="^"
#
def obte_arguments():
    """ retorna els arguments de la crida al programa en forma 
    d'opcions de optparse """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.0")
    p.add_option("-f", "--fromfile", action="store", help=u"Fitxer que conté les notes en format csv", nargs=1, dest="source")
    p.add_option("-t", "--tofile", action="store", help=u"Fitxer on deixar les notes formatades", nargs=1, dest="destination")
    p.add_option("-d", "--delimitador", action="store", help=u"Caràcter delimitador del fitxer de notes. Per defecte '^'", nargs=1, dest="delimitador", default="^")
    opcions, _ = p.parse_args()
    return opcions
#
def main():
    opcions = obte_arguments()
    
    source = opcions.source if opcions.source else sys.stdin
    destination = opcions.destination if opcions.destination else sys.stdout
    delimitador = #
    if posanotes(notes, br):
       print "Fet!"
    else:
       return 7 
    return 0
#
if __name__=="__main__":
    sys.exit(main())
