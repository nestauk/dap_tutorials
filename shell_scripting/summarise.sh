#!/usr/bin/env bash

set -e
set -o pipefail

usage() {
 cat << EOF
Summarise the files in a directory

Options:
   -i <path>   --input-directory <path>   The input directory
   -h          --help                     Prints this help message and exits

EOF
}

while [ -n "$1" ]; do
  case $1 in
  -i | --input-directory)
    shift
    IN_DIR=$1
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo -e "Unknown option $1...\n"
    usage
    exit 1
    ;;
  esac
  shift
done

if [ -z "$IN_DIR" ]; then
  echo "Please provide an input directory."
  usage
  exit 1
fi

for FILE in $IN_DIR/*; do
  [ -f "$FILE" ] || break
  BYTES=$(wc -c < "$FILE")
  echo "$(file $FILE) - has: $BYTES bytes"
done
