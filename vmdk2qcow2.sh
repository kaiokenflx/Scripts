#!/bin/bash

if [[ $# -eq 0 ]]
then
	echo "Please provide the path to the VMDK source file!"
	exit 1
fi

VMDK="$1"

if [[ "$(qemu-img info $VMDK |grep 'file format:')" != *"vmdk"* ]]
then
	echo "Error: Failed to verify the provided source file"
	exit 1
fi

VMDK_BASENAME="${VMDK%.*}"
#QCOW_OUTPUT_FILENAME="$VMDK_BASENAME.qcow2"
QCOW_OUTPUT_FILENAME="Term.qcow2"

printf "Convert: '%s' => '%s'..\n" $VMDK $QCOW_OUTPUT_FILENAME

qemu-img convert -cpf vmdk -O qcow2 $VMDK $QCOW_OUTPUT_FILENAME

echo "Finished!"
