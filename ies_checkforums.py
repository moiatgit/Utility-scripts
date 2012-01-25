#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  ies_checkforums.py
# Autor:    moises
# Fecha:    20120124
# Descr:    Comprova si hi ha entrades sense llegir a un o més fòrums
#           de Moodle.
#           La descripció de funcionament es troba a la variable 
#           DESCR_FUNCIONAMENT
#
import sys, os
import optparse
import mechanize
from BeautifulSoup import BeautifulSoup
import getpass
import re
import urllib2
import base64
#
DESCR_OBTENCIO_DADES = u"""
Pot obtenir la url, l'usuari i el password, i els identificadors
dels fòrums a comprovar per tres vies. Un cop
trobat valor per a un element, ignorarà la resta de vies. 
(1) se li pot passar com a argument. Compte: el password és llegible i 
pot quedar a l'històric de la shell. 
(2) els pot obtenir del fitxer ~/.checkforums.dat. El password apareix
codificat amb base64.b64encode() per dificultar una lectura furtiva. Es
recomana, però, vigilar els permisos de lectura del fitxer donada la 
fragilitat del mecanisme de protecció. 
(3) finalment, per l'usuari i password només, es pot introduir 
interactivament. El password no serà visible."
"""
#
DESCR_FUNCIONAMENT=u"Comprova si hi ha entrades sense llegir a un o més fòrums de Moodle " + \
                   DESCR_OBTENCIO_DADES 
# fitxer amb l'usuari i password del moodle
FITXER_CONF=os.path.join(os.environ["HOME"], ".checkforums.dat")
# sufix per la pàgina del login
LOGIN_URL="/login/index.php"
# plantilla per la pàgina dels lliuraments
FORUM_URL="/mod/forum/view.php?id=%s"
# expressió regular per obtenir la url
REGEXP_URL='(http://)?(.*?)(/.*)?$'
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
def obte_titol(soup):
    """ obté i retorna el títol del fòrum """
    try:
        titol = soup.title.contents[0]
    except:
        titol = "Desconegut"
    return titol
#
def seguiment_actiu(soup):
    """ retorna True si el seguiment del fórm està actiu """
    try:
        res = soup.table.thead.tr.contents[3].contents[0] == u'No llegit&nbsp;'
    except:
        res = False
    return res
#
def comprova_forum(forumid,  url, br):
    """ comprova el fòrum amb l'identificador forumid. """
    pgforum = url + FORUM_URL%forumid
    try:
        pagina = br.open(pgforum)
        if br.geturl() <> pgforum:
            print >> sys.stderr, "Error: no s'ha pogut accedir a la pàgina %s"%pgforum
            return
        html = pagina.read()
        soup = BeautifulSoup(html)
        titol = u"[%s]: %s"%(forumid, obte_titol(soup))
        if not seguiment_actiu(soup):
            print >> sys.stderr, "Avís: el fòrum %s no té el seguiment actiu"%titol
            return
        llista = []     # llista d'entrades amb comentaris sense llegir
        for tr in soup.table.findAll('tr')[1:]:
            llista_td = tr.findAll('td')
            n = llista_td[4].text 
            if n <> '0':
                llista.append((llista_td[0].text, n))
        if llista <> []:
            print u"%s: té comentaris nous a les entrades:"%titol
            for e, n in llista:
                print u"\t%s (%s comentari%s)"%(e, n, "" if n=="1" else "s")
    except:
        print >> sys.stderr, "Error: no s'ha pogut accedir a %s "%pgforum
        print >> sys.stderr, sys.exc_info()[0]
#
def obte_arguments():
    """ retorna els arguments de la crida al programa en forma d'opcions de optparse """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.1")
    p.add_option("-i", "--idforum", action="store", help=u"Número identificador del fòrum o forums (separats per coma i sense espais)", nargs=1, dest="forums")
    p.add_option("-u", "--username", action="store", help="Login de l'usuari", nargs=1, dest="username")
    p.add_option("-p", "--password", action="store", help="Password de l'usuari", nargs=1, dest="password")
    p.add_option("-w", "--website", action="store", help=u"URL de la pàgina principal del Moodle", nargs=1, dest="url")
    opcions, _ = p.parse_args()
    return opcions
#
def obte_params(url, username, password, forums):
    """ obté els paràmetres url, usuari i pasword, i forums del fitxer de configuració
    i els retorna per a aquells paràmetres que no estiguin definits. """
    if os.path.exists(FITXER_CONF):
        f = open(FITXER_CONF)
        urltmp=f.readline().strip()
        usernametmp=f.readline().strip()
        passwordtmp=base64.b64decode(f.readline().strip())
        forumstmp=f.readline().strip()
        f.close()
        if not url: url=urltmp
        if not username: username=usernametmp
        if not password: password=passwordtmp
        if not forums:   forums=forumstmp
    return url, username, password, forums
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
            url = "http://"+m.group(2)
        else:
            url = None
    return url
#
def obte_forums(forums):
    """ en cas que forums no estigui definit, demana la llista d'ids a l'usuari i
    la retorna """
    if not forums:
        forums = raw_input("Ids dels fòrums:   ")
    return forums
#
def neteja_forums(forums):
    """ retorna la llista d'identificadors numèrics """
    return re.findall("[0-9]+", forums)
#
def main():
    opcions = obte_arguments()
    #
    url, username, password, forums = obte_params(opcions.url, opcions.username, opcions.password, opcions.forums)
    #
    forums = obte_forums(forums)
    llistaforums = neteja_forums(forums)
    if not llistaforums:
        print >> sys.stderr, "Error: Cal indicar al menys un fòrum a comprovar"
        return 2
    #
    url = neteja_url(url)
    if not url:
        print >> sys.stderr, "Error: Cal indicar la url del Moodle"
        return 3
    #
    username, password = obte_userpass(username, password)
    #
    # print "Connectant a %s amb l'usuari %s"%(url, username)
    br = connecta(url, username, password)
    if not br:
        print >> sys.stderr, "Error: no es pot entrar amb l'usuari '%s'"%usuari
        return 4
    #
    for f in llistaforums:
        comprova_forum(f, url, br)
    #
    return 0
#
if __name__=="__main__":
    sys.exit(main())
