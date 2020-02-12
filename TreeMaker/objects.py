import os
import sys
import math
import utils as ut
import ROOT

import common as c
import functions as fun

class event():

    def __init__(self, ev):

        self.weight = ev.__getattr__("_weight")
    
class electron():

    idx = -1

    def __init__(self, ev, idx, mva):

        self.idx = idx
        self.passed = False
        self.type = 0

        self.pt = ev.__getattr__("_lPt")[idx]
        self.eta = ev.__getattr__("_lEta")[idx]
        self.phi = ev.__getattr__("_lPhi")[idx]
        self.E = ev.__getattr__("_lE")[idx]
        
        self.dxy = ev.__getattr__("_dxy")[idx]
        self.dz = ev.__getattr__("_dz")[idx]
        self.miniIso = ev.__getattr__("_miniIso")[idx]
        self.POGNoIsoLoose = ev.__getattr__("_lElectronPassMVAFall17NoIsoWPLoose")[idx]
        
        self.jetNDauChargedMVASel = ev.__getattr__("_selectedTrackMult")[idx]
        self.miniRelIsoCharged = ev.__getattr__("_miniIsoCharged")[idx]
        self.miniRelIsoNeutral = ev.__getattr__("_miniIso")[idx] - self.miniRelIsoCharged
        self.jetPtRelv2 = ev.__getattr__("_ptRel")[idx]
        self.jetPtRatio = min(ev.__getattr__("_ptRatio")[idx], 1.5)
        self.jetBTag = 0 if math.isnan(ev.__getattr__("_closestJetDeepFlavor")[idx]) else ev.__getattr__("_closestJetDeepFlavor")[idx]
        self.sip3d = ev.__getattr__("_3dIPSig")[idx]
        if math.fabs(self.dxy) < 10E-20: self.dxy = 10E-20
        if math.fabs(self.dz) < 10E-20: self.dz = 10E-20
        self.dxylog = math.log(math.fabs(self.dxy))
        self.dzlog = math.log(math.fabs(self.dz))
        self.relIso0p3 = ev.__getattr__("_relIso")[idx]
        self.mvaIDsegComp = ev.__getattr__("_lElectronMvaFall17NoIso")[idx]
        
        self.leptonMvaTTH = ev.__getattr__("_leptonMvaTTH")[idx]
        self.leptonMvatZq = ev.__getattr__("_leptonMvatZq")[idx]

        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.5)
        passIso = bool(self.miniIso < 0.4)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGNoIsoLoose == 1)
    
        self.passed = (passPt and passEta and passIPSig and passDxy and passDz and passIso and passID)
        
        matchPdgId = ev.__getattr__("_lMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_lMomPdgId")[idx]
        isPrompt = ev.__getattr__("_lIsPrompt")[idx]
        
        self.isPrompt = isPrompt
        
        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)

class muon():

    idx = -1

    def __init__(self, ev, idx, mva):

        self.idx = idx
        self.passed = False
        self.type = 1

        self.pt = ev.__getattr__("_lPt")[idx]
        self.eta = ev.__getattr__("_lEta")[idx]
        self.phi = ev.__getattr__("_lPhi")[idx]
        self.E = ev.__getattr__("_lE")[idx]
        
        self.dxy = ev.__getattr__("_dxy")[idx]
        self.dz = ev.__getattr__("_dz")[idx]
        self.miniIso = ev.__getattr__("_miniIso")[idx]
        self.POGMedium = ev.__getattr__("_lPOGMedium")[idx]
        
        self.jetNDauChargedMVASel = ev.__getattr__("_selectedTrackMult")[idx]
        self.miniRelIsoCharged = ev.__getattr__("_miniIsoCharged")[idx]
        self.miniRelIsoNeutral = ev.__getattr__("_miniIso")[idx] - self.miniRelIsoCharged
        self.jetPtRelv2 = ev.__getattr__("_ptRel")[idx]
        self.jetPtRatio = min(ev.__getattr__("_ptRatio")[idx], 1.5)
        self.jetBTag = 0 if math.isnan(ev.__getattr__("_closestJetDeepFlavor")[idx]) else ev.__getattr__("_closestJetDeepFlavor")[idx]
        self.sip3d = ev.__getattr__("_3dIPSig")[idx]
        if math.fabs(self.dxy) < 10E-20: self.dxy = 10E-20
        if math.fabs(self.dz) < 10E-20: self.dz = 10E-20
        self.dxylog = math.log(math.fabs(self.dxy))
        self.dzlog = math.log(math.fabs(self.dz))
        self.relIso0p3 = ev.__getattr__("_relIso")[idx]
        self.mvaIDsegComp = ev.__getattr__("_lMuonSegComp")[idx]
        
        self.leptonMvaTTH = ev.__getattr__("_leptonMvaTTH")[idx]
        self.leptonMvatZq = ev.__getattr__("_leptonMvatZq")[idx]
        
        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.4)
        passIso = bool(self.miniIso < 0.4)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGMedium == 1)
    
        self.passed = (passPt and passEta and passIso and passIPSig and passDxy and passDz and passID)

        matchPdgId = ev.__getattr__("_lMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_lMomPdgId")[idx]
        isPrompt = ev.__getattr__("_lIsPrompt")[idx]
        
        self.isPrompt = isPrompt
        
        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)
