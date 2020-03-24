#!/bin/sh

proxy=${proxy}
arch=${arch}
dout=${dout}
outpath=${outpath}
mva=${mva}
chan=${chan}
pt=${pt}
nmax=${nmax}
testt=${testt}
year=${year}

export X509_USER_PROXY=${proxy}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${dout}/../../
export SCRAM_ARCH=${arch}
eval `scramv1 runtime -sh`
cd -

input="/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/${testt}.root"

echo "Executing python roc.py --output ${outpath} --pt ${pt} --mva TTH,TZQ,${mva} --chan ${chan} --nmax ${nmax} --input ${input} --year ${year}"
time python ${dout}/./roc.py --output "${outpath}" --pt "${pt}" --mva "TTH,TZQ,${mva}" --chan "${chan}" --nmax "${nmax}" --input "${input}" --year "${year}"
