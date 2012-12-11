#! /usr/bin/env python
# encoding: utf-8
#
#   Ús: sys.argv[0] numver nomfitxer.quiz [--force] [--noshuffle]
#
#   On:
#
#       numver: nombre de versions a composar
#
#       nomfitxer.quiz: nom del fitxer amb les preguntes i respostes
#       reordenades
#
#       --force: opcionalment permet indicar que es poden sobrescriure
#       els fitxers de sortida.

#       --noshuffle: opcionalment permet indicat que no es barregin les preguntes
#       ni les respostes.
#
#  L'entrada ha de tenir el format
#       .. pregunta:
#       títol de la pregunta
#       .. enunciat:
#       text de l'enunciat
#       .. resposta: [+-]
#       text de la resposta
#       «altres respostes»
#       «altres preguntes»
#
#  Qualsevol línia pot començar amb ".. #" o ".. //" per indicar que un comentari
#
#  El resultat generat tindrà format restructuredtext
#
#  TODO: de moment aquest codi està en fase molt experimental. Caldria afegir-li
#   alguns elements que el facin més robust (ex. control d'errors amb el paràmetre
#   esperat) així com alguns elements de parametrització (ex. format de sortida) i
#   d'ajuda a l'ús (ex. capacitat per processar respostes i pesos, i de generar
#   un document associat amb la correcció de l'ordenació generada)
#
import os, sys, random, re
#
class Pregunta:
    def __init__(self, titol, enunciat, respostes):
        """ inicialitza la pregunta """
        self.titol = titol.strip("\n")
        self.enunciat = enunciat.strip("\n")
        self.respostes = [(r[0].strip("\n"), r[1]) for r in respostes]

    def mostra_pregunta(self, num=0):
        """ mostra la pregunta amb el número indicat. """
        if num == 0:
            titol = "Pregunta: %s"%self.titol
        else:
            titol = "Pregunta %s: %s"%(num, self.titol)

        # mostra el títol de la pregunta
        print titol
        print "-" * len(titol)
        print

        # mostra l'enunciat
        print self.enunciat
        print

        print "-"*4     # separació de les respostes
        print

        # mostra les diferents respostes
        for i in range(len(self.respostes)):
            print "*%s)*"%chr(ord("a")+i),
            print self.respostes[i][0]
            print

    def barreja_respostes(self):
        """ barreja les respostes """
        random.shuffle(self.respostes)

    def mostra_noms_respostes(self, num):
        """ mostra els ids de les respostes de la pregunta amb el número indicat"""
        for i in range(len(self.respostes)):
            print "p%s.%s "%(num, chr(ord("a")+i)),

    def mostra_pesos_respostes(self, num):
        """ mostra els pesos de les respostes de la pregunta amb el número indicat"""
        for i in range(len(self.respostes)):
            print "%s "%(self.respostes[i][1]),

#
def barreja(preguntes):
    """ a partir d'una llista de preguntes, genera una nova llista de preguntes
    en les que s'ha barrejat:
    1. les preguntes
    2. les respostes de cada pregunta """
    for p in preguntes:
        p.barreja_respostes()
    random.shuffle(preguntes)
#
def processa_continguts(f):
    """ llegeix el fitxer i intenta interpretar les preguntes que inclou.
        Retorna una llista de Questions """
    preguntes = []
    estat = "pregunta"  # de moment no ha trobat pregunta
    titol = ""
    enunciat = ""
    resposta = ""
    pes = ""
    respostes = []
    nlin = 0
    for lin in f:
        nlin += 1
        if lin.startswith(".. #") or lin.startswith(".. /"):   # és un comentari
            pass
        elif estat == "pregunta":
            if lin.startswith(".. pregunta:"):
                estat = "títol"  # ha trobat una pregunta i mira d'obtenir el títol
            else:
                # ignora
                pass
        elif estat == "títol":
            if lin.startswith(".. enunciat:"):   # s'ha completat el títol
                estat = "enunciat"      # s'ha llegit el títol, ara toca l'enunciat
            else:   # forma part del títol
                titol += lin
        elif estat == "enunciat":
            if lin.startswith(".. resposta:"):  # s'ha finalitzat l'enunciat
                pes = lin.lstrip(".. resposta:").strip()
                if pes not in ('+', '-'):
                    print >> sys.stderr, "WARNING: resposta sense pes (lin %s)"%nlin
                estat = "resposta"      # s'està llegint una resposta
            else:
                enunciat += lin
        elif estat == "resposta":
            if lin.startswith(".. pregunta:"):  # s'han acabat les respostes
                respostes.append((resposta, pes))
                preguntes.append(Pregunta(titol, enunciat, respostes))
                estat = "títol"
                titol = ""
                enunciat = ""
                resposta = ""
                pes = ""
                respostes = []
            elif lin.startswith(".. resposta:"):    # s'ha llegit una altra resposta
                noupes = lin.lstrip(".. resposta:").strip()
                if noupes not in ('+', '-'):
                    print >> sys.stderr, "WARNING: resposta sense pes (lin %s)"%nlin
                respostes.append((resposta, pes))
                resposta = ""
                pes = noupes
            else:
                resposta += lin
    if estat == "resposta": # encara no s'ha guardat la darrera pregunta
        respostes.append((resposta, pes))
        preguntes.append(Pregunta(titol, enunciat, respostes))

    return preguntes
