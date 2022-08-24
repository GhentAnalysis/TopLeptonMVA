import os
import sys
import math
from array import array
import utils
import ROOT

class tree():

    def __init__(self, name, toSplit):
        
        self.weight = array( 'f', [ -777 ] )

        self.nvertex = array( 'i', [ 0 ] )
        
        self.pt, self.eta, self.etaAbs, self.trackMultClosestJet, self.miniIsoCharged, self.miniIsoNeutral, \
        self.miniIso, self.pTRel, self.ptRatio, self.relIso, \
        self.bTagDeepJetClosestJet, \
        self.sip3d, self.dxy, self.dz, self.drMin, \
        self.dxylog, self.dzlog, self.segmentCompatibility, self.mvaIdFall17v2noIso \
        = (array( 'f', [ -777 ] ) for _ in range(19))
        
        self.puppiChargedHadronIso, self.puppiNeutralHadronIso, self.puppiPhotonIso, \
        self.puppiNoLeptonsChargedHadronIso, self.puppiNoLeptonsNeutralHadronIso, self.puppiNoLeptonsPhotonIso, \
        self.puppiIso, self.puppiNoLeptonsIso, self.puppiCombIso \
        = (array( 'f', [ -777 ] ) for _ in range(9))

        self.leptonMvaTOPULTOPv1, self.leptonMvaTOPULTOPv2, \
        self.leptonMvaTOPUL4TOPv1, self.leptonMvaTOPUL4TOPv2, \
        self.leptonMvaTOPULTOPTAUFLIPv1, self.leptonMvaTOPULTOPTAUFLIPv2, \
        self.leptonMvaTOPUL4TOPTAUFLIPv1, self.leptonMvaTOPUL4TOPTAUFLIPv2, \
        self.leptonMvaTOPUL, self.leptonMvaTOP \
        = (array( 'f', [ -777 ] ) for _ in range(10))
        
        self.nEvent, self.matchPdgId, self.missHits, self.POGMedium = (array( 'i', [ -777 ] ) for _ in range(4))
        
        self.isPrompt, self.isPromptAll, self.fromPromptW, self.fromPromptTau, self.fromPromptPhoton, \
        self.fromBHadron, self.fromDHadron, self.fromLightMeson, self.fromOtherHadron, self.fromUnknown, \
        self.fromExtConv, self.isChargeFlip, self.fromNone, self.passedPresel, self.isLeptonMva4TOP = \
        (array( 'b', [ False ] ) for _ in range(15))

        self.weightDs = []
        
        self.nvertexDs = []
        
        self.ptDs, self.etaDs, self.etaAbsDs, self.trackMultClosestJetDs, self.miniIsoChargedDs, self.miniIsoNeutralDs, \
        self.miniIsoDs, \
        self.pTRelDs, self.ptRatioDs, self.relIsoDs, self.sip3dDs, \
        self.dxyDs, self.dxylogDs, self.dzDs, self.dzlogDs, self.drMinDs, \
        self.bTagDeepJetClosestJetDs, \
        self.segmentCompatibilityDs, self.mvaIdFall17v2noIsoDs \
        = ([] for _ in range(19))

        self.puppiChargedHadronIsoDs, self.puppiNeutralHadronIsoDs, self.puppiPhotonIsoDs, \
        self.puppiNoLeptonsChargedHadronIsoDs, self.puppiNoLeptonsNeutralHadronIsoDs, self.puppiNoLeptonsPhotonIsoDs, \
        self.puppiIsoDs, self.puppiNoLeptonsIsoDs, self.puppiCombIsoDs \
        = ([] for _ in range(9))

        self.leptonMvaTOPULTOPv1Ds, self.leptonMvaTOPULTOPv2Ds, \
        self.leptonMvaTOPUL4TOPv1Ds, self.leptonMvaTOPUL4TOPv2Ds, \
        self.leptonMvaTOPULTOPTAUFLIPv1Ds, self.leptonMvaTOPULTOPTAUFLIPv2Ds, \
        self.leptonMvaTOPUL4TOPTAUFLIPv1Ds, self.leptonMvaTOPUL4TOPTAUFLIPv2Ds, \
        self.leptonMvaTOPULDs, self.leptonMvaTOPDs \
        = ([] for _ in range(10))
        
        self.nEventDs, self.matchPdgIdDs, self.missHitsDs, self.POGMediumDs = ([] for _ in range(4))

        self.isPromptDs, self.isPromptAllDs, self.fromPromptWDs, self.fromPromptTauDs, self.fromPromptPhotonDs, \
        self.fromBHadronDs, self.fromDHadronDs, self.fromLightMesonDs, self.fromOtherHadronDs, self.fromUnknownDs, \
        self.fromExtConvDs, self.isChargeFlipDs, self.fromNoneDs, self.passedPreselDs, self.isLeptonMva4TOPDs = \
        ([] for _ in range(15))
        
        self.t = ROOT.TTree( name, 'Training tree' )

        self.t.Branch( 'weight', self.weight, 'weight/F' )
        
        self.t.Branch( 'nvertex', self.nvertex, 'nvertex/I' )

        self.t.Branch( 'pt', self.pt, 'pt/F' )
        self.t.Branch( 'eta', self.eta, 'eta/F' )
        self.t.Branch( 'etaAbs', self.etaAbs, 'etaAbs/F' )
        self.t.Branch( 'trackMultClosestJet', self.trackMultClosestJet, 'trackMultClosestJet/F' )
        self.t.Branch( 'miniIso', self.miniIso, 'miniIso/F' )
        self.t.Branch( 'miniIsoCharged', self.miniIsoCharged, 'miniIsoCharged/F' )
        self.t.Branch( 'miniIsoNeutral', self.miniIsoNeutral, 'miniIsoNeutral/F' )
        self.t.Branch( 'missHits', self.missHits, 'missHits/I' )
        self.t.Branch( 'pTRel', self.pTRel, 'pTRel/F' )
        self.t.Branch( 'ptRatio', self.ptRatio, 'ptRatio/F' )
        self.t.Branch( 'relIso', self.relIso, 'relIso/F' )
        self.t.Branch( 'bTagDeepJetClosestJet', self.bTagDeepJetClosestJet, 'bTagDeepJetClosestJet/F' )
        self.t.Branch( 'sip3d', self.sip3d, 'sip3d/F' )
        self.t.Branch( 'dxy', self.dxy, 'dxy/F' )
        self.t.Branch( 'dz', self.dz, 'dz/F' )
        self.t.Branch( 'dxylog', self.dxylog, 'dxylog/F' )
        self.t.Branch( 'dzlog', self.dzlog, 'dzlog/F' )
        self.t.Branch( 'drMin', self.drMin, 'drMin/F' )
        self.t.Branch( 'POGMedium', self.POGMedium, 'POGMedium/I' )
        self.t.Branch( 'segmentCompatibility', self.segmentCompatibility, 'segmentCompatibility/F' )
        self.t.Branch( 'mvaIdFall17v2noIso', self.mvaIdFall17v2noIso, 'mvaIdFall17v2noIso/F' )
        
        self.t.Branch( 'puppiChargedHadronIso', self.puppiChargedHadronIso, 'puppiChargedHadronIso/F' )
        self.t.Branch( 'puppiNeutralHadronIso', self.puppiNeutralHadronIso, 'puppiNeutralHadronIso/F' )
        self.t.Branch( 'puppiPhotonIso', self.puppiPhotonIso, 'puppiPhotonIso/F' )
        self.t.Branch( 'puppiNoLeptonsChargedHadronIso', self.puppiNoLeptonsChargedHadronIso, 'puppiNoLeptonsChargedHadronIso/F' )
        self.t.Branch( 'puppiNoLeptonsNeutralHadronIso', self.puppiNoLeptonsNeutralHadronIso, 'puppiNoLeptonsNeutralHadronIso/F' )
        self.t.Branch( 'puppiNoLeptonsPhotonIso', self.puppiNoLeptonsPhotonIso, 'puppiNoLeptonsPhotonIso/F' )
        self.t.Branch( 'puppiIso', self.puppiIso, 'puppiIso/F' )
        self.t.Branch( 'puppiNoLeptonsIso', self.puppiNoLeptonsIso, 'puppiNoLeptonsIso/F' )
        self.t.Branch( 'puppiCombIso', self.puppiCombIso, 'puppiCombIso/F' )
        
        self.t.Branch( 'leptonMvaTOPULTOPv1', self.leptonMvaTOPULTOPv1, 'leptonMvaTOPULTOPv1/F' )
        self.t.Branch( 'leptonMvaTOPUL4TOPv1', self.leptonMvaTOPUL4TOPv1, 'leptonMvaTOPUL4TOPv1/F' )
        self.t.Branch( 'leptonMvaTOPULTOPTAUFLIPv1', self.leptonMvaTOPULTOPTAUFLIPv1, 'leptonMvaTOPULTOPTAUFLIPv1/F' )
        self.t.Branch( 'leptonMvaTOPUL4TOPTAUFLIPv1', self.leptonMvaTOPUL4TOPTAUFLIPv1, 'leptonMvaTOPUL4TOPTAUFLIPv1/F' )

        self.t.Branch( 'leptonMvaTOPULTOPv2', self.leptonMvaTOPULTOPv2, 'leptonMvaTOPULTOPv2/F' )
        self.t.Branch( 'leptonMvaTOPUL4TOPv2', self.leptonMvaTOPUL4TOPv2, 'leptonMvaTOPUL4TOPv2/F' )
        self.t.Branch( 'leptonMvaTOPULTOPTAUFLIPv2', self.leptonMvaTOPULTOPTAUFLIPv2, 'leptonMvaTOPULTOPTAUFLIPv2/F' )
        self.t.Branch( 'leptonMvaTOPUL4TOPTAUFLIPv2', self.leptonMvaTOPUL4TOPTAUFLIPv2, 'leptonMvaTOPUL4TOPTAUFLIPv2/F' )
        
        self.t.Branch( 'leptonMvaTOPUL', self.leptonMvaTOPUL, 'leptonMvaTOPUL/F' )
        self.t.Branch( 'leptonMvaTOP', self.leptonMvaTOP, 'leptonMvaTOP/F' )
        
        self.t.Branch( 'passedPresel', self.passedPresel, 'passedPresel/O' )
        
        self.t.Branch( 'isLeptonMva4TOP', self.isLeptonMva4TOP, 'isLeptonMva4TOP/O' )
        
        if not toSplit:
            self.t.Branch( 'nEvent', self.nEvent, 'nEvent/I' )
            self.t.Branch( 'isPrompt', self.isPrompt, 'isPrompt/O' )
            self.t.Branch( 'isPromptAll', self.isPromptAll, 'isPromptAll/O' )
            self.t.Branch( 'isChargeFlip', self.isChargeFlip, 'isChargeFlip/O' )
            self.t.Branch( 'matchPdgId', self.matchPdgId, 'matchPdgId/I' )
            self.t.Branch( 'fromPromptW', self.fromPromptW, 'fromPromptW/O' )
            self.t.Branch( 'fromPromptTau', self.fromPromptTau, 'fromPromptTau/O' )
            self.t.Branch( 'fromPromptPhoton', self.fromPromptPhoton, 'fromPromptPhoton/O' )
            self.t.Branch( 'fromBHadron', self.fromBHadron, 'fromBHadron/O' )
            self.t.Branch( 'fromDHadron', self.fromDHadron, 'fromDHadron/O' )
            self.t.Branch( 'fromLightMeson', self.fromLightMeson, 'fromLightMeson/O' )
            self.t.Branch( 'fromOtherHadron', self.fromOtherHadron, 'fromOtherHadron/O' )
            self.t.Branch( 'fromUnknown', self.fromUnknown, 'fromUnknown/O' )
            self.t.Branch( 'fromExtConv', self.fromExtConv, 'fromExtConv/O' )
            self.t.Branch( 'fromNone', self.fromNone, 'fromNone/O' )
        
    def fill(self):

        self.t.Fill()
        
