#! /bin/sh
echo "Clean up of vim temporary files (*~)"
find . -type f -name '*~' -delete
