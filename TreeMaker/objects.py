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
        self.nvertex = ev.__getattr__("_nVertex")

class jets():

    def __init__(self, ev):

        self.n = ev.__getattr__("_jetN")
        self.pt = ev.__getattr__("_jetPt")
        self.eta = ev.__getattr__("_jetEta")
        self.phi = ev.__getattr__("_jetPhi")
        
def findClosestJetDr(Lepton, Jets):
    
    # remove the closest jet in dR overlapping with a lepton in dR=0.4
    drMinOverlap, idxMinOverlap = 777, -1
    for jidx in range(Jets.n):
        dr = ut.deltaR(Lepton.eta, Lepton.phi, Jets.eta[jidx], Jets.phi[jidx])
        if dr < drMinOverlap and dr < 0.4:
            drMinOverlap = dr
            idxMinOverlap = jidx

    # find the closest jet after lepton-jet overlap removal
    drMin, idxMin = 777, -1
    for jidx in range(Jets.n):
        if jidx in [idxMinOverlap]: continue
        dr = ut.deltaR(Lepton.eta, Lepton.phi, Jets.eta[jidx], Jets.phi[jidx])
        if dr < drMin:
            drMin = dr
            idxMin = jidx
            
    return drMin
        
class electron():

    idx = -1

    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
        self.type = 0
        
        self.drMin = -777

        self.charge = ev.__getattr__("_elecCharge")[idx]
        self.pt = ev.__getattr__("_elecPt")[idx]
        self.eta = ev.__getattr__("_elecEta")[idx]
        self.etaabs = math.fabs(self.eta)
        self.phi = ev.__getattr__("_elecPhi")[idx]
        self.E = ev.__getattr__("_elecE")[idx]        
        
        self.dxy = ev.__getattr__("_elecDxy")[idx]
        self.dz = ev.__getattr__("_elecDz")[idx]
        self.miniIso = ev.__getattr__("_elecMiniIso")[idx]
        self.POGNoIsoLoose = ev.__getattr__("_elecPassMVAFall17NoIsoWPLoose")[idx]
        self.POGMedium = 0

        self.trackMultClosestJet = ev.__getattr__("_elecSelectedTrackMult")[idx]
        self.miniIsoCharged = ev.__getattr__("_elecMiniIsoCharged")[idx]
        self.miniIsoNeutral = ev.__getattr__("_elecMiniIso")[idx] - self.miniIsoCharged
        self.pTRel = ev.__getattr__("_elecPtRel")[idx]
        self.ptRatio = min(ev.__getattr__("_elecPtRatio")[idx], 1.5)
        self.bTagDeepJetClosestJet = 0 if math.isnan(ev.__getattr__("_elecClosestJetDeepFlavor")[idx]) else ev.__getattr__("_elecClosestJetDeepFlavor")[idx]
        self.sip3d = ev.__getattr__("_elec3dIPSig")[idx]
        self.dxylog = math.log(max(math.fabs(self.dxy),10E-20))
        self.dzlog = math.log(max(math.fabs(self.dz),10E-20))
        self.missHits = ev.__getattr__("_elecMissingHits")[idx]
        self.relIso = ev.__getattr__("_elecRelIso")[idx]
        self.mvaIdFall17v2noIso = ev.__getattr__("_elecMvaFall17NoIso")[idx]
        self.segmentCompatibility = -777
        self.provenance = ev.__getattr__("_elecProvenance")[idx]
 
        self.puppiChargedHadronIso = ev.__getattr__("_elecPuppiChargedHadronIso")[idx]
        self.puppiNeutralHadronIso = ev.__getattr__("_elecPuppiNeutralHadronIso")[idx]
        self.puppiPhotonIso = ev.__getattr__("_elecPuppiPhotonIso")[idx]
        self.puppiNoLeptonsChargedHadronIso = ev.__getattr__("_elecPuppiNoLeptonsChargedHadronIso")[idx]
        self.puppiNoLeptonsNeutralHadronIso = ev.__getattr__("_elecPuppiNoLeptonsNeutralHadronIso")[idx]
        self.puppiNoLeptonsPhotonIso = ev.__getattr__("_elecPuppiNoLeptonsPhotonIso")[idx]
        self.puppiIso = (self.puppiChargedHadronIso+self.puppiNeutralHadronIso+self.puppiPhotonIso)/self.pt if self.pt > 0 else 0.
        self.puppiNoLeptonsIso = (self.puppiNoLeptonsChargedHadronIso+self.puppiNoLeptonsNeutralHadronIso+self.puppiNoLeptonsPhotonIso)/self.pt if self.pt > 0 else 0.
        self.puppiCombIso = (self.puppiIso+self.puppiNoLeptonsIso)/2.
        
        self.matchPdgId = ev.__getattr__("_elecMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_elecMomPdgId")[idx]        
        isPrompt = ev.__getattr__("_elecIsPrompt")[idx]
        parentIds = ev.__getattr__("_elecParentIds")[idx]
        
        self.fromPromptW = bool(ev.__getattr__("_elecIsFromPromptW")[idx])
        self.fromPromptTau = bool(ev.__getattr__("_elecIsFromPromptTau")[idx])
        self.fromPromptPhoton = bool(ev.__getattr__("_elecIsFromPromptPhoton")[idx])
        self.fromBHadron = bool(ev.__getattr__("_elecIsFromBHadron")[idx])
        self.fromDHadron = bool(ev.__getattr__("_elecIsFromDHadron")[idx])
        self.fromLightMeson = bool(ev.__getattr__("_elecIsFromLightMeson")[idx])
        self.fromOtherHadron = bool(ev.__getattr__("_elecIsFromOtherHadron")[idx])
        self.fromUnknown = bool(ev.__getattr__("_elecIsFromUnknown")[idx])
        self.fromNone = bool(len(parentIds) == 0)
            
        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.5)
        passIso = bool(self.miniIso < 0.4)
        passHits = bool(self.missHits < 2)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGNoIsoLoose)
        passConv = bool(self.matchPdgId != 22)
        passProv = bool(self.provenance != 1)
        passTau = bool(abs(momPdgId) != 15)

        passLooseIPSig = bool(math.fabs(self.sip3d) < 15.)
        passLooseRelIso = bool(self.relIso < 1.)
    
        self.passedPresel = (passIPSig and passDxy and passDz and passIso and passHits)
        self.passed = (passPt and passEta and passLooseIPSig and passLooseRelIso)
        self.passedPresel = True
        self.passed = bool(self.pt > 10)
        
        self.isPromptAll = bool(self.fromPromptW or self.fromPromptPhoton or self.fromPromptTau)
        self.isPromptOld = bool(((isPrompt and passProv) or not passTau) and bool(abs(self.matchPdgId) == 11) and passConv)
        self.isPrompt = ((abs(self.matchPdgId) == 11) and self.isPromptAll)
        self.isNonPrompt = (not self.isPrompt)
        self.fromExtConv = bool(not passConv)
        self.isChargeFlip = bool(self.matchPdgId*self.charge > 0) and bool(abs(self.matchPdgId) == 11) and self.isPromptAll

        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)

        self.isLeptonMva4TOP = bool(self.miniIso < 0.12) and bool(self.ptRatio > 0.80 or self.pTRel > 7.2)
        
        if abs(self.eta) < 0.8 and (self.pt > 10 and self.pt < 15) and self.mvaIdFall17v2noIso < 0.77: self.isLeptonMva4TOP = False
        elif abs(self.eta) < 0.8 and (self.pt > 25) and self.mvaIdFall17v2noIso < 0.52: self.isLeptonMva4TOP = False
        elif abs(self.eta) > 0.8 and abs(self.eta) < 1.479 and (self.pt > 10 and self.pt < 15) and self.mvaIdFall17v2noIso < 0.56: self.isLeptonMva4TOP = False
        elif abs(self.eta) > 0.8 and abs(self.eta) < 1.479 and (self.pt > 25) and self.mvaIdFall17v2noIso < 0.11: self.isLeptonMva4TOP = False
        elif abs(self.eta) > 1.479 and abs(self.eta) < 2.5 and (self.pt > 10 and self.pt < 15) and self.mvaIdFall17v2noIso < 0.48: self.isLeptonMva4TOP = False
        elif abs(self.eta) > 1.479 and abs(self.eta) < 2.5 and (self.pt > 25) and self.mvaIdFall17v2noIso < -0.01: self.isLeptonMva4TOP = False

