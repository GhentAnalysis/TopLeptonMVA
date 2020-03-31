#! /usr/bin/env python

import os
import sys
import math
from array import array
import ROOT

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Script to run a sync exercise"

    parser = OptionParser(usage)
    parser.add_option("-m","--mva",default="TTV",help="the tagger name [default: %default]")
    parser.add_option("-n","--nmax",default=20,help="max number of events [default: %default]")
    parser.add_option("-c","--chan",default="muon",help="channel [default: %default]")
    parser.add_option("-y","--year",default="2018",help="year of data taking [default: %default]")
    parser.add_option("-i","--input",default="vienna.root,/user/kskovpen/analysis/heavyNeutrinoTEST/CMSSW_10_2_20/src/heavyNeutrino/multilep/test/noskim.root",help="input file list [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()

    pt, eta, etaAbs, trackMultClosestJet, miniIsoCharged, miniIsoNeutral, \
    pTRel, ptRatio, relIso, sip3d, dxy, dxylog, dz, dzlog, \
    bTagDeepCSVClosestJet, bTagDeepJetClosestJet, mvaIdSummer16GP, segmentCompatibility, mvaIdFall17v2noIso, \
    leptonMvaTTH, leptonMvaTTV \
    = (array( 'f',  [0.]) for _ in range(21))

    nElectron, nMuon \
    = (array( 'i',  [0]) for _ in range(2))
    
    finput = options.input.split(',')
    
    chan = options.chan
    
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    
    tmva = ROOT.TMVA.Reader("!Color:!Silent")
    
    mvaName = options.mva

    tr1 = ROOT.TChain('blackJackAndHookers/blackJackAndHookersTree')
    tr1.Add(finput[1])

    tr2 = ROOT.TChain('Events')
    tr2.Add(finput[0])
    
    if mvaName == 'TTV':
                        
        tmva.AddVariable('pt', pt)
        tmva.AddVariable('eta', etaAbs)
        tmva.AddVariable('trackMultClosestJet', trackMultClosestJet)
        tmva.AddVariable('miniIsoCharged', miniIsoCharged)
        tmva.AddVariable('miniIsoNeutral', miniIsoNeutral)
        tmva.AddVariable('pTRel', pTRel)
        tmva.AddVariable('ptRatio', ptRatio)
        tmva.AddVariable('relIso', relIso)
        tmva.AddVariable('deepCsvClosestJet', bTagDeepCSVClosestJet)
        tmva.AddVariable('sip3d', sip3d)
        tmva.AddVariable('dxy', dxylog)
        tmva.AddVariable('dz', dzlog)
        if chan == 'elec':
            if options.year == '2016':
                tmva.AddVariable('electronMvaSpring16GP', mvaIdSummer16GP)
            else:
                tmva.AddVariable('electronMvaFall17NoIso', mvaIdFall17v2noIso)
        else:
            tmva.AddVariable('segmentCompatibility', segmentCompatibility)
                    
    elif mvaName == 'TTH':
                            
        tmva.AddVariable('LepGood_pt', pt)
        tmva.AddVariable('LepGood_eta', eta)
        tmva.AddVariable('LepGood_jetNDauChargedMVASel', trackMultClosestJet)
        tmva.AddVariable('LepGood_miniRelIsoCharged', miniIsoCharged)
        tmva.AddVariable('LepGood_miniRelIsoNeutral', miniIsoNeutral)
        tmva.AddVariable('LepGood_jetPtRelv2', pTRel)
        tmva.AddVariable('LepGood_jetDF', bTagDeepJetClosestJet)
        tmva.AddVariable('LepGood_jetPtRatio', ptRatio)
        tmva.AddVariable('LepGood_dxy', dxylog)
        tmva.AddVariable('LepGood_sip3d', sip3d)
        tmva.AddVariable('LepGood_dz', dzlog)
        if chan == 'elec':
            tmva.AddVariable('LepGood_mvaFall17V2noIso', mvaIdFall17v2noIso)
        else:
            tmva.AddVariable('LepGood_segmentComp', segmentCompatibility)

    elif mvaName == 'TOP':

        tmva.AddVariable('dxylog', dxylog)
        tmva.AddVariable('miniIsoCharged', miniIsoCharged)
        tmva.AddVariable('miniIsoNeutral', miniIsoNeutral)
        tmva.AddVariable('pTRel', pTRel)
        tmva.AddVariable('sip3d', sip3d)
        if chan == 'elec':
            tmva.AddVariable('mvaIdFall17v2noIso', mvaIdFall17v2noIso)
        else:
            tmva.AddVariable('segmentCompatibility', segmentCompatibility)
        tmva.AddVariable('ptRatio', ptRatio)
        tmva.AddVariable('bTagDeepJetClosestJet', bTagDeepJetClosestJet)
        tmva.AddVariable('pt', pt)
        tmva.AddVariable('trackMultClosestJet', trackMultClosestJet)
        tmva.AddVariable('etaAbs', etaAbs)
        tmva.AddVariable('dzlog', dzlog)
        tmva.AddVariable('relIso', relIso)

    if mvaName == 'TTV':
        if options.year == '2016':
            if chan == 'elec': tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_tZqTTV16_BDTG.weights.xml')
            else: tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_tZqTTV16_BDTG.weights.xml')
        else:
            if chan == 'elec': tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_tZqTTV17_BDTG.weights.xml')
            else: tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_tZqTTV17_BDTG.weights.xml')                        
    elif mvaName == 'TTH':
        if options.year == '2016':
            if chan == 'elec': tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH16_BDTG.weights.xml')
            else: tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_ttH16_BDTG.weights.xml')
        else:
            if chan == 'elec': tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH17_BDTG.weights.xml')
            else: tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_ttH17_BDTG.weights.xml')
    elif mvaName == 'TOP':
        if chan == 'elec': tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/elec_TOP_'+options.year+'/cuts200_depth4_trees1000_shrinkage0p1/dataset/weights/TMVAClassification_BDTG_cuts200_depth4_trees1000_shrinkage0p1_elec.weights.xml')
        else: tmva.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/muon_TOP_'+options.year+'/cuts200_depth4_trees1000_shrinkage0p1/dataset/weights/TMVAClassification_BDTG_cuts200_depth4_trees1000_shrinkage0p1_muon.weights.xml')

    ie = 0
    for ev in tr1:

        ie = ie + 1
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break
            
        for i in range(ev.__getattr__("_nLight")):
        
            if ev.__getattr__("_lFlavor")[i] == 0 and chan != 'elec': continue
            if ev.__getattr__("_lFlavor")[i] == 1 and chan != 'muon': continue
            
            pt[0] = ev.__getattr__("_lPt")[i]
            
            if pt[0] < 25: continue

            eta[0] = ev.__getattr__("_lEta")[i]
            etaAbs[0] = abs(eta[0])
            trackMultClosestJet[0] = ev.__getattr__("_selectedTrackMult")[i]
            miniIsoCharged[0] = ev.__getattr__("_miniIsoCharged")[i]
            miniIsoNeutral[0] = ev.__getattr__("_miniIso")[i] - miniIsoCharged[0]
            pTRel[0] = ev.__getattr__("_ptRel")[i]
            ptRatio[0] = ev.__getattr__("_ptRatio")[i]
            relIso[0] = ev.__getattr__("_relIso")[i]
            bTagDeepCSVClosestJet[0] = ev.__getattr__("_closestJetDeepCsv")[i]
            bTagDeepJetClosestJet[0] = ev.__getattr__("_closestJetDeepFlavor")[i]
            sip3d[0] = ev.__getattr__("_3dIPSig")[i]
            dxy[0] = ev.__getattr__("_dxy")[i]
            dxylog[0] = math.log(abs(dxy[0]))
            dz[0] = ev.__getattr__("_dz")[i]
            dzlog[0] = math.log(abs(dz[0]))
            if chan == 'elec':
                mvaIdFall17v2noIso[0] = ev.__getattr__("_lElectronMvaFall17NoIso")[i]
            else:
                segmentCompatibility[0] = ev.__getattr__("_lMuonSegComp")[i]
            
            leptonMvaTTH[0] = ev.__getattr__("_leptonMvaTTH")[i]
            leptonMvaTTV[0] = ev.__getattr__("_leptonMvatZq")[i]
            
            print '--- Ghent ---'
            
            print 'pt='+str(pt[0]), 'eta='+str(eta[0]), 'trackMultClosestJet='+str(trackMultClosestJet[0]), \
            'miniIsoCharged='+str(miniIsoCharged[0]), 'miniIsoNeutral='+str(miniIsoNeutral[0]), \
            'pTRel='+str(pTRel[0]), \
            'ptRatio='+str(ptRatio[0]), 'relIso='+str(relIso[0]), \
            'bTagDeepCSVClosestJet='+str(bTagDeepCSVClosestJet[0]), \
            'bTagDeepJetClosestJet='+str(bTagDeepJetClosestJet[0]), \
            'sip3d='+str(sip3d[0]), 'dxylog='+str(dxylog[0]), 'dzlog='+str(dzlog[0]), \
            'mvaIdFall17v2noIso='+str(mvaIdFall17v2noIso[0]), 'segmentCompatibility='+str(segmentCompatibility[0])
            
            print 'leptonMvaTTH=', leptonMvaTTH[0], 'leptonMvaTTV=', leptonMvaTTV[0]
            
            pred = tmva.EvaluateMVA('BDTG method')
            print 'pred=', pred

    lep = 'Electron'
    if chan == 'muon': lep = 'Muon'
        
    ie = 0
    for ev in tr2:

        ie = ie + 1
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break
            
        for i in range(ev.__getattr__("n"+lep)):

            pt[0] = ev.__getattr__(lep+"_pt")[i]
            
            if pt[0] < 25: continue
            
            eta[0] = ev.__getattr__(lep+"_eta")[i]
            etaAbs[0] = abs(eta[0])
            trackMultClosestJet[0] = ev.__getattr__(lep+"_jetNDauChargedMVASel")[i]
            miniIsoCharged[0] = ev.__getattr__(lep+"_miniPFRelIso_chg")[i]
            miniIsoNeutral[0] = ev.__getattr__(lep+"_miniPFRelIso_neu")[i]
            pTRel[0] = ev.__getattr__(lep+"_jetPtRelv2")[i]
            ptRatio[0] = ev.__getattr__(lep+"_jetPtRatio")[i]
            relIso[0] = ev.__getattr__(lep+"_pfRelIso03_all")[i]
            bTagDeepCSVClosestJet[0] = ev.__getattr__(lep+"_jetDeepCSV")[i]
            bTagDeepJetClosestJet[0] = ev.__getattr__(lep+"_jetDeepFlavor")[i]
            sip3d[0] = ev.__getattr__(lep+"_sip3d")[i]
            dxy[0] = ev.__getattr__(lep+"_dxy")[i]
            dxylog[0] = math.log(abs(dxy[0]))
            dz[0] = ev.__getattr__(lep+"_dz")[i]
            dzlog[0] = math.log(abs(dz[0]))
            if chan == 'elec':
                mvaIdFall17v2noIso[0] = ev.__getattr__(lep+"_mvaFall17V2noIso")[i]
            else:
                segmentCompatibility[0] = ev.__getattr__(lep+"_segmentComp")[i]
            
            leptonMvaTTH[0] = ev.__getattr__(lep+"_mvaTTH")[i]
            leptonMvaTTV[0] = ev.__getattr__(lep+"_mvaTTV")[i]
            
            print '--- Vienna ---'
            
            print 'pt='+str(pt[0]), 'eta='+str(eta[0]), 'trackMultClosestJet='+str(trackMultClosestJet[0]), \
            'miniIsoCharged='+str(miniIsoCharged[0]), 'miniIsoNeutral='+str(miniIsoNeutral[0]), \
            'pTRel='+str(pTRel[0]), \
            'ptRatio='+str(ptRatio[0]), 'relIso='+str(relIso[0]), \
            'bTagDeepCSVClosestJet='+str(bTagDeepCSVClosestJet[0]), \
            'bTagDeepJetClosestJet='+str(bTagDeepJetClosestJet[0]), \
            'sip3d='+str(sip3d[0]), 'dxylog='+str(dxylog[0]), 'dzlog='+str(dzlog[0]), \
            'mvaIdFall17v2noIso='+str(mvaIdFall17v2noIso[0]), 'segmentCompatibility='+str(segmentCompatibility[0])
            
            print 'leptonMvaTTH=', leptonMvaTTH[0], 'leptonMvaTTV=', leptonMvaTTV[0]
            
            pred = tmva.EvaluateMVA('BDTG method')
            print 'pred=', pred
        
