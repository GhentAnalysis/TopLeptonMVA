import os
import sys
import math
from array import array
import utils
import ROOT

class tree():

    def __init__(self, name):
        
        self.weight \
        = array( 'f', [ -777 ] )
        
        self.pt, self.eta, self.etaAbs, self.trackMultClosestJet, self.miniIsoCharged, self.miniIsoNeutral, \
        self.pTRel, self.ptRatio, self.relIso, \
        self.bTagDeepCSVClosestJet, self.bTagDeepJetClosestJet, \
        self.sip3d, self.dxy, self.dz, \
        self.dxylog, self.dzlog, self.segmentCompatibility, self.mvaIdSummer16GP, self.mvaIdFall17v2noIso, \
        self.leptonMvaTTHHN, self.leptonMvaTZQHN, self.leptonMvaTOPHN \
        = (array( 'f', [ -777 ] ) for _ in range(22))

        self.weightDs \
        = []

        self.ptDs, self.etaDs, self.etaAbsDs, self.trackMultClosestJetDs, self.miniIsoChargedDs, self.miniIsoNeutralDs, \
        self.pTRelDs, self.ptRatioDs, self.relIsoDs, self.sip3dDs, \
        self.dxyDs, self.dxylogDs, self.dzDs, self.dzlogDs, \
        self.leptonMvaTTHHNDs, self.leptonMvaTZQHNDs, self.leptonMvaTOPHNDs, \
        self.bTagDeepCSVClosestJetDs, self.bTagDeepJetClosestJetDs, self.mvaIdSummer16GPDs, \
        self.segmentCompatibilityDs, self.mvaIdFall17v2noIsoDs \
        = ([] for _ in range(22))
        
        self.t = ROOT.TTree( name, 'Training tree' )

        self.t.Branch( 'weight', self.weight, 'weight/F' )

        self.t.Branch( 'pt', self.pt, 'pt/F' )
        self.t.Branch( 'eta', self.eta, 'eta/F' )
        self.t.Branch( 'etaAbs', self.etaAbs, 'etaAbs/F' )
        self.t.Branch( 'trackMultClosestJet', self.trackMultClosestJet, 'trackMultClosestJet/F' )
        self.t.Branch( 'miniIsoCharged', self.miniIsoCharged, 'miniIsoCharged/F' )
        self.t.Branch( 'miniIsoNeutral', self.miniIsoNeutral, 'miniIsoNeutral/F' )
        self.t.Branch( 'pTRel', self.pTRel, 'pTRel/F' )
        self.t.Branch( 'ptRatio', self.ptRatio, 'ptRatio/F' )
        self.t.Branch( 'relIso', self.relIso, 'relIso/F' )
        self.t.Branch( 'bTagDeepCSVClosestJet', self.bTagDeepCSVClosestJet, 'bTagDeepCSVClosestJet/F' )
        self.t.Branch( 'bTagDeepJetClosestJet', self.bTagDeepJetClosestJet, 'bTagDeepJetClosestJet/F' )
        self.t.Branch( 'sip3d', self.sip3d, 'sip3d/F' )
        self.t.Branch( 'dxy', self.dxy, 'dxy/F' )
        self.t.Branch( 'dz', self.dz, 'dz/F' )
        self.t.Branch( 'dxylog', self.dxylog, 'dxylog/F' )
        self.t.Branch( 'dzlog', self.dzlog, 'dzlog/F' )
        self.t.Branch( 'segmentCompatibility', self.segmentCompatibility, 'segmentCompatibility/F' )
        self.t.Branch( 'mvaIdSummer16GP', self.mvaIdSummer16GP, 'mvaIdSummer16GP/F' )
        self.t.Branch( 'mvaIdFall17v2noIso', self.mvaIdFall17v2noIso, 'mvaIdFall17v2noIso/F' )
        
#        self.t.Branch( 'leptonMvaTTH', self.leptonMvaTTH, 'leptonMvaTTH/F' )
#        self.t.Branch( 'leptonMvaTZQ', self.leptonMvaTZQ, 'leptonMvaTZQ/F' )
#        self.t.Branch( 'leptonMvaTOP', self.leptonMvaTOP, 'leptonMvaTOP/F' )

        self.t.Branch( 'leptonMvaTTHHN', self.leptonMvaTTHHN, 'leptonMvaTTHHN/F' )
        self.t.Branch( 'leptonMvaTZQHN', self.leptonMvaTZQHN, 'leptonMvaTZQHN/F' )
        self.t.Branch( 'leptonMvaTOPHN', self.leptonMvaTOPHN, 'leptonMvaTOPHN/F' )
        
    def fill(self):

        self.t.Fill()
        
