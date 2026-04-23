#!/bin/bash

###### CONFIGURATIONS ######
VM_ID=100
IMAGE_PATH="DC1-1.qcow2"
STORAGE="RAID"
############################

printf "Import virtual disk image '%s' to %s for VM (ID=%d)..\n" \
	$IMAGE_PATH $STORAGE $VM_ID

qm importdisk $VM_ID $IMAGE_PATH $STORAGE --format qcow2
