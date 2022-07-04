#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# Fichero:  cerca_iguals.py
# Autor:    moises
# Fecha:    20070823
# Descr:    Compara tots els fitxers a partir del directori actual (incloent subdirectoris)
#           Escriu per sortida estandard la llista dels fitxers amb mateix contingut en parells separats per |
#           Escriu la llista de directoris que contenen algun fitxer repetit, amb el % de repetits que conté
# Ús:       Des del directori a comparar, executar el programa

import os
import filecmp


dicM = {}   # diccionari amb clau la mida dels fitxers i valor la llista de fitxers de mateixa mida
dicF = {}   # diccionari amb clau el nom d'un fitxer i valor la llista de fitxers amb mateix contingut
dicD = {}   # diccionari amb clau el nom d'un directori i valor el nombre de fitxers que conté trobats repetits
nf   = 0    # nombre de fitxers tractats
mt   = 0    # mida total dels fitxers tractats
mr   = 0    # mida total dels fitxers repetits


def compara_fitxer_lst(f, lst):
    """ compara f amb els fitxers de lst.
        Retorna el primer fitxer que sigui igual, "" si no n'hi ha cap """
    res = ""
    for cf in lst:
        if filecmp.cmp(f, cf):
            fd = open(f, 'rb')
            cfd = open(cf, 'rb')
            vf = fd.read(10000)        # només compara els primers 10Kb
            vcf = cfd.read(10000)
            fd.close()
            cfd.close()
            if (vf == vcf):
                res = cf
                break
    return res

def carrega_fitxer(f):
    """ carrega el fitxer f als diccionaris de fitxers """
    global dicM
    global dicF
    global dicD
    global totalbr
    global nf
    global mt
    global mr
    nf += 1
    mida = os.stat(f)[6]
    mt += mida
    if mida in dicM:
        feq = compara_fitxer_lst(f, dicM[mida])
        if feq == "":       # no hi ha cap fitxer igual
            dicM[mida].append(f)
        else:               # hi ha un fitxer igual
            mr += mida
            if feq in dicF:   # hi ha més d'un fitxer igual
                registra_repetit_a_directori(os.path.dirname(f))
                dicF[feq].append(f)
            else:                   # és el primer igual
                registra_repetit_a_directori(os.path.dirname(feq))
                registra_repetit_a_directori(os.path.dirname(f))
                dicF[feq]=[f]
    else:
        dicM[mida]=[f]

def carrega_fitxers(d):
    """ carrega els fitxers del directori d als diccionaris de fitxers """
    print("Carregant directory %s" % d)
    for f in os.listdir(d):
        fc = os.path.join(d,f)
        if os.path.isdir(fc):
            carrega_fitxers(fc)
        elif os.path.isfile(fc) and not os.path.islink(fc):
            carrega_fitxer(fc)

def registra_repetit_a_directori(d):
    """ registra un nou repetit al directori d """
    global dicD
    if d in dicD:     # ja tenia repetits
        dicD[d]=dicD[d]+1
    else:
        dicD[d]=1

def mostra_iguals():
    """ mostra la llista de fitxers que s'han trobat iguals """
    global dicF
    for f in dicF.keys():
        print("equals %s | %s" % (f, " | ".join(dicF[f])))

def mostra_dir_iguals():
    """ mostra els directoris que contenen fitxers repetits """
    global dicD
    for d in dicD:
        #nfitxers = len([n for n in os.listdir(d) if os.path.isfile(n)])   # compta el nombre total de fitxers al directori
        nfitxers = len(os.listdir(d))
        percent = 0 if nfitxers == 0 else (100.0 * dicD[d] / nfitxers)
        print(d, "%s repetits de %s fitxers = %1.1f%%" % (dicD[d], nfitxers, percent))

def mostra_resum():
    """ mostra un resum estadistic """
    global nf
    global mt
    global mr
    print("Nombre total de fitxers tractats: %s" % nf)
    print("Mida total dels fitxers tractats: %s" % mt)
    print("Mida total dels fitxers repetits: %s (%1.2f%%)" % (mr, (100.0 * mr/mt)))

carrega_fitxers(os.getcwd())
print("===============================")
mostra_iguals()
print("===============================")
mostra_dir_iguals()
print("===============================")
mostra_resum()
