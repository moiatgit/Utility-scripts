#! /bin/bash
echo "Genera la versió odt d'un fitxer rst"
if [[ "$1" == "" ]];
then
    echo "Cal indicar un fitxer .rst"
    exit 1
fi
src=$1
path=$(dirname $src)
name=$(basename $src)
extension="${name##*.}"
namesrc="${name%.*}"

# troba el fitxer d'estils al directori on es troba aquest script
basepath=$(dirname $0)
stylepath="$basepath/styles.odt"
if [ ! -f "$stylepath" ];
then
    echo "No trobo el fitxer $stylepath"
    exit 1
fi

# Comprova l'entrada
if [[ "$extension" != "rst" ]];
then
    echo "El document no sembla ser un .rst"
    exit 1
fi

if [ ! -f "$src" ];
then
    echo "El document no sembla existir o ser un fitxer"
    exit 1
fi

# genera la sortida
nomdest="$path/$namesrc.odt"
rst2odt.py --stylesheet=$stylepath --no-sections $src $nomdest


