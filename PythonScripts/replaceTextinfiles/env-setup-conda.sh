#! /bin/bash
#  * ******************************************************************************
#  *                                     env-setup-conda.sh
#  *  BigDataGrapes
#  *  Copyright © INRA 2018
#  *  Creation date:  20 December, 2018
#  *  Contact: arnaud.charleroy@inra.fr, pascal.neveu@inra.fr
#  * ******************************************************************************

nameEnv=replacetext-env

conda create --name ${nameEnv} python=3.5 --yes
conda install --name ${nameEnv} pip

# using pip inside our environment : conda doesn't handle well the dependencies/version without gpu
# pip reference here the envornment version, so don't use pip3
source activate ${nameEnv}
pip install pyyaml
