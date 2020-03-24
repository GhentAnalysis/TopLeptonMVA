#!/bin/sh

proxy=${proxy}
arch=${arch}
dout=${dout}
outname=${outname}
definition=${definition}
mva=${mva}
chan=${chan}
year=${year}

export X509_USER_PROXY=${proxy}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${dout}/../../
export SCRAM_ARCH=${arch}
eval `scramv1 runtime -sh`
cd -

echo "Executing python train.py --path ${outname} --definition ${definition} --mva ${mva} --chan ${chan} --input train_${year}.root"
time python ${dout}/./train.py --path "${outname}" --definition "${definition}" --mva "${mva}" --chan "${chan}" --input "train_${year}.root"
