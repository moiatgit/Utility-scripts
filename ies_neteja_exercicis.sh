#! /bin/sh
# neteja els fitxers amb determinades extensions a partir del CWD
# 
extensions="zip tar.gz tar rar class"
echo "Neteja els fitxers d'exercicis a partir del directori actual"
echo "S'eliminaran tots els fitxers amb extensió: $extensions"
echo "Prem c + <ENTER> per continuar"
read resposta
if [ "$resposta" == "c" ]
then
    for e in $extensions
    do
        find . -name *.$e -exec rm -v \{\} \;
    done
else
    echo "No s'ha eliminat cap fitxer"
fi
