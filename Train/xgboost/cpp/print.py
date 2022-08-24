#!/bin/env python3

import sys
import ROOT
import xgboost as xgb
import pandas as pd

f = ROOT.TFile('/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/jobs_train_UL17_splitfine/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2017-v2_UL17/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2017-v2_UL17_1.root')
tr = f.Get('muonPrompt')
varall = ["pt", "eta", "trackMultClosestJet", "miniIsoCharged", "miniIsoNeutral", "pTRel", \
"ptRatio", "relIso", "bTagDeepJetClosestJet", "sip3d", "dxylog", "dzlog", "segmentCompatibility", "mvaIdFall17v2noIso", \
"leptonMvaTOPULTOPv1", "leptonMvaTOPULTOPv2", "missHits"]
data = {}
for iev, ev in enumerate(tr):
    for v in varall:
        var = eval('ev.'+v)
        data[v] = var
        print(v+'='+str(var))
    if iev >= 0: break

var = {}
var['elecv1'] = ["pt", "eta", "trackMultClosestJet", "miniIsoCharged", "miniIsoNeutral", "pTRel", \
"ptRatio", "relIso", "bTagDeepJetClosestJet", "sip3d", "dxylog", "dzlog", "mvaIdFall17v2noIso"]
var['muonv1'] = ["pt", "eta", "trackMultClosestJet", "miniIsoCharged", "miniIsoNeutral", "pTRel", \
"ptRatio", "relIso", "bTagDeepJetClosestJet", "sip3d", "dxylog", "dzlog", "segmentCompatibility"]
vard = var['muonv1']
mod = xgb.Booster()
mod.load_model('../weights/TOP_v1_muon_2017/n_estimators-2000__max_depth-4__eta-0.1__gamma-5__min_child_weight-500/xgb.bin')
df = pd.DataFrame(\
columns=vard, \
data=[[data[v] for v in vard]])
x = xgb.DMatrix(df, feature_names=vard)
res = mod.predict(x)
print(res)
