#!/usr/bin/env bash

rm function.zip
rm -rf package
mkdir package

pip install --target ./package requests beautifulsoup4

cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD

cd src
zip -g -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