class muon():

    idx = -1

    def __init__(self, ev, idx):

        self.idx = idx
        self.passed = False
        self.type = 1
        
        self.drMin = -777

        self.charge = ev.__getattr__("_muonCharge")[idx]
        self.pt = ev.__getattr__("_muonPt")[idx]
        self.eta = ev.__getattr__("_muonEta")[idx]
        self.etaabs = math.fabs(self.eta)
        self.phi = ev.__getattr__("_muonPhi")[idx]
        self.E = ev.__getattr__("_muonE")[idx]
        
        self.dxy = ev.__getattr__("_muonDxy")[idx]
        self.dz = ev.__getattr__("_muonDz")[idx]
        self.miniIso = ev.__getattr__("_muonMiniIso")[idx]
        self.POGMedium = int(bool(ev.__getattr__("_muonPOGMedium")[idx]) == True)
        
        self.trackMultClosestJet = ev.__getattr__("_muonSelectedTrackMult")[idx]
        self.miniIsoCharged = ev.__getattr__("_muonMiniIsoCharged")[idx]
        self.miniIsoNeutral = ev.__getattr__("_muonMiniIso")[idx] - self.miniIsoCharged
        self.pTRel = ev.__getattr__("_muonPtRel")[idx]
        self.ptRatio = min(ev.__getattr__("_muonPtRatio")[idx], 1.5)
        self.bTagDeepJetClosestJet = 0 if math.isnan(ev.__getattr__("_muonClosestJetDeepFlavor")[idx]) else ev.__getattr__("_muonClosestJetDeepFlavor")[idx]
        self.sip3d = ev.__getattr__("_muon3dIPSig")[idx]
        self.dxylog = math.log(max(math.fabs(self.dxy),10E-20))
        self.dzlog = math.log(max(math.fabs(self.dz),10E-20))
        self.relIso = ev.__getattr__("_muonRelIsoDeltaBeta")[idx]
        self.segmentCompatibility = ev.__getattr__("_muonSegComp")[idx]
        self.missHits = -777
        self.mvaIdFall17v2noIso = -777
        self.mvaIdSummer16GP = -777
        self.provenance = ev.__getattr__("_muonProvenance")[idx]

        self.puppiChargedHadronIso = ev.__getattr__("_muonPuppiChargedHadronIso")[idx]
        self.puppiNeutralHadronIso = ev.__getattr__("_muonPuppiNeutralHadronIso")[idx]
        self.puppiPhotonIso = ev.__getattr__("_muonPuppiPhotonIso")[idx]
        self.puppiNoLeptonsChargedHadronIso = ev.__getattr__("_muonPuppiNoLeptonsChargedHadronIso")[idx]
        self.puppiNoLeptonsNeutralHadronIso = ev.__getattr__("_muonPuppiNoLeptonsNeutralHadronIso")[idx]
        self.puppiNoLeptonsPhotonIso = ev.__getattr__("_muonPuppiNoLeptonsPhotonIso")[idx]
        self.puppiIso = (self.puppiChargedHadronIso+self.puppiNeutralHadronIso+self.puppiPhotonIso)/self.pt if self.pt > 0 else 0.
        self.puppiNoLeptonsIso = (self.puppiNoLeptonsChargedHadronIso+self.puppiNoLeptonsNeutralHadronIso+self.puppiNoLeptonsPhotonIso)/self.pt if self.pt > 0 else 0.
        self.puppiCombIso = (self.puppiIso+self.puppiNoLeptonsIso)/2.
        
        self.matchPdgId = ev.__getattr__("_muonMatchPdgId")[idx]
        momPdgId = ev.__getattr__("_muonMomPdgId")[idx]
        isPrompt = ev.__getattr__("_muonIsPrompt")[idx]
        parentIds = ev.__getattr__("_muonParentIds")[idx]

        self.fromPromptW = bool(ev.__getattr__("_muonIsFromPromptW")[idx])
        self.fromPromptTau = bool(ev.__getattr__("_muonIsFromPromptTau")[idx])
        self.fromPromptPhoton = bool(ev.__getattr__("_muonIsFromPromptPhoton")[idx])
        self.fromBHadron = bool(ev.__getattr__("_muonIsFromBHadron")[idx])
        self.fromDHadron = bool(ev.__getattr__("_muonIsFromDHadron")[idx])
        self.fromLightMeson = bool(ev.__getattr__("_muonIsFromLightMeson")[idx])
        self.fromOtherHadron = bool(ev.__getattr__("_muonIsFromOtherHadron")[idx])
        self.fromUnknown = bool(ev.__getattr__("_muonIsFromUnknown")[idx])
        self.fromNone = bool(len(parentIds) == 0)
        
        passPt = bool(self.pt > 10)
        passEta = bool(math.fabs(self.eta) < 2.4)
        passIso = bool(self.miniIso < 0.4)
        passIPSig = bool(math.fabs(self.sip3d) < 8)
        passDxy = bool(math.fabs(self.dxy) < 0.05)
        passDz = bool(math.fabs(self.dz) < 0.1)
        passID = bool(self.POGMedium)
        passConv = bool(self.matchPdgId != 22)
        passProv = bool(self.provenance != 1)
        passTau = bool(abs(momPdgId) != 15)
    
        passLooseIPSig = bool(math.fabs(self.sip3d) < 15.)
        passLooseRelIso = bool(self.relIso < 1.)

        self.passedPresel = (passIso and passIPSig and passDxy and passDz and passID)
        self.passed = (passPt and passEta and passID and passLooseIPSig and passLooseRelIso)
        self.passedPresel = True
        self.passed = bool(self.pt > 10)

        self.isPromptAll = bool(self.fromPromptW or self.fromPromptPhoton or self.fromPromptTau)
        self.isPromptOld = bool(((isPrompt and passProv) or not passTau) and bool(abs(self.matchPdgId) == 13) and passConv)
        self.isPrompt = ((abs(self.matchPdgId) == 13) and self.isPromptAll)
        self.isNonPrompt = (not self.isPrompt)
        self.fromExtConv = bool(not passConv)
        self.isChargeFlip = bool(self.matchPdgId*self.charge > 0) and bool(abs(self.matchPdgId) == 13) and self.isPromptAll
            
        self.px = self.pt*math.cos(self.phi)
        self.py = self.pt*math.sin(self.phi)
        self.pz = self.pt*math.sinh(self.eta)

        self.isLeptonMva4TOP = self.POGMedium and \
        bool(self.miniIso < 0.16) and bool(self.ptRatio > 0.76 or self.pTRel > 7.2)
