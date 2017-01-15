#! /bin/sh
echo "Clean up of java classes and temporary files (*~)"
find . -type f -name '*.class' -delete
find . -type f -name '*~' -delete
