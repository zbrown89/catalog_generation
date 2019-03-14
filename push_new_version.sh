#!/bin/bash

python_version=`python -c "import sys; print(\"{}.{}\".format(sys.version_info[0], sys.version_info[1]))"`
# only update the version number for python 3.6 build
if [ $python_version == "3.6" ]; then 
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
    git clone https://${GH_TOKEN}@github.com/DESI-UR/catalog_generation.git -b development catgen-dev
    cd catgen-dev
    python py/paramock/versioning.py
    git commit -m '[skip travis] after the successful build, updating the version number' py/paramock/_version.py
    git push
fi
