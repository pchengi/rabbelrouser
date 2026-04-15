#!/bin/bash
git submodule init
git submodule update
cd sv-eng|| exit -1
python dictops.py -u
python dictops.py -x
bash gensaolwords.sh
python dictops.py -a -i saol14.words --source saol14|tee sauladds.out