#
def mostra_preguntes(preguntes):
    """ mostra la llista de preguntes"""
    for i in range(len(preguntes)):
        p = preguntes[i]
        p.mostra_pregunta(i+1)
#
def mostra_titols(preguntes):
    """ mostra la llista de títols i pesos de les preguntes"""
    # mostra els títols de les respostes
    for i in range(len(preguntes)):
        p = preguntes[i]
        p.mostra_noms_respostes(i+1)
    print
    # mostra els pesos de les respostes
    for i in range(len(preguntes)):
        p = preguntes[i]
        p.mostra_pesos_respostes(i+1)
    print
#
def valida_parametres():
    """ valida els paràmetres de l'entrada.
        Valida que el nombre de versions sigui un enter de 1 a 28.
        Valida que s'hagi especificat un path de fitxer
        existent, llegible i amb extensió .quiz. 
        Mostra missatge d'error adequat pels paràmetres
        Retorna:
            None: si els paràmetres no són correctes
            fitxer: si els paràmetres són correctes
        """
    if len(sys.argv)<3:
        print >> sys.stderr, "Ús: %s numver nomfitxer.quiz [--force] [--noshuffle] [--showtitles]"%sys.argv[0]
        return None

    if not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        print >> sys.stderr, "Error: %s no és un nombre adequat"%sys.argv[1]
        return None

    numver=int(sys.argv[1])

    fitxer = sys.argv[2]
    base, ext = os.path.splitext(fitxer)
    if ext <> ".quiz":
        print >> sys.stderr, "Error: %s no és un fitxer .quiz"%fitxer
        return None

    if not os.path.isfile(fitxer):
        print >> sys.stderr, "Error: %s no és un fitxer vàlid"%fitxer
        return None

    force = False
    shuffle = True
    showtitles = False
    if len(sys.argv) >= 3:
        if "--force" in (sys.argv[2:]):
            force = True
            print >> sys.stderr, "WARNING: opció --force encara no implementada"
        if "--noshuffle" in (sys.argv[2:]):
            shuffle=False
        if "--showtitles" in (sys.argv[2:]):
            showtitles=True;

    outtext = composa_nom_text(fitxer)
    outsol  = composa_nom_solucions(fitxer)
    if (os.path.isfile(outtext) or os.path.isfile(outsol)) and not force:
        print >> sys.stderr, "Error: trobats %s o/i %s. Elimina'ls o fes servir l'opció --force"%(outtext, outsol)
        return None

    return numver, fitxer, shuffle, showtitles
#
def composa_nom_text(fitxer):
    """ retorna el nom del fitxer de sortida a generar amb les preguntes
    a partir del nom del fitxer d'entrada """
    base, _ = os.path.splitext(fitxer)
    return "%s.text.rst"
#
def composa_nom_solucions(fitxer):
    """ retorna el nom del fitxer de sortida a generar amb les solucions
    a partir del nom del fitxer d'entrada """
    base, _ = os.path.splitext(fitxer)
    return "%s.solucions.rst"
#
def generaVersions(numver, preguntes, shuffle, showtitles):
    for i in range(numver): 
        if shuffle: 
            barreja(preguntes)
        if showtitles:
            mostra_titols(preguntes)
        mostra_preguntes(preguntes)
#
def main():
    validacio = valida_parametres()
    if validacio == None:
        return 1
    numver, fitxer, shuffle, showtitles = validacio
    f = open(fitxer)
    preguntes = processa_continguts(f)
    f.close()
    generaVersions(numver, preguntes, shuffle, showtitles)
    return 0
#
if __name__=="__main__":
    sys.exit(main())

