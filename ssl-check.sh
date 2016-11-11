#!/bin/bash
# Author: fkolacek@redhat.com
# Description: Check modules of key,csr and pem files
# Version: 1.0

set -e

OPENSSL=$(which openssl 2>/dev/null)
FQDN="$1"

[ -z "${OPENSSL}" ] && { echo "[!] Please install openssl package!"; exit 1; }
[ -z "${FQDN}" ] && { echo "[!] Usage $0 [COMMON_NAME]"; exit 2; }

pem=$(openssl x509 -noout -modulus -in ${FQDN}.pem | openssl md5)
key=$(openssl rsa -noout -modulus -in ${FQDN}.key | openssl md5)
csr=$(openssl req -noout -modulus -in ${FQDN}.csr | openssl md5)

echo "[*] Checking module for ${FQDN}"
echo " - PEM ${FQDN}.pem ${pem}"
echo " - KEY ${FQDN}.key ${pem}"
echo " - CSR ${FQDN}.csr ${pem}"

if [ "${pem}" == "${key}" ] && [ "${pem}" == "${csr}" ]; then
  echo "[*] Module is the same!"
  exit 0
else
  echo "[!] Module is not the same!"
  exit 1
fi
