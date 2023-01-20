#!/bin/bash

VERSION="1.8.2"

echo "Download Vorpalite..."
wget https://github.com/BrunoLevy/geogram/releases/download/v1.8.2/geogram_$VERSION.tar.gz

echo "Verify hash..."
RIGHT_SUM="0abf9745013cd87926285f5195af5b4e"

if [ "$RIGHT_SUM" != "$(md5sum geogram_$VERSION.tar.gz | cut -d " " -f 1)" ]; then
    echo "Not the right hash"
    exit
fi

echo "Unzip..."
tar -xf geogram_$VERSION.tar.gz

echo "Build..."
cd geogram_$VERSION
cmake .
make
