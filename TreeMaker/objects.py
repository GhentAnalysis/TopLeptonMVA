import os
import sys
import math
import utils as ut
import ROOT

import common as c
import functions as fun

def removeOverlap(Electrons, Muons):
    
    for eidx, e in enumerate(Electrons):
        
        eta = e.eta
        phi = e.phi
        
        passed, drMin, idxMin = fun.overlap(eta,phi,Muons,0.05)
        
        if not passed:
            del Electrons[eidx]
#            del Muons[idxMin]

class event():

    def __init__(self, ev):

        self.weight = ev.__getattr__("_weight")
    
class electron():

    idx = -1

    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
        self.type = 0

        self.pt = ev.__getattr__("_lPt")[idx]
        self.eta = ev.__getattr__("_lEta")[idx]
        self.etaabs = math.fabs(self.eta)
        self.phi = ev.__getattr__("_lPhi")[idx]
        self.E = ev.__getattr__("_lE")[idx]
        
        self.dxy = ev.__getattr__("_dxy")[idx]
        self.dz = ev.__getattr__("_dz")[idx]
        self.miniIso = ev.__getattr__("_miniIso")[idx]
        self.POGNoIsoLoose = ev.__getattr__("_lElectronPassMVAFall17NoIsoWPLoose")[idx]
        
        self.trackMultClosestJet = ev.__getattr__("_selectedTrackMult")[idx]
        self.miniIsoCharged = ev.__getattr__("_miniIsoCharged")[idx]
        self.miniIsoNeutral = ev.__getattr__("_miniIso")[idx] - self.miniIsoCharged
        self.pTRel = ev.__getattr__("_ptRel")[idx]
        self.ptRatio = min(ev.__getattr__("_ptRatio")[idx], 1.5)
        self.bTagDeepJetClosestJet = 0 if math.isnan(ev.__getattr__("_closestJetDeepFlavor")[idx]) else ev.__getattr__("_closestJetDeepFlavor")[idx]
        self.bTagDeepCSVClosestJet = 0 if math.isnan(ev.__getattr__("_closestJetDeepCsv")[idx]) else max(ev.__getattr__("_closestJetDeepCsv")[idx],0)
        self.sip3d = ev.__getattr__("_3dIPSig")[idx]
        self.dxylog = math.log(max(math.fabs(self.dxy),10E-20))
        self.dzlog = math.log(max(math.fabs(self.dz),10E-20))
        self.missHits = ev.__getattr__("_lElectronMissingHits")[idx]
        self.relIso = ev.__getattr__("_relIso")[idx]
        self.mvaIdFall17v2noIso = ev.__getattr__("_lElectronMvaFall17NoIso")[idx]
        self.mvaIdSummer16GP = ev.__getattr__("_lElectronMvaSummer16GP")[idx]
        self.segmentCompatibility = -777
        self.provenance = ev.__getattr__("_lProvenance")[idx]
        
        self.leptonMvaTTH = ev.__getattr__("_leptonMvaTTH")[idx]
        self.leptonMvaTZQ = ev.__getattr__("_leptonMvatZq")[idx]
        self.leptonMvaTOP = ev.__getattr__("_leptonMvaTOP")[idx]

        matchPdgId = ev.__getattr__("_lMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_lMomPdgId")[idx]        
        isPrompt = ev.__getattr__("_lIsPrompt")[idx]
        
        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.5)
        passIso = bool(self.miniIso < 0.4)
        passHits = bool(self.missHits < 2)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGNoIsoLoose == 1)
        passConv = bool(matchPdgId != 22)
        passProv = bool(self.provenance != 1)
        passTau = bool(abs(momPdgId) != 15)
    
        self.passed = (passPt and passEta and passIPSig and passDxy and passDz and passIso and passHits)
        
        self.isPrompt = (isPrompt and bool(abs(matchPdgId) == 11) and passConv and passProv and passTau)
        self.isNonPrompt = (not isPrompt)
        
        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)

class muon():

    idx = -1

    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
        self.type = 1

        self.pt = ev.__getattr__("_lPt")[idx]
        self.eta = ev.__getattr__("_lEta")[idx]
        self.etaabs = math.fabs(self.eta)
        self.phi = ev.__getattr__("_lPhi")[idx]
        self.E = ev.__getattr__("_lE")[idx]
        
        self.dxy = ev.__getattr__("_dxy")[idx]
        self.dz = ev.__getattr__("_dz")[idx]
        self.miniIso = ev.__getattr__("_miniIso")[idx]
        self.POGMedium = ev.__getattr__("_lPOGMedium")[idx]
        
        self.trackMultClosestJet = ev.__getattr__("_selectedTrackMult")[idx]
        self.miniIsoCharged = ev.__getattr__("_miniIsoCharged")[idx]
        self.miniIsoNeutral = ev.__getattr__("_miniIso")[idx] - self.miniIsoCharged
        self.pTRel = ev.__getattr__("_ptRel")[idx]
        self.ptRatio = min(ev.__getattr__("_ptRatio")[idx], 1.5)
        self.bTagDeepJetClosestJet = 0 if math.isnan(ev.__getattr__("_closestJetDeepFlavor")[idx]) else ev.__getattr__("_closestJetDeepFlavor")[idx]
        self.bTagDeepCSVClosestJet = 0 if math.isnan(ev.__getattr__("_closestJetDeepCsv")[idx]) else max(ev.__getattr__("_closestJetDeepCsv")[idx],0)
        self.sip3d = ev.__getattr__("_3dIPSig")[idx]
        self.dxylog = math.log(max(math.fabs(self.dxy),10E-20))
        self.dzlog = math.log(max(math.fabs(self.dz),10E-20))
        self.relIso = ev.__getattr__("_relIsoDeltaBeta")[idx]
        self.segmentCompatibility = ev.__getattr__("_lMuonSegComp")[idx]
        self.mvaIdFall17v2noIso = -777
        self.mvaIdSummer16GP = -777
        self.provenance = ev.__getattr__("_lProvenance")[idx]
        
        self.leptonMvaTTH = ev.__getattr__("_leptonMvaTTH")[idx]
        self.leptonMvaTZQ = ev.__getattr__("_leptonMvatZq")[idx]
        self.leptonMvaTOP = ev.__getattr__("_leptonMvaTOP")[idx]

        matchPdgId = ev.__getattr__("_lMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_lMomPdgId")[idx]
        isPrompt = ev.__getattr__("_lIsPrompt")[idx]
        
        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.4)
        passIso = bool(self.miniIso < 0.4)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGMedium == 1)
        passConv = bool(matchPdgId != 22)
        passProv = bool(self.provenance != 1)
        passTau = bool(abs(momPdgId) != 15)
    
        self.passed = (passPt and passEta and passIso and passIPSig and passDxy and passDz and passID)
        
        self.isPrompt = (isPrompt and bool(abs(matchPdgId) == 13) and passConv and passProv and passTau)
        self.isNonPrompt = (not isPrompt)
        
        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)
