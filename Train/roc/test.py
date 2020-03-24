#! /usr/bin/env python

import os
import sys
import math
from array import array
import ROOT

weight, pt, eta, etaAbs, trackMultClosestJet, miniIsoCharged, miniIsoNeutral, \
pTRel, ptRatio, relIso, sip3d, dxy, dxylog, dz, dzlog, \
bTagDeepCSVClosestJet, bTagDeepJetClosestJet, mvaIdSummer16GP, segmentCompatibility, mvaIdFall17v2noIso, \
= (array( 'f',  [0.]) for _ in range(20))
    
ROOT.TMVA.Tools.Instance()
ROOT.TMVA.PyMethodBase.PyInitialize()

tmva = ROOT.TMVA.Reader("!Color:!Silent")
                    
tmva.AddVariable('dxylog', dxylog)
tmva.AddVariable('miniIsoCharged', miniIsoCharged)
tmva.AddVariable('miniIsoNeutral', miniIsoNeutral)
tmva.AddVariable('pTRel', pTRel)
tmva.AddVariable('sip3d', sip3d)
#tmva.AddVariable('mvaIdFall17v2noIso', mvaIdFall17v2noIso)
tmva.AddVariable('segmentCompatibility', segmentCompatibility)
tmva.AddVariable('ptRatio', ptRatio)
tmva.AddVariable('bTagDeepJetClosestJet', bTagDeepJetClosestJet)
tmva.AddVariable('pt', pt)
tmva.AddVariable('trackMultClosestJet', trackMultClosestJet)
tmva.AddVariable('etaAbs', etaAbs)
tmva.AddVariable('dzlog', dzlog)
tmva.AddVariable('relIso', relIso)

hyp = 'cuts200_depth4_trees1000_shrinkage0p1'
year = '2016'
#tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/elec_TOP_'+year+'/'+hyp+'/dataset/weights/TMVAClassification_BDTG_'+hyp+'_elec.weights.xml')
tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/muon_TOP_'+year+'/'+hyp+'/dataset/weights/TMVAClassification_BDTG_'+hyp+'_muon.weights.xml')

pt[0] = 8.01505
etaAbs[0] = math.fabs(0.0953984)
trackMultClosestJet[0] = 0
miniIsoCharged[0] = 0
miniIsoNeutral[0] = 0
pTRel[0] = 0
ptRatio[0] = 1
relIso[0] = 6.92435e-310
bTagDeepJetClosestJet[0] = 0
sip3d[0] = 3.06713
dxylog[0] = math.log(abs(0.00927156))
dzlog[0] = math.log(abs(-0.0106015))
#mvaIdFall17v2noIso[0] = 0.267195
segmentCompatibility[0] = 0.940197

pred = tmva.EvaluateMVA('BDTG method')

print pred
