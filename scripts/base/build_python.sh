#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir python
cd python

curl -C - --location https://www.python.org/ftp/python/${PYTHON_VERSION_FULL}/Python-${PYTHON_VERSION_FULL}.tgz -o $DOWNLOADS_DIR/Python-${PYTHON_VERSION_FULL}.tgz


mkdir -p ${ASWF_INSTALL_PREFIX}/bin
echo "PATH=$PATH"

# Create script to allow use of system python
cat <<EOF > ${ASWF_INSTALL_PREFIX}/bin/run-with-system-python
#!/bin/sh
# Unsets all environment variables so that the system python can function normally
# To use, just prefix any command with run-with-system-python
unset PYTHONPATH
unset LIBRARY_PATH
unset PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/opt/rh/devtoolset-6/root/usr/lib64:/opt/rh/devtoolset-6/root/usr/lib
export PATH=/opt/rh/devtoolset-6/root/usr/bin:/opt/app-root/src/bin:/opt/rh/devtoolset-6/root/usr/bin/:/usr/sbin:/usr/bin:/sbin:/bin
exec "\$@"
EOF
chmod a+x ${ASWF_INSTALL_PREFIX}/bin/run-with-system-python

# Create a yum wrapper that uses the system python
cat <<EOF > ${ASWF_INSTALL_PREFIX}/bin/yum
#!/bin/sh
# This runs yum with system python
exec ${ASWF_INSTALL_PREFIX}/bin/run-with-system-python /usr/bin/yum "\$@"
EOF
chmod a+x ${ASWF_INSTALL_PREFIX}/bin/yum

tar xf $DOWNLOADS_DIR/Python-${PYTHON_VERSION_FULL}.tgz
cd Python-${PYTHON_VERSION_FULL}

# Ensure configure, build and install is done with no reference to ${ASWF_INSTALL_PREFIX} as this somehow messes up the system install
run-with-system-python ./configure \
    --prefix=${ASWF_INSTALL_PREFIX} \
    --enable-unicode=ucs4 \
    --enable-shared
run-with-system-python make -j$(nproc)

run-with-system-python make install

if [[ $PYTHON_VERSION == 3* ]]; then
    # Create symlink from python3 to python
    ln -s python3 ${ASWF_INSTALL_PREFIX}/bin/python
    export PIP=pip3
else
    export PIP=pip
fi

cd ../..
rm -rf python

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
rm get-pip.py

$PIP install \
    nose \
    coverage \
    docutils \
    epydoc \
    "numpy==${NUMPY_VERSION}"
