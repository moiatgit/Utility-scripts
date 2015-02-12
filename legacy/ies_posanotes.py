#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  ies_posanotes.py
# Autor:    moises
# Fecha:    20101026
# Descr:    Posa notes a un exercici de moodle
#           Les notes han d'estar incloses a un fitxer .csv amb el format:
#               id alumne ^ nota ^ comentari
#           On la nota s'espera en base 100 i els comentaris poden ser 
#           qualsevol string que es pugui representar com a comentari "raw"
#           d'una nota de Moodle
#
#           Fa servir mètodes de ies_descarrega.py
#
import sys, os
import optparse
import mechanize
import getpass
import csv
import ies_descarrega
#
ID_FORM_LLIURAMENTS = 'fastg'      # id del formulari amb els lliuraments
DESCR_FUNCIONAMENT=u"""
Posa notes d'un exercici de moodle. 
Cal indicar el camí al fitxer que conté les notes amb el 
format (idalumne^qualificació^comentari). On idalumne correspon a 
l'identificador Moodle de l'alumne, la qualificació és el valor 
numèric i el comentari és un string tal i com es col·locarien al 
formulari de retroacció del Moodle. """ + \
                   ies_descarrega.DESCR_OBTENCIO_DADES
#
def carreganotes(fitxer, delimitador):
    """ carrega les notes del fitxer i les retorna en forma de diccionari
    amb clau id d'estudiant i valor la tupla (nota, comentari) """
    if delimitador==0:
        delimitador="^"
    else:
        delimitador=delimitador[0]  # ens quedem amb el primer caràcter
    try:
        f = open(fitxer)
        reader = csv.reader(f, delimiter=delimitador)
        notes = dict()
        for linia in reader:
            if len(linia)!=3:
                print >> sys.stderr, "Error: format incorrecte del fitxer. Linia:%s"%linia
                raise Exception()
            notes[linia[0].strip()] = (linia[1].strip(), linia[2].strip())
        f.close()
    except:
        print >> sys.stderr, "Error carregant les notes del fitxer %s"%fitxer
        notes = None
    return notes
#
def extreunum(s):
    """ extreu el número de un nom de control com ara 'menu[25]' """
    resultat = ''
    try:
        resultat = s.split("[")[1][:-1]
    except:
        pass
    return resultat
#
def trobaformindex(br, id):
    """ troba al browser el formulari amb identificador id i retorna 
    la seva posició. -1 si no el troba """
    index = 0
    trobat = False
    for f in br.forms():
        if 'id' in f.attrs and f.attrs['id']==id:
            trobat = True
            break
        index += 1
    if not trobat:
        index = -1
    return index  
#
def posanotes(notes, br):
    """ posa les notes a l'exercici. Retorna True si tot correcte. """
    #
    index = trobaformindex(br, ID_FORM_LLIURAMENTS)
    if index < 0:
        print >>sys.stderr, "Error: no s'ha trobat el formulari de lliuraments"
        return False
    br.select_form(nr=index)
    numassign = 0       # nombre de notes assignades
    numnp = 0           # nombre d'alumnes sense nota
    for c in br.controls:
        if c.name.startswith("menu["):
            idestudiant = extreunum(c.name)
            if idestudiant in notes:
                nota = notes[idestudiant][0]
                numassign += 1
            else:
                nota = '-1'   # no es disposa de nota
                numnp += 1
            c.value=[nota]
            continue
        if c.name.startswith("submissioncomment["):
            idestudiant = extreunum(c.name)
            if idestudiant in notes:
                c.value=notes[idestudiant][1]
    #
    br.submit()
    print "Notes assignades: %s"%numassign
    print "Notes NP        : %s"%numnp
    return True # tot correcte
#
def obte_arguments():
    """ retorna els arguments de la crida al programa en forma 
    d'opcions de optparse """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.0")
    p.add_option("-n", "--numexercici", action="store", help=u"Número identificador de l'exercici", nargs=1, dest="numexercici")
    p.add_option("-f", "--fitxer", action="store", help=u"Fitxer que conté les notes en format csv", nargs=1, dest="fitxer")
    p.add_option("-u", "--username", action="store", help=u"Login de l'usuari", nargs=1, dest="username")
    p.add_option("-p", "--password", action="store", help=u"Password de l'usuari", nargs=1, dest="password")
    p.add_option("-w", "--website", action="store", help=u"URL de la pàgina principal del Moodle", nargs=1, dest="url")
    p.add_option("-d", "--delimitador", action="store", help=u"Caràcter delimitador del fitxer de notes. Per defecte '^'", nargs=1, dest="delimitador", default="^")
    opcions, _ = p.parse_args()
    return opcions
#
def carrega_paginaexercici(br, url, exercici):
    """ carrega la pàgina de l'exercici sobre el browser i el retorna """
    pgexercici = url + ies_descarrega.ASSIGN_URL%exercici
    br.open(pgexercici)
    if br.geturl() <> pgexercici:
        print >> sys.stderr, "Error: no es pot accedir a la pàgina %s"%pgexercici
        br = None
    return br
#
def main():
    opcions = obte_arguments()
    
    if not opcions.numexercici:
        print >> sys.stderr, "Error: Cal indicar el número de l'exercici a qualificar"
        return 1
    if not opcions.fitxer:
        print >> sys.stderr, "Error: Cal indicar el fitxer que conté les notes"
        return 2
    #
    notes = carreganotes(opcions.fitxer, opcions.delimitador)
    if not notes: 
        print >> sys.stderr, "Error: El fitxer %s no conté notes en el format esperat"%opcions.fitxer
        return 3
    #
    url, username, password = ies_descarrega.obte_params(opcions.url, opcions.username, opcions.password)
    url = ies_descarrega.neteja_url(url)
    if not url:
        print >> sys.stderr, "Error: Cal indicar la url del Moodle"
        return 4
    #
    username, password = ies_descarrega.obte_userpass(username, password)
    #
    print "Connectant a %s amb l'usuari %s"%(url, username)
    br = ies_descarrega.connecta(url, username, password)
    if not br:
        print >> sys.stderr, "Error: no es pot entrar amb l'usuari '%s'"%usuari
        return 5
    #
    br = carrega_paginaexercici(br, url, opcions.numexercici)
    if not br:
        return 6
    #
    if posanotes(notes, br):
       print "Fet!"
    else:
       return 7 
    return 0
#
if __name__=="__main__":
    sys.exit(main())
