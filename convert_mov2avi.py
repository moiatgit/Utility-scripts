#! /usr/bin/env python
# encoding: utf-8
# programa que converteix de .mov a .avi
# a partir del cwd cerca recursivament tots els directoris i
# quan troba un fitxer .MOV o .mov el converteix a .avi mantenint
# el mateix nom.
# En cas que ja existeixi un fitxer .avi (o .AVI) amb el mateix nom
# al directori del .mov, mostra un warning i no fa res.
# No segueix links
# En cas que no s'especifiqui l'opció --force només mostra els fitxers
# a convertir.
import optparse, os
import subprocess
import shlex
#
_CONVERTITS = list()
# La conversió es fa en dues passades, segons la proposta de 
# http://rubensa.wordpress.com/2006/08/27/mencoder-mov-2-avi/
_COMMAND_PAS1 = "mencoder %s -o /dev/null -vf scale=496:368 -ofps 25 -srate 48000 -af channels=2 -ovc xvid -xvidencopts pass=1:bitrate=4700 -oac mp3lame -lameopts vbr=3:br=32"
_COMMAND_PAS2 = "mencoder %s -o %s -vf scale=496:368 -ofps 25 -srate 48000 -af channels=2 -ovc xvid -xvidencopts pass=2:bitrate=4700 -oac mp3lame -lameopts vbr=3:br=32"
#mencoder 20100829-114720_MVI_4157.MOV -o /dev/null -vf scale=496:368 -ofps 25 -srate 48000 -af channels=2 -ovc xvid -xvidencopts pass=1:bitrate=4700 -oac mp3lame -lameopts vbr=3:br=32
#mencoder 20100829-114720_MVI_4157.MOV -o MVI_4157.avi -vf scale=496:368 -ofps 25 -srate 48000 -af channels=2 -ovc xvid -xvidencopts pass=2:bitrate=4700 -oac mp3lame -lameopts vbr=3:br=32
# altres intents previs
#call(["mencoder", "-oac", "mp3lame", "-lameopts", "q=0", "-ovc", "xvid", "-xvidencopts",  "bitrate=1200", fitxer, "-o", fitxeravi])
#call(["mencoder", "-oac", "mp3lame", "-lameopts", "cbr=128", "-ovc", "xvid", "-xvidencopts",  "bitrate=1200", fitxer, "-o", fitxeravi])
#call(["ffmpeg", "-i", fitxer, "-sameq", "-vcodec", "msmpeg4v2", "-acodec", "pcm_u8", fitxeravi])
#ffmpeg -i MVI_3441.MOV -sameq -vcodec msmpeg4v2 -acodec pcm_u8 output.avi
#
def converteix(dirpath, force, override):
    """ converteix tots els fitxers .mov del directori dirpath i els seus
    subdirectoris """
    global _CONVERTITS
    llista = os.listdir(dirpath)
    for e in llista:
        fitxer = os.path.join(dirpath, e)
        if not os.path.islink(fitxer):  # no segueix links
            if os.path.isfile(fitxer):
                nom, ext = os.path.splitext(fitxer)
                if ext.upper() == ".MOV":
                    fitxeravi = "%s.avi"%nom
                    if not override and os.path.exists(fitxeravi):
                        print "Warning: ja existeix %s"%fitxeravi
                    else:
                        print "Convert %s"%fitxer
                        if force:
                            # pas 1
                            args = shlex.split(_COMMAND_PAS1%fitxer)
                            subprocess.call(args)
                            # pas 2
                            args = shlex.split(_COMMAND_PAS2%(fitxer, fitxeravi))
                            subprocess.call(args)
                            _CONVERTITS.append(fitxer)
            elif os.path.isdir(fitxer):
                converteix(fitxer, force, override)
#
def main():
    p = optparse.OptionParser(description="Conversor de .mov (versió de càmera de fotos) a .avi.",
        version="1.1")
    p.add_option("-f", "--force", action="store_true", dest="force", default=False, help=u"força la conversió")
    p.add_option("-o", "--override", action="store_true", dest="override", default=False, help=u"en cas que existeixi el fitxer destinació, el sobrescriu")
    p.add_option("-d", "--dir", action="store", help=u"indica el directori des d'on començar la conversió", nargs=1, dest="dir", default=os.getcwd())
    opcions, arguments = p.parse_args()
    converteix(opcions.dir, opcions.force, opcions.override)
    if len(_CONVERTITS)>0:
        print "S'ha convertit els següents fitxers"
        for l in _CONVERTITS:
            print "\t%s"%l
#
if __name__=="__main__":
    main()            
