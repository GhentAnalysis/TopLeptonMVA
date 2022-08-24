#!/bin/env python

import os, sys, ROOT

f = ROOT.TFile("output.root")
tr = f.Get("muonAll")
for ev in tr:
    print ev.leptonMvaTOPULTOPv1, ev.pt, ev.eta, ev.trackMultClosestJet, ev.miniIso, \
    ev.miniIsoNeutral, ev.pTRel, ev.ptRatio, ev.sip3d, ev.dxylog, ev.dzlog
#    tr.miniIsoCharged[0] = tr.miniIsoChargedDs[i]
#    tr.miniIsoNeutral[0] = tr.miniIsoNeutralDs[i]
#    tr.missHits[0] = tr.missHitsDs[i]
#    tr.pTRel[0] = tr.pTRelDs[i]
#    tr.ptRatio[0] = tr.ptRatioDs[i]
#    tr.relIso[0] = tr.relIsoDs[i]
#    tr.sip3d[0] = tr.sip3dDs[i]
#    tr.dxy[0] = tr.dxyDs[i]
#    tr.dxylog[0] = tr.dxylogDs[i]
#    tr.dz[0] = tr.dzDs[i]
#    tr.dzlog[0] = tr.dzlogDs[i]
#    tr.drMin[0] = tr.drMinDs[i]
#    tr.POGMedium[0] = tr.POGMediumDs[i]
#    tr.bTagDeepJetClosestJet[0] = tr.bTagDeepJetClosestJetDs[i]
#    tr.segmentCompatibility[0] = tr.segmentCompatibilityDs[i]
#    tr.mvaIdFall17v2noIso[0] = tr.mvaIdFall17v2noIsoDs[i]
    
    
