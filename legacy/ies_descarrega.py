#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  ies_descarrega.py
# Autor:    moises
# Fecha:    20101001
# Descr:    Descarrega els fitxers d'un exercici de moodle
#           La descripció de funcionament es troba a la variable 
#           DESCR_FUNCIONAMENT
#
import sys, os, shutil
import optparse
import mechanize
import getpass
import re
import urllib2
import base64
#
DESCR_OBTENCIO_DADES = u"""
Requereix el número de l'exercici que es troba al moodle. 
Pot obtenir la url, l'usuari i el password per tres vies. Un cop
trobat valor per a un element, ignorarà la resta de vies. 
(1) se li pot passar com a argument. Compte: el password és llegible i 
pot quedar a l'històric de la shell. 
(2) els pot obtenir del fitxer ~/.descarrega.dat. El password apareix
codificat amb base64.b64encode() per dificultar una lectura furtiva. Es
recomana, però, vigilar els permisos de lectura del fitxer donada la 
fragilitat del mecanisme de protecció. 
(3) finalment, per l'usuari i password només, es pot introduir 
interactivament. El password no serà visible.",
"""
#
DESCR_FUNCIONAMENT="Descarrega els fitxers d'un exercici de moodle. " + \
                   DESCR_OBTENCIO_DADES 
# fitxer amb l'usuari i password del moodle
FITXER_CONF=os.path.join(os.environ["HOME"], ".descarrega.dat")
# sufix per la pàgina del login
LOGIN_URL="/login/index.php"
# plantilla per la pàgina dels lliuraments
ASSIGN_URL="/mod/assignment/submissions.php?id=%s"
# expressió regular per obtenir la url
REGEXP_URL='(https?://)?(.*?)(/.*)?$'
#
def connecta(url, usuari, password):
    """ connecta i retorna el mechanize.Browser """
    pglogin = url + LOGIN_URL
    br = mechanize.Browser()
    try:
        br.open(pglogin)
        br.select_form(nr=1)
        br.form['username']=usuari
        br.form['password']=password
        br.submit()
        if pglogin == br.geturl():
            raise Error
    except:
        br = None
    return br
#
def descarrega(exercici, directori, url, br):
    """ descarrega els exercicis de la pàgina a la destinació.
    Retorna True si tot ha anat correctament """
    pgexercici = url + ASSIGN_URL%exercici
    try:
        br.open(pgexercici)
        if br.geturl() <> pgexercici:
            print >> sys.stderr, "Error: no s'ha pogut accedir a la pàgina %s"%pgexercici
            return False
        links = br.links(url_regex='moddata/assignment')
        numdesc = 0     # comptador de fitxers descarregats
        for l in links:
            nomfitxer = os.path.basename(l.url)
            dirname = os.path.dirname(l.url)
            numlliurament = os.path.basename(dirname)   # id del lliurament
            if numlliurament.isdigit():
                strlliurament = "%04d"%int(numlliurament)
            else:
                strlliurament = numlliurament
            subdir = os.path.join(directori, strlliurament)
            if not os.path.exists(subdir):
                os.makedirs(subdir)
            fitxer = os.path.join(subdir, nomfitxer)
            print "Descarregant el fitxer", fitxer, 
            f = br.retrieve(l.url)
            shutil.move(f[0], fitxer)
            # os.rename(f[0], fitxer)
            print "(fet)"
            numdesc += 1
        print "Descarregat%(plural)s %(num)s fitxer%(plural)s"%\
            {"plural":"" if numdesc==1 else "s", "num":numdesc}
    except:
        print >> sys.stderr, "Error: no s'ha pogut accedir a %s (%s)"%(pgexercici, sys.exc_info()[0])
        return False
    return True
#
def obte_arguments():
    """ retorna els arguments de la crida al programa en forma d'opcions de optparse """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.1")
    p.add_option("-n", "--numexercici", action="store", help=u"Número identificador de l'exercici", nargs=1, dest="numexercici")
    p.add_option("-d", "--destinacio", action="store", help="Directori on deixar els fitxers resultants. Per defecte cwd", nargs=1, dest="destinacio", default=".")
    p.add_option("-u", "--username", action="store", help="Login de l'usuari", nargs=1, dest="username")
    p.add_option("-p", "--password", action="store", help="Password de l'usuari", nargs=1, dest="password")
    p.add_option("-w", "--website", action="store", help=u"URL de la pàgina principal del Moodle", nargs=1, dest="url")
    opcions, _ = p.parse_args()
    return opcions
#
def obte_params(url, username, password):
    """ obté els paràmetres url, usuari i pasword del fitxer de configuració
    i els retorna per a aquells paràmetres que no estiguin definits. """
    if os.path.exists(FITXER_CONF):
        f = open(FITXER_CONF)
        urltmp=f.readline().strip()
        usernametmp=f.readline().strip()
        passwordtmp=base64.b64decode(f.readline().strip())
        f.close()
        if not url: url=urltmp
        if not username: username=usernametmp
        if not password: password=passwordtmp
    return url, username, password
#
def obte_userpass(username, password):
    """ obté d'entrada estàndard i retorna l'usuari i el password """
    if not username:
        username = raw_input(      "Usuari:   ")
    if not password:
        password = getpass.getpass("Password: ")
    return username, password
#
def neteja_url(url):
    """ elimina informació de pàgina de la url """
    if url:
        m = re.match(REGEXP_URL, url)
        if m:
            url = m.group(1)+m.group(2)
        else:
            url = None
    return url
#
def main():
    opcions = obte_arguments()
    #
    if not opcions.numexercici:
        print >> sys.stderr, "Error: Cal indicar el número de l'exercici a descarregar"
        return 1
    #
    url, username, password = obte_params(opcions.url, opcions.username, opcions.password)
    url = neteja_url(url)
    if not url:
        print >> sys.stderr, "Error: Cal indicar la url del Moodle"
        return 2
    #
    username, password = obte_userpass(username, password)
    #
    print "Connectant a %s amb l'usuari %s"%(url, username)
    br = connecta(url, username, password)
    if not br:
        print >> sys.stderr, "Error: no es pot entrar amb l'usuari '%s'"%username
        return 3
    #
    print "Descarregant l'exercici %s"%opcions.numexercici
    if not descarrega(opcions.numexercici, opcions.destinacio, url, br):
        return 4
    #
    return 0
#
if __name__=="__main__":
    sys.exit(main())
