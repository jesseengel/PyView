#!/bin/bash

set -ex

orig_dir=$(pwd)
tmp_dir=$(mktemp -d -t pyview-XXXX)
git clone https://github.com/jesseengel/PyView.git $tmp_dir
cd $tmp_dir

python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/* --verbose

cd $orig_dir
rm -rf $tmp_dir
