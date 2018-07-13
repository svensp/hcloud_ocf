#!/bin/sh

if [ -d build ] ; then
	rm -Rf build
fi

DIR=$(pwd)

mkdir ${DIR}/build

cp -r -L ${DIR}/floating_ip ${DIR}/build/floating_ip_build
cd "${DIR}/build/floating_ip_build"
zip "${DIR}/build/floating_ip.zip" *
echo '#!/usr/bin/env python3' | cat - "${DIR}/build/floating_ip.zip" > "${DIR}/build/floating_ip"
chmod +x  "${DIR}/build/floating_ip"

cp -r -L "${DIR}/stonith" "${DIR}/build/stonith_build"
cd "${DIR}/build/stonith_build"
zip "${DIR}/build/stonith.zip" *
echo '#!/usr/bin/env python3' | cat - "${DIR}/build/stonith.zip" > "${DIR}/build/stonith"
chmod +x  "${DIR}/build/stonith"

cd ${DIR}
