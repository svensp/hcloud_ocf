#!/bin/sh

if [ -d build ] ; then
	sudo rm -Rf build
fi

DIR=$(pwd)

mkdir ${DIR}/build

FLOATING_IP_DIR="${DIR}/build/floating_ip_build"
cp -r -L ${DIR}/floating_ip "${FLOATING_IP_DIR}"
cd "${DIR}/build/floating_ip_build"
sudo python3 -m pip install hetznercloud --target .
sudo python3 -m pip install ifaddr --upgrade --target .
python3 -m zipapp -p '/usr/bin/env python3' --output "${DIR}/build/floating_ip" "${FLOATING_IP_DIR}"

STONITH_DIR="${DIR}/build/stonith_build"
cp -r -L "${DIR}/stonith" "${STONITH_DIR}"
cd "${DIR}/build/stonith_build"
sudo python3 -m pip install hetznercloud --target .
sudo python3 -m pip install ifaddr --upgrade --target .
python3 -m zipapp -p '/usr/bin/env python3' --output "${DIR}/build/hetzner_cloud" "${STONITH_DIR}"

cd ${DIR}
