#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  formatanotes.py
# Autor:    moises
# Fecha:    20101028
# Descr:    Formata les notes per a ser tractades pel programa posanotes.py
#           Les notes han d'estar incloses a un fitxer .csv
#           El format esperat és un csv separat per _DELIMITADOR_ORIGEN, on:
#               - la primera fila correspon als títols de capçalera
#               - la capçalera de la primera columna és "id"
#               - la primera columna indica l'identificador de l'alumne
#               - la segona columna indica la qualificació moodle en base 100 (o NP)
#
#           Com a sortida es genera un csv separat per _DELIMITADOR_DESTINACIO, on
#               - no hi ha capçalera
#               - la primera columna indica l'identificador de l'alumne
#               - la segona columna indica la qualificació moodle en base 100 (els NP d'entrada passen a ser 0)
#               - la tercera columna indica un comentari en html amb NP si la nota era no presentat, o una composició
#                 de les columnes restants de l'entrada en forma de UL amb <li>capçalera: <b>valor</b></li>
#
import csv
import optparse
import os
import sys
#
_DELIMITADOR_ORIGEN = ','           # marca de delimitació origen
_DELIMITADOR_DESTINACIO = '^'       # marca de delimitació destinació
#
def es_numeric(val):
    """retorna True si val és numèric"""
    return unicode(val).isnumeric()
#
def llegeix_cap(reader):
    """ llegeix la fila de capçaleres. Si no comença amb el mot "id", mostra error i 
    finalitza execució. Altrament retorna les capçaleres"""
    filacap    = reader.next()      # fila amb les capçaleres
    if filacap[0].lower() <> "id":
        print >> sys.stderr, "Error: la capçalera ha de començar amb id"
        sys.exit(1)
    return filacap
#
def llegeix_files(reader, ncol):
    """ llegeix les files amb les notes i les retorna en una llista de files.
    Ignora les files que no tenen un id numèric > 0, i aquelles que no arriben
    a disposar del nombre de columnes indicat per ncol."""
    files = list()
    for r in reader:
        i = r[0]
        if es_numeric(i) and int(i)>0 and len(r)==ncol:
            files.append(r)
        else:
            print >> sys.stderr, "Warning: ignorada la fila '%s'"%r
    return files
#
def composa_comentaris(cap, fila):
    """ composa els comentaris de la fila a partir de la capçalera """
    comentaris = list()
    for i in range(len(fila) - 2):
        comentaris.append("<li>%s: <b>%s</b></li>"%(cap[i+2], fila[i+2]))
    if len(comentaris)==0:
        return ""
    else:
        return "<ul>%s</ul>"%("".join(comentaris))
#
def formata_files(cap, files):
    """ formata les files a partir de la capçalera.
    Retorna la composició segons sortida [(id, nota, comentari)]
    on a id se li eliminen els 0 inicials, a nota se la converteix
    en un valor numèric quan NP, i a comentaris es composen els comentaris
    o bé un missatge de NP en cas de no presentat."""
    notes = list()
    for fila in files:
        if fila[1].lower() == "NP":
            nota = 0
            comentaris = "No Presentat"
        else:
            nota = fila[1]
            comentaris = composa_comentaris(cap, fila)
        linia = (fila[0].lstrip("0"), nota, comentaris)
        notes.append(linia)
    return notes
#
def formata(reader, writer):
    """ formata el fitxer d'origen i el guarda a destinacio """
    cap = llegeix_cap(reader)               # llegeix les capçaleres
    files = llegeix_files(reader, len(cap)) # llegeix la resta de files
    resultat = formata_files(cap, files)    # formata les files segons sortida
    writer.writerows(resultat)              # escriu el resultat al writer
#
def main():
    p = optparse.OptionParser(description=u"Formata les notes d'un exercici de moodle",
        version="1.0")
    p.add_option("-o", "--origen", action="store", help=u"Fitxer que conté les notes d'origen en format csv", nargs=1, dest="origen")
    p.add_option("-d", "--destinacio", action="store", help=u"Fitxer on deixar el resultat formatat", nargs=1, dest="destinacio")    
    p.add_option("-f", "--force", action="store_true", help=u"Indica que es sobreescrigui el fitxer de destinació si ja existia", dest="force")    
    opcions, arguments = p.parse_args()
    if not opcions.origen:
        print >> sys.stderr, "Error: Cal indicar el fitxer d'origen"
        return 1
    if not opcions.destinacio:
        print >> sys.stderr, "Error: Cal indicar el fitxer destinació"
        return 1
    #
    if os.path.exists(opcions.destinacio) and not opcions.force:
        print >> sys.stderr, "Error: ja existeix el fitxer de destinació. --force per sobreescriure"
        return 1
    #
    try:
        forigen = open(opcions.origen)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer d'origen"
        return 1
    #
    try:
        reader = csv.reader(forigen, delimiter=_DELIMITADOR_ORIGEN)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer d'origen com a csv"
        return 1
    #
    try:
        fdestinacio = open(opcions.destinacio, "w")
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer de destinació"
        return 1
    #
    try:
        writer = csv.writer(fdestinacio, delimiter=_DELIMITADOR_DESTINACIO)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer de destinació com a csv"
        return 1
    #
    formata(reader, writer)
    #
    fdestinacio.close()
    forigen.close()
    #
    return 0
#
if __name__=="__main__":
    sys.exit(main())
