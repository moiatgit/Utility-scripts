#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  descarregamoodle.py
# Autor:    moises
# Fecha:    20101001
# Descr:    Descarrega els fitxers d'un exercici de moodle
#           Requereix el número de l'exercici que es troba al moodle
#
import sys, os
import optparse
import mechanize
import getpass
#
FITXER_CONF=os.path.join(os.environ["HOME"], ".descarrega.dat")     # fitxer amb l'usuari i password del moodle
#
def descarrega(exercici, directori, usuari, password):
    """ descarrega els exercicis de la pàgina a la destinació """
    br = mechanize.Browser()
    # login
    br.open('http://moodle.insjoandaustria.org/login/index.php')
    br.select_form(nr=1)
    br.form['username']=usuari
    br.form['password']=password
    br.submit()
    # obtenció de la pàgina amb l'exerici
    pgexercici = 'http://moodle.insjoandaustria.org/mod/assignment/submissions.php?id=%s'%exercici
    br.open(pgexercici)
    for l in br.links(url_regex='moddata/assignment'):
        nomfitxer = os.path.basename(l.url)
        dirname = os.path.dirname(l.url)
        numlliurament = os.path.basename(dirname)                   # id del lliurament
        strlliurament = "%04d"%int(numlliurament) if numlliurament.isdigit() else numlliurament
        subdir = os.path.join(directori, strlliurament)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        fitxer = os.path.join(subdir, nomfitxer)
        print "Descarregant el fitxer", fitxer, 
        f = br.retrieve(l.url)
        os.rename(f[0], fitxer)
        print "(fet)"
#
def main():
    p = optparse.OptionParser(description="Descarrega els fitxers d'un exercici de moodle",
        version="1.1")
    p.add_option("-n", "--numexercici", action="store", help=u"Número identificador de l'exercici", nargs=1, dest="numexercici")
    p.add_option("-d", "--destinacio", action="store", help="Directori on deixar els fitxers resultants. Per defecte cwd", nargs=1, dest="destinacio", default=".")
    p.add_option("-u", "--username", action="store", help="Login de l'usuari", nargs=1, dest="username")
    p.add_option("-p", "--password", action="store", help="Password de l'usuari", nargs=1, dest="password")
    opcions, arguments = p.parse_args()
    if not opcions.numexercici:
        print >> sys.stderr, "Error: Cal indicar el número de l'exercici a descarregar"
        return -1
    username=""
    password=""
    if not (opcions.username or opcions.password):
        if os.path.exists(FITXER_CONF):
            f = open(FITXER_CONF)
            username=f.readline().strip()
            password=f.readline().strip()
            f.close()
    if username == "":
        if not opcions.username:
            username = raw_input(      "Usuari:   ")
        else:
            username = opcions.username
        if not opcions.password:
            password = getpass.getpass("Password: ")
        else:
            password = opcions.password
    print "Descarregant l'exercici %s amb l'usuari %s"%(opcions.numexercici, username)
    descarrega(opcions.numexercici, opcions.destinacio, username, password)
    return 0
#
if __name__=="__main__":
    sys.exit(main())
