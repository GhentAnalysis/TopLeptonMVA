#!/bin/bash

export X509_USER_PROXY=/user/kskovpen/proxy/x509up_u20657
echo "Start: $(/bin/date)"
echo "User: $(/usr/bin/id)"
echo "Node: $(/bin/hostname)"
echo "CPUs: $(/bin/nproc)"
echo "Directory: $(/bin/pwd)"
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /storage_mnt/storage/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost
export SCRAM_ARCH=slc7_amd64_gcc820
eval `scramv1 runtime -sh`
source /user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/setup.sh
cd /storage_mnt/storage/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/jobs/PUPv1_elec_2017//n_estimators-100__max_depth-3__eta-0.1/
python3 /storage_mnt/storage/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/./train.py --path /storage_mnt/storage/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/jobs/PUPv1_elec_2017//n_estimators-100__max_depth-3__eta-0.1/ --version PUPv1 --objective logistic --definition n_estimators-100__max_depth-3__eta-0.1 --chan elec --cv 
