#!/bin/bash
#
#For Ubuntu 20.04
#
#

#Startup 
apt-get -y update
apt-get -y install linux-headers-$(uname -r)

#Dependencies
apt-get -y install xorg
apt-get -y install openbox
apt-get -y install libglu1-mesa-dev freeglut3-dev mesa-common-dev
