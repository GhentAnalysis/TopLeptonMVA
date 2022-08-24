import os
import sys
import math
import pickle, json
from array import array
import utils
import common as c

import ROOT
import xgboost as xgb

class mva():

    def __init__(self, tree, model, typ, year):

        self.isValid = False
        
        if typ == 'tmva':

            self.MVAreader = {}
            for m in model.split(','): self.MVAreader[m] = {}
            
            for k, v in self.MVAreader.iteritems():
                for lep in ['Elec', 'Muon']:
                    v[lep] = ROOT.TMVA.Reader("!Color:!Silent")

            self.pt, self.etaAbs, self.trackMultClosestJet, self.miniIsoCharged, self.miniIsoNeutral, \
            self.pTRel, self.ptRatio, self.relIso, self.sip3d, self.dxy, self.dxylog, self.dz, self.dzlog, \
            self.bTagDeepJetClosestJet, self.segmentCompatibility, self.mvaIdFall17v2noIso, \
            = (array( 'f',  [0.]) for _ in range(16))

            for k, m in self.MVAreader.iteritems():
                for kl, vl in m.iteritems():
                    
                    v = c.var[kl][k]
                    
                    if k in ['TOP-UL']:

                        vl.AddVariable(v['dxy'], self.dxylog)
                        vl.AddVariable(v['miniIsoCharged'], self.miniIsoCharged)
                        vl.AddVariable(v['miniIsoNeutral'], self.miniIsoNeutral)
                        vl.AddVariable(v['pTRel'], self.pTRel)
                        vl.AddVariable(v['sip3d'], self.sip3d)
                        if kl == 'Elec':
                            vl.AddVariable(v['idSeg'], self.mvaIdFall17v2noIso)
                        else:
                            vl.AddVariable(v['idSeg'], self.segmentCompatibility)
                        vl.AddVariable(v['ptRatio'], self.ptRatio)
                        vl.AddVariable(v['bTagClosestJet'], self.bTagDeepJetClosestJet)
                        vl.AddVariable(v['pt'], self.pt)
                        vl.AddVariable(v['trackMultClosestJet'], self.trackMultClosestJet)
                        vl.AddVariable(v['eta'], self.etaAbs)
                        vl.AddVariable(v['dz'], self.dzlog)
                        vl.AddVariable(v['relIso'], self.relIso)

                    elif k in ['TOP']:

                        vl.AddVariable(v['dxy'], self.dxylog)
                        vl.AddVariable(v['miniIsoCharged'], self.miniIsoCharged)
                        vl.AddVariable(v['miniIsoNeutral'], self.miniIsoNeutral)
                        vl.AddVariable(v['pTRel'], self.pTRel)
                        vl.AddVariable(v['sip3d'], self.sip3d)
                        if kl == 'Elec':
                            vl.AddVariable(v['idSeg'], self.mvaIdFall17v2noIso)
                        else:
                            vl.AddVariable(v['idSeg'], self.segmentCompatibility)
                        vl.AddVariable(v['ptRatio'], self.ptRatio)
                        vl.AddVariable(v['bTagClosestJet'], self.bTagDeepJetClosestJet)
                        vl.AddVariable(v['pt'], self.pt)
                        vl.AddVariable(v['trackMultClosestJet'], self.trackMultClosestJet)
                        vl.AddVariable(v['eta'], self.etaAbs)
                        vl.AddVariable(v['dz'], self.dzlog)
                        vl.AddVariable(v['relIso'], self.relIso)

                    if year == '2016APV': year = '2016'
                    if k == 'TOP-UL':
                        if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/TMVA/elec_TOP_'+year+'/cuts200_depth4_trees1000_shrinkage0p1/dataset/weights/TMVAClassification_BDTG_cuts200_depth4_trees1000_shrinkage0p1_elec.weights.xml')
                        else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/TMVA/muon_TOP_'+year+'/cuts200_depth4_trees1000_shrinkage0p1/dataset/weights/TMVAClassification_BDTG_cuts200_depth4_trees1000_shrinkage0p1_muon.weights.xml')
                    elif k == 'TOP':
                        if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Weights/TOP/TMVA_BDTG_TOP_elec_'+year+'.weights.xml')
                        else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Weights/TOP/TMVA_BDTG_TOP_muon_'+year+'.weights.xml')

        if typ == 'xgb' and model != '':

            self.XGBReader = {}
            models = model.split(',')
            mpath = '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/weights'
            mconf = 'n_estimators-2000__max_depth-4__eta-0.1__gamma-5__min_child_weight-500'

            for kl in ['Elec', 'Muon']:

                self.XGBReader[kl] = {}
                for m in models:
                    self.XGBReader[kl][m] = xgb.Booster()
                    mver = m.split('.')[1]
                    self.XGBReader[kl][m].load_model(mpath+'/'+m.replace('TOP-UL.','')+'_'+kl.lower()+'_'+year+'/'+mconf+'/xgb.bin')
#                    self.XGBReader[kl][m].load_model(mpath+'/'+m.replace('TOP-UL.','')+'_'+kl.lower()+'_2017/'+mconf+'/xgb.bin')
                    self.isValid = True
            
    def predictXGB(self, lep, x, m):

        return self.XGBReader[lep][m].predict(x)

    def predictTMVA(self, lep, name):

        return self.MVAreader[name][lep].EvaluateMVA('BDTG method')
        
