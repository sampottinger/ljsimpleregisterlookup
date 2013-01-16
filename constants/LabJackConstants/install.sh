#! /bin/sh
#
# Installs the LabJack constant files for Linux and Mac. Run with sudo.
#

DESTINATION=/usr/local/share
TARGET=LabJack
OS=`uname -s`

if [ "$OS" != 'Linux' ] && [ "$OS" != 'Darwin' ]; then
	echo "Unknown operating system $OS"
	exit 1
fi

echo "Installing LabJack constant files..."

test -z $DESTINATION || mkdir -p $DESTINATION
cp -R $TARGET $DESTINATION

echo "Done"

exit 0
