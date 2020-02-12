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

        self.pt, self.eta, self.jetNDauChargedMVASel, self.miniRelIsoCharged, self.miniRelIsoNeutral, \
        self.jetPtRelv2, self.jetPtRatio, self.jetBTag, self.sip3d, self.dxy, self.dz, self.relIso0p3, self.mvaIDsegComp, \
        self.leptonMvaTTH, self.leptonMvatZq, self.leptonMvaTop \
        = (array( 'f', [ -777 ] ) for _ in range(16))

        self.weightDs \
        = []

        self.ptDs, self.etaDs, self.jetNDauChargedMVASelDs, self.miniRelIsoChargedDs, self.miniRelIsoNeutralDs, \
        self.jetPtRelv2Ds, self.jetPtRatioDs, self.jetBTagDs, self.sip3dDs, self.dxyDs, self.dzDs, self.relIso0p3Ds, self.mvaIDsegCompDs, \
        self.leptonMvaTTHDs, self.leptonMvatZqDs, self.leptonMvaTopDs \
        = ([] for _ in range(16))
        
        self.t = ROOT.TTree( name, 'Training tree' )

        self.t.Branch( 'weight', self.weight, 'weight/F' )

        self.t.Branch( 'pt', self.pt, 'pt/F' )
        self.t.Branch( 'eta', self.eta, 'eta/F' )
        self.t.Branch( 'jetNDauChargedMVASel', self.jetNDauChargedMVASel, 'jetNDauChargedMVASel/F' )
        self.t.Branch( 'miniRelIsoCharged', self.miniRelIsoCharged, 'miniRelIsoCharged/F' )
        self.t.Branch( 'miniRelIsoNeutral', self.miniRelIsoNeutral, 'miniRelIsoNeutral/F' )
        self.t.Branch( 'jetPtRelv2', self.jetPtRelv2, 'jetPtRelv2/F' )
        self.t.Branch( 'jetPtRatio', self.jetPtRatio, 'jetPtRatio/F' )
        self.t.Branch( 'jetBTag', self.jetBTag, 'jetBTag/F' )
        self.t.Branch( 'sip3d', self.sip3d, 'sip3d/F' )
        self.t.Branch( 'dxy', self.dxy, 'dxy/F' )
        self.t.Branch( 'dz', self.dz, 'dz/F' )
        self.t.Branch( 'relIso0p3', self.relIso0p3, 'relIso0p3/F' )
        self.t.Branch( 'mvaIDsegComp', self.mvaIDsegComp, 'mvaIDsegComp/F' )
        
        self.t.Branch( 'leptonMvaTTH', self.leptonMvaTTH, 'leptonMvaTTH/F' )
        self.t.Branch( 'leptonMvatZq', self.leptonMvatZq, 'leptonMvatZq/F' )
        self.t.Branch( 'leptonMvaTop', self.leptonMvaTop, 'leptonMvaTop/F' )
        
    def fill(self):

        self.t.Fill()
        
