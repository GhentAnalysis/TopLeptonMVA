#!/bin/bash

export LD_LIBRARY_PATH=/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/cpp/xgboost/lib:$LD_LIBRARY_PATH

./test
