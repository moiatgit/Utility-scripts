#! /bin/bash
# Descarrega un site sencer a partir de la URL indicada
echo "Aquest script descarrega tot un lloc web a partir del directori actual"
echo "Està pensat per descarregar documentació com ara l'API de Java"
if [[ -z "$1" ]]
then
    echo "usage: $0 «url»"
else
    wget -nH -k -m -p -L -np $1
fi
