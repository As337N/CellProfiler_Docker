#!/bin/bash

#set -e # El script fallara si hay un error

source /workspace/variables.env

#Corremos el py script para generar el CSV con el que alimentar LoadFile
python3 "$SCRIPT_PY" "$PATH_IMAGES" "$CP_WORKSPACE" "$CSV_FILE" 1

echo "Python script: $SCRIPT_PY has been successfully runned."

#Modificamos los placeholders del template cpipeline y guardamos el nuevo cpipeline que ejecutaremos
if [ ! -f "$TEMPLATE_CPPIPE" ]; then
    echo "No file with the .cppipe extension was found in the folder."
    exit 1
fi

sed "s|INPUT_PATH_CSV|${CP_WORKSPACE}|g" "$TEMPLATE_CPPIPE" | \
sed "s|SAVING_OUTPUT_PATH|${PATH_OUTPUT}|g" | \
sed "s|INPUT_PATH_IMAGES|${PATH_IMAGES}|g" > "$CPPIPE"

echo "File: $CPPIPE has been successfully created."

cellprofiler -c -r \
  --data-file "$CP_WORKSPACE/$CSV_FILE" \
  -o "$PATH_OUTPUT" \
  -p "$CPPIPE" \
  -i "$PATH_IMAGES"

echo "CellProfiler pipeline: $CPPIPE has been successfully runned."