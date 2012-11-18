#! /usr/bin/python
# encoding: utf-8
#
# Fichero:  formatanotes.py
# Autor:    moises
# Fecha:    20101028
# Descr:    Formata les notes per a ser tractades pel programa posanotes.py
#           Les notes han d'estar incloses a un fitxer .csv amb el delimitador ^
#           El format requerit és el següent
# fila          columna             contingut
#   0, 1                            ignorat
#   2            ?                  pesos dels criteris de correcció (coincideix amb capçalera criteris de correcció)
#   3           "#"                 capçalera id alumne
#   3           "Total"             capçalera nota
#   3           "Comentaris"        capçalera de comentaris
#   3           a continuació       capçalera dels criteris de correcció (fins el primer blanc)
#   4+          segons capçaleres   valors per a cada alumne (fins primer '#' en blanc)
#
#           El format de sortida és:
#               idalumne, nota, comentaris
#           On els comentaris són una composició en html dels valors per l'alumne als criteris.
#           La resta d'informació del full és ignorada
#
import csv
import optparse
import os
import sys
#
_DELIMITADOR_ORIGEN = '^'           # marca de delimitació origen
_DELIMITADOR_DESTINACIO = '^'       # marca de delimitació destinació
#
_CAP_ID     = '#'                   # capçalera d'identificador
_CAP_TOTAL  = 'Total'               # capçalera de total de nota
_CAP_COMENT = 'Comentaris'          # capçalera de comentaris
#
def formata(reader, writer):
    """ formata el fitxer d'origen i el guarda a destinacio """
    # ignora primeres dues files
    for i in range(2): reader.next()
    # obté les files desitjades
    filapesos  = reader.next()      # fila amb els pesos dels criteris (cal esperar per saber les columnes)
    filacap    = reader.next()      # fila amb les capçaleres
    filesnotes = list()             # files amb les notes
    for r in reader:
        if r[0]=="": break
        filesnotes.append(r)
    # processa les capçaleres
    colid     = -1
    coltotal  = -1
    colcoment = -1
    for i in range(len(filacap)):
        if filacap[i]==_CAP_ID:
            colid = i
        elif filacap[i]==_CAP_TOTAL:
            coltotal = i
        elif filacap[i]==_CAP_COMENT:
            colcoment = i
            break
    if colid < 0 or coltotal < 0 or colcoment < 0:
        print >> sys.stderr, "Error: format incorrecte del fitxer d'origen"
        return -1
    capcriteris = dict()            # capçaleres de criteris {col: (criteri, pes)}
    iniciatCriteris = False         # es considera que inicien criteris a partir del primer
                                    # no blanc després dels comentaris
    for i in range(colcoment+1, len(filacap)):
        if filacap[i]=='':
            if iniciatCriteris:
                break               # es considera finalitzats els criteris a partir del
                                    # primer blanc després d'iniciats els criteris
            else:
                iniciatCriteris = True
        else:
            capcriteris[i]=(filacap[i], filapesos[i])
    #
    notesalumnes = dict()           # notes dels criteris per cada alumne {idalumne: (nota, comentari, {criteris})}
    for l in filesnotes:
        try:
            idalumne = int(l[colid])                    # conversió del id alumne
                                                        # a enter per eliminar el caràcter 0
                                                        # inicial
        except:
            print >>sys.stderr, "Error: el id de l'alumne %s no és numèric"%l[colid]
            return -1
        try:
            nota =  float(l[coltotal].replace(',', '.')) # conversió de nota
                                                        # en str amb decimal 
                                                        # separat per ',' a
                                                        # float
        except:
            print >>sys.stderr, "Error: la nota %s no és numèrica"%l[coltotal]
            return -1
        comentari = l[colcoment]
        notescriteris = dict()      # {columna: valoració de l'alumne}
        for c in capcriteris:
            notescriteris[c]=l[c]
        notesalumnes[idalumne]=(nota, comentari, notescriteris)
    #    
    # composició de l'html
    resultat = list()               # llista on es deixarà el resultat final:
                                    # [(idalumne, nota100, anotacio)]
    for idalumne in notesalumnes:
        nota100       = int(round(notesalumnes[idalumne][0]*10))    # passa a base 100
        comentari     = notesalumnes[idalumne][1]
        notescriteris = notesalumnes[idalumne][2]
        #
        # comprovació de no presentat -> cap valoració
        nopresentat = False
        if nota100 == 0:
            nopresentat = True
            for criteri in notescriteris:
                if not notescriteris[criteri]=="":
                    nopresentat = False
                    break
        anotacio = "" if comentari=="" else "<p><i>Comentaris</i>: %s</p>"%comentari
        if nopresentat:
            resultat.append((idalumne, -1, anotacio))
        else:        
            anotacio += "<table><tr><td><i>Criteri</i></td><td><i>Pes</i></td><td><i>Valoració</i></td></tr>"
            for criteri in notescriteris:   # el criteri correspon a la columna en que apareix
                descrcriteri = capcriteris[criteri][0]
                pescriteri   = capcriteris[criteri][1]
                valoracio    = "&nbsp;" if notescriteris[criteri]=="" else notescriteris[criteri]
                anotacio += "<tr><td>%s</td><td>%s</td><td><b>%s</b></td></tr>"%(descrcriteri, pescriteri, valoracio)
            anotacio += "</tr></table>"
            resultat.append((idalumne, nota100, anotacio))
    # escriu el resultat al writer
    writer.writerows(resultat)
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
        return -1
    if not opcions.destinacio:
        print >> sys.stderr, "Error: Cal indicar el fitxer destinació"
        return -1
    #
    if os.path.exists(opcions.destinacio) and not opcions.force:
        print >> sys.stderr, "Error: ja existeix el fitxer de destinació. --force per sobreescriure"
        return -1
    #
    try:
        forigen = open(opcions.origen)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer d'origen"
        return -1
    #
    try:
        reader = csv.reader(forigen, delimiter=_DELIMITADOR_ORIGEN)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer d'origen com a csv"
        return -1
    #
    try:
        fdestinacio = open(opcions.destinacio, "w")
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer de destinació"
        return -1
    #
    try:
        writer = csv.writer(fdestinacio, delimiter=_DELIMITADOR_DESTINACIO)
    except:
        print >> sys.stderr, "Error: no es pot obrir el fitxer de destinació com a csv"
        return -1
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
