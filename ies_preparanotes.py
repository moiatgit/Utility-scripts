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
Prepara les notes a partir d'un csv al format requerit per ies_posanotes.py. 
Cal indicar el nom del fitxer d'origen i el de destinació en aquest ordre o bé fent
servir opcions. Altrament es farà servir l'entrada/sortida estàndard.
El csv d'entrada ha de contenir una fila d'informació amb els tags <i> i <n>, i 
opcionalment <c> i zero o més <e>. 
<i> Indica que la columna correspon a l'identificador de l'alumne al moodle. 
<n> Indica la nota (un valor numèric o "NP") que es col·locarà com a valoració.
<c> Indica que és un comentari.
<e> Indica el resultat d'una valoració parcial (pot ser o no numèrica). En cas que 
correspongui a un valor numèric amb decimals, es considerarà un màxim de dos decimals.
A continuació de la fila d'informació, ha de venir la fila de capçaleres que contindrà
a les columnes indicades pels tags, el títol de la columna. Només es considerarà
els títols per les entrades (<e>).
A continuació de la fila de capçaleres apareixerà una o més files amb els valors per a
cada alumne. Es considerarà que es finalitza quan la cel·la corresponent a l'identificador
de l'alumne no contingui un valor numèric o aquest sigui 0. S'ignorarà les files dels
alumnes que a Nota no tinguin un valor numèric o bé "NP".
La resta de les files del document seran ignorades.
"""
#
DELIMITADOR_DEFECTE="^"
#
def cnvint(v):
    """ si v correspon a un enter retorna el valor enter. Altrament retorna None """
    try:
        i = int(v)
    except ValueError:
        i = None
    return i
#
def tractanota(v):
    """ tracta la nota. 
        Si v correspon a un enter, retorna (int(v), v)
        Si v correspon a "NP", retorna (-1, v)
        Si v correspon a un valor decimal, retorna (int(v), tractapossibledecimal(v))
        Altrament retorna (None, v) """
    nota_num = cnvint(v)
    nota_str = v
    if nota_num == None:
        nota_num = tractapossibledecimal(v)
        if nota_num.upper() == "NP":
            nota_num = -1
        else:
            cf = cnvfloat(nota_num)
            if cf:
                nota_num = int(round(cf))
                nota_str = tractapossibledecimal(v)
            else:
                nota_num = None
    return nota_num, nota_str
#
def cnvfloat(v):
    """ si v correspon a un float retorna el valor float. Altrament retorna None """
    if v.count(',') == 1:
        v = v.replace(',', '.')
    try:
        f = float(v)
    except ValueError:
        f = None
    return f

def tractapossibledecimal(v):
    """ en cas que v sigui un valor numèric amb decimals, el formateja per que
        tingui un màxim de 2 decimals.
        És capaç d'acceptar decimals puntuats amb ',' i amb '.'
        """
    v = v.strip()
    cf = cnvfloat(v)
    if cf:
        v = ("%.2f"%cf).rstrip("0.")
    return v
#
def interpreta_entrada(fo):
    """ interpreta l'entrada. Retorna una llista de tuples amb els valors corresponents.
    La primera llista correspon a les capçaleres. La resta de les llistes contenen, 
        id_alumne
        nota_num    és la nota entera (arrodonida si cal i -1 si NP)
        nota_str    és la nota tal i com es rep (amb dos decimals com a màxim)
        comentari ("" si no n'hi ha)
        llista de valors d'entrades (coincidirà amb les capçaleres)
    En cas de trobar error, mostrarà missatge per stderr i retornarà la llista buida.
    """
    entrada = csv.reader(fo)
    trobada_fila_inicial = False    # s'ha trobat ja la línia amb la info de composició?
    trobats_titols = False          # s'han trobat ja les capçaleres?
    #
    pos_id = -1                     # columna de l'identificador d'alumne
    pos_nota = -1                   # columna de la nota
    pos_comentaris = -1             # columna dels comentaris
    pos_entrades = []               # llista de columnes de les entrades
    #
    resultat = []                   # llista amb els resultats.
    #
    for fila in entrada:
        if trobada_fila_inicial:
            if trobats_titols:
                idalumne = cnvint(fila[pos_id])
                if idalumne == None:
                    break           # s'ha arribat al final de la llista d'alumnes
                nota_num, nota_str = tractanota(fila[pos_nota])
                if nota_num == None:
                    continue        # alumne sense valorar
                filaalumne = [ idalumne, nota_num, nota_str ]
                if pos_comentaris >= 0:
                    filaalumne.append(fila[pos_comentaris])
                for pos in pos_entrades:
                    val = tractapossibledecimal(fila[pos]) 
                    filaalumne.append(val)
                resultat.append(filaalumne)
            else:
                titols = [ "id", "final", "nota", "comentaris"]
                for pos in pos_entrades:
                    titols.append(fila[pos])
                trobats_titols = True
                resultat.append(titols)
        elif "<i>" in fila and "<n>" in fila:
            trobada_fila_inicial = True
            pos_id = fila.index("<i>")
            pos_nota = fila.index("<n>")
            if "<c>" in fila:
                pos_comentaris = fila.index("<c>")
            i = 0
            pos_entrades = []
            while "<e>" in fila[i:]:
                i = fila.index("<e>", i)
                pos_entrades.append(i)
                i += 1
        else:
            pass    # ignora línies anteriors a la fila inicial
    return resultat
#
def formateja_entrada(valoracions):
    """ formateja les valoracions.
    Converteix els comentaris (si hi són) i les entrades de cada línia de entrada
    en un snippet html a col·locar com a comentari a la retroacció de Moodle.
    El format de sortida és:
        <table 
    """
    titols = valoracions[0]
    titol_comentari = '<table border="1" style="border-width:1px;border-style:none">' + \
                      '<tr><td><b>Nota</b></td>'
    for i in range(4, len(titols)):
        titol_comentari += '<td><b>%s</b></td>'%titols[i]
    titol_comentari += '</tr><tr><td align="center">%s</td>'
    for i in range(4, len(titols)):
        titol_comentari += '<td align="center">%s</td>'
    titol_comentari += "</tr></table>"
    #
    formatades = []
    for valalumne in valoracions[1:]:
        notesalumne = titol_comentari%tuple([valalumne[2]] + valalumne[4:])
        if valalumne[3]<>"":
            notesalumne += '<p><b>Comentaris:</b> %s</p>'%valalumne[3]
        formatades.append([valalumne[0], valalumne[1], notesalumne])
    return formatades
#
def prepara_csv(fo, fd, delimitador):
    """ prepara el contingut del fitxer fo i el deixa en fd fent servir el delimitador """
    entrada = interpreta_entrada(fo)
    if entrada == []:
        print >> sys.stderr, "ERROR: l'entrada no es pot interpretar correctament"
        return False
    formatades = formateja_entrada(entrada)
    sortida = csv.writer(fd, delimiter=delimitador)
    for f in formatades:
        sortida.writerow(f)
    return True
#
def obte_arguments():
    """ retorna la tupla 
        (sourcefilename,            nom del fitxer d'entrada
         destinationfilename,       nom del fitxer de sortida
         delimitator)               delimitador
    """
    p = optparse.OptionParser(description = DESCR_FUNCIONAMENT, version="1.0")
    p.add_option("-f", "--fromfile", action="store", help=u"Fitxer que conté les notes en format csv", nargs=1, dest="source")
    p.add_option("-t", "--tofile", action="store", help=u"Fitxer on deixar les notes formatades", nargs=1, dest="destination")
    p.add_option("-d", "--delimitador", action="store", help=u"Caràcter delimitador del fitxer de notes. Per defecte '^'", nargs=1, dest="delimitador", default="^")
    opcions, arguments = p.parse_args()
    #
    if opcions.source:
        sourcefilename = opcions.source
    elif len(arguments) > 0:
        sourcefilename = arguments[0]
    else:
        sourcefilename = None
    #
    if opcions.destination:
        destinationfilename = opcions.destination
    elif len(arguments) > 1:
        destinationfilename = arguments[1]
    else:
        destinationfilename = None
    #
    if opcions.delimitador:
        delimitator = opcions.delimitador
        if len(delimitator)<1:
            delimitator = DELIMITADOR_DEFECTE
        else:
            delimitator = delimitator[0]        # només es queda amb el primer caràcter
    else:
        delimitator = DELIMITADOR_DEFECTE
    return sourcefilename, destinationfilename, delimitator
#
def main():
    sourcefilename, destinationfilename, delimitador = obte_arguments()
    #
    source = open(sourcefilename, "r") if sourcefilename else sys.stdin
    destination = open(destinationfilename, "w") if destinationfilename else sys.stdout
    #
    if not prepara_csv(source, destination, delimitador):
       return 1 
    return 0
#
if __name__=="__main__":
    sys.exit(main())
