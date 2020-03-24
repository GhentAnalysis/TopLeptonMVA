import os
import sys
import math
from array import array
import utils
import common as c

import ROOT
import xgboost as xgb

class mva():

    def __init__(self, tree, model, typ):

        self.isValid = False
        
        if typ == 'tmva':
            
            self.MVAreader = {}
#            self.MVAreader['TOPJET'] = {}
            self.MVAreader['TZQ'] = {}
            self.MVAreader['TTH'] = {}
            
            for k, v in self.MVAreader.iteritems():
                for lep in ['Elec','Muon']:
                    v[lep] = ROOT.TMVA.Reader("!Color:!Silent")

            self.pt, self.eta, self.etaAbs, self.trackMultClosestJet, self.miniIsoCharged, self.miniIsoNeutral, \
            self.pTRel, self.ptRatio, self.relIso, self.sip3d, self.dxy, self.dxylog, self.dz, self.dzlog, \
            self.bTagDeepCSVClosestJet, self.bTagDeepJetClosestJet, self.mvaIdSummer16GP, \
            self.segmentCompatibility, self.mvaIdFall17v2noIso, \
            = (array( 'f',  [0.]) for _ in range(19))

            for k, m in self.MVAreader.iteritems():
#                if k == 'TOP': continue
                for kl, vl in m.iteritems():
                    
                    v = c.var[kl][k]
                    
                    if k == 'TZQ':
                        
                        vl.AddVariable(v['pt'], self.pt)
                        vl.AddVariable(v['eta'], self.etaAbs)
                        vl.AddVariable(v['trackMultClosestJet'], self.trackMultClosestJet)
                        vl.AddVariable(v['miniIsoCharged'], self.miniIsoCharged)
                        vl.AddVariable(v['miniIsoNeutral'], self.miniIsoNeutral)
                        vl.AddVariable(v['pTRel'], self.pTRel)
                        vl.AddVariable(v['ptRatio'], self.ptRatio)
                        vl.AddVariable(v['relIso'], self.relIso)
                        vl.AddVariable(v['bTagClosestJet'], self.bTagDeepCSVClosestJet)
                        vl.AddVariable(v['sip3d'], self.sip3d)
                        vl.AddVariable(v['dxy'], self.dxylog)
                        vl.AddVariable(v['dz'], self.dzlog)
                        if kl == 'Elec':
                            vl.AddVariable(v['idSeg'], self.mvaIdSummer16GP)
                        else:
                            vl.AddVariable(v['idSeg'], self.segmentCompatibility)
                            
                    elif k == 'TTH':
                            
                        vl.AddVariable(v['pt'], self.pt)
                        vl.AddVariable(v['eta'], self.eta)
                        vl.AddVariable(v['trackMultClosestJet'], self.trackMultClosestJet)
                        vl.AddVariable(v['miniIsoCharged'], self.miniIsoCharged)
                        vl.AddVariable(v['miniIsoNeutral'], self.miniIsoNeutral)
                        vl.AddVariable(v['pTRel'], self.pTRel)
                        vl.AddVariable(v['bTagClosestJet'], self.bTagDeepJetClosestJet)
                        vl.AddVariable(v['ptRatio'], self.ptRatio)
                        vl.AddVariable(v['dxy'], self.dxylog)
                        vl.AddVariable(v['sip3d'], self.sip3d)
                        vl.AddVariable(v['dz'], self.dzlog)
                        if kl == 'Elec':
                            vl.AddVariable(v['idSeg'], self.mvaIdFall17v2noIso)
                        else:
                            vl.AddVariable(v['idSeg'], self.segmentCompatibility)

                    if k == 'TOPJET':
                        
                        vl.AddVariable(v['dxy'], self.dxylog)
                        vl.AddVariable(v['miniIsoCharged'], self.miniIsoCharged)
                        vl.AddVariable(v['miniIsoNeutral'], self.miniIsoNeutral)
                        vl.AddVariable(v['pTRel'], self.pTRel)
                        vl.AddVariable(v['sip3d'], self.sip3d)
                        if kl == 'Elec':
                            vl.AddVariable(v['idSeg'], self.mvaIdSummer16GP)
                        else:
                            vl.AddVariable(v['idSeg'], self.segmentCompatibility)
                        vl.AddVariable(v['ptRatio'], self.ptRatio)
                        vl.AddVariable(v['bTagClosestJet'], self.bTagDeepCSVClosestJet)
                        vl.AddVariable(v['pt'], self.pt)
                        vl.AddVariable(v['trackMultClosestJet'], self.trackMultClosestJet)
                        vl.AddVariable(v['eta'], self.etaAbs)
                        vl.AddVariable(v['dz'], self.dzlog)
                        vl.AddVariable(v['relIso'], self.relIso)
                            
                    if k == 'TZQ':
                        if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_tZqTTV16_BDTG.weights.xml')
                        else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_tZqTTV16_BDTG.weights.xml')
                    elif k == 'TTH':
                        if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH16_BDTG.weights.xml')
                        else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_ttH16_BDTG.weights.xml')
                    elif k == 'TOPJET':
#                        if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH16_BDTG.weights.xml')
                        vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/weights/muon2016.xml')

        if typ == 'xgb' and model != '':
            
            self.mod = xgb.Booster()
            self.mod.load_model(model)
            self.isValid = True
            
    def predictXGB(self, x):

        return self.mod.predict(x)

    def predictTMVA(self, lep, name):

        return self.MVAreader[name][lep].EvaluateMVA('BDTG method')
        
