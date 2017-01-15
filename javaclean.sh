#! /bin/sh
echo "Clean up of java classes and temporary files (*~)"
echo "ctrl-c to abort"
read resposta
find . -type f -name '*.class' -delete
find . -type f -name '*~' -delete
