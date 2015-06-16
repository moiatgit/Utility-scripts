#! /bin/bash
# Script to convert .rst prepared for pelican to sphinx

function convert() {
    echo -n "Converting $1.."
    # remove linenos type
    sed -i 's/:linenos: inline/:linenos:/' "$1"
    sed -i 's/:linenos: table/:linenos:/' "$1"
    # remove default code-block
    sed -i 's/code-block:: default/code-block:: none/' "$1"
    # remove metadata
    rst_metadata.py -d --key updated "$1"
    rst_metadata.py -d --key date "$1"
    rst_metadata.py -d --key next_entry "$1"
    rst_metadata.py -d --key tags "$1"
    echo "Done"
}


for f in $*;
do
    if [ ! -f "$f" ]
    then
        echo "WARNING: not found file $f"
    else
        base=$(basename $f)
        extension="${base##*.}"
        name="${base%.*}"
        if [[ "$extension" == "rst" ]]
        then
            convert $f
        else
            echo "WARNING: ignored file $f"
        fi
    fi
done
