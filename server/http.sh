#!/bin/bash
args=$*
cd /openmidas/server/images
python3 -m http.server $args