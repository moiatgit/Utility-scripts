#! /usr/bin/env python
# encoding: utf-8
# programa que converteix de .rmvb a .avi
# a partir del cwd cerca recursivament tots els directoris i
# quan troba un fitxer .RMVB o .rmvb el converteix a .avi mantenint
# el mateix nom.
# En cas que ja existeixi un fitxer .avi (o .AVI) amb el mateix nom
# al directori del .rmvb, mostra un warning i no fa res.
# No segueix links
# En cas que no s'especifiqui l'opció --force només mostra els fitxers
# a convertir.
import optparse, os
from subprocess import call
#
_CONVERTITS = list()
#
def converteix(dirpath, force):
    """ converteix tots els fitxers .rmvb del directori dirpath i els seus
    subdirectoris """
    global _CONVERTITS
    llista = os.listdir(dirpath)
    for e in llista:
        fitxer = os.path.join(dirpath, e)
        if not os.path.islink(fitxer):  # no segueix links
            if os.path.isfile(fitxer):
                nom, ext = os.path.splitext(fitxer)
                if ext.upper() == ".RMVB":
                    fitxeravi = "%s.avi"%nom
                    if os.path.exists(fitxeravi):
                        print "Warning: ja existeix %s"%fitxeravi
                    else:
                        print "Convert %s"%fitxer
                        if force:
                            call(["mencoder", "-oac", "mp3lame", "-lameopts", "cbr=128", "-ovc", "xvid", "-xvidencopts",  "bitrate=1200", fitxer, "-o", fitxeravi])
                            #mencoder -oac mp3lame -lameopts cbr=128 -ovc xvid -xvidencopts bitrate=1200 video_input.rmvb -o video_output.avi
                            _CONVERTITS.append(fitxer)
            elif os.path.isdir(fitxer):
                converteix(fitxer, force)
#
def main():
    p = optparse.OptionParser(description="Conversor de .mov a .avi",
        version="1.0")
    p.add_option("-f", "--force", action="store_true", dest="force", default=False, help=u"força la conversió")
    p.add_option("-d", "--dir", action="store", help=u"indica el directori des d'on començar la conversió", nargs=1, dest="dir", default=os.getcwd())
    opcions, arguments = p.parse_args()
    converteix(opcions.dir, opcions.force)
    if len(_CONVERTITS)>0:
        print "S'ha convertit els següents fitxers"
        for l in _CONVERTITS:
            print "\t%s"%l
#
if __name__=="__main__":
    main()            
