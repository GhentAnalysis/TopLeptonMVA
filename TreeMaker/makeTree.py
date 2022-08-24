import os
import sys
import math
import operator
from array import array
import xml.etree.ElementTree as ET
import xgboost as xgb
import pandas as pd
import ROOT

import common as c
import objects as obj
import tree as tr
import mva

ROOT.PyConfig.IgnoreCommandLineOptions = True
from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Script to produce training trees"

    parser = OptionParser(usage)
    parser.add_option("--sample", default="sample", help="input sample [default: %default]")
    parser.add_option("--tag", default="tag", help="production tag [default: %default]")
    parser.add_option("--xml", default="samples.xml", help="input xml configuration [default: %default]")
    parser.add_option("--output", default="output.root", help="output file name [default: %default]")
    parser.add_option("--nmax", default=-1, help="max number of events [default: %default]")
    parser.add_option("--modelxgb", default="model.bin", help="model file (xgboost) [default: %default]")
    parser.add_option("--modeltmva", default="model.bin", help="model file (TMVA) [default: %default]")
    parser.add_option("--split", action="store_true", help="split into prompt and nonprompt [default: %default]")
    parser.add_option("--splitfine", action="store_true", help="split into classes [default: %default]")
    parser.add_option("--year", default="2017", help="year of the data taking [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    ROOT.gROOT.SetBatch()
    
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    outFile = ROOT.TFile.Open(options.output, "RECREATE")

    files=[]
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        if s.get('id') == options.sample and s.get('tag') == options.tag:
            for child in s:
                files.append(child.text)
                
    splitf = (options.split or options.splitfine)

    if options.splitfine:
        
        elecPrompt = tr.tree('elecPrompt', splitf)
        elecPromptTau = tr.tree('elecPromptTau', splitf)
        elecPromptFlip = tr.tree('elecPromptFlip', splitf)
        elecNonpromptHF = tr.tree('elecNonpromptHF', splitf)
        elecNonpromptLF = tr.tree('elecNonpromptLF', splitf)
        elecNonpromptConv = tr.tree('elecNonpromptConv', splitf)
        elecNonpromptPileup = tr.tree('elecNonpromptPileup', splitf)
        
        muonPrompt = tr.tree('muonPrompt', splitf)
        muonPromptTau = tr.tree('muonPromptTau', splitf)
        muonPromptFlip = tr.tree('muonPromptFlip', splitf)
        muonNonpromptHF = tr.tree('muonNonpromptHF', splitf)
        muonNonpromptLF = tr.tree('muonNonpromptLF', splitf)
        muonNonpromptPileup = tr.tree('muonNonpromptPileup', splitf)

    elif options.split:
        
        elecPrompt = tr.tree('elecPrompt', splitf)
        elecNonprompt = tr.tree('elecNonprompt', splitf)
        muonPrompt = tr.tree('muonPrompt', splitf)
        muonNonprompt = tr.tree('muonNonprompt', splitf)
        
    else:
        
        elecAll = tr.tree('elecAll', splitf)
        muonAll = tr.tree('muonAll', splitf)

    gtr = ROOT.TChain(c.treeName)

    for f in files:
        print(f)
        gtr.Add(f)

    nEntries = gtr.GetEntries()
    print('Number of events:', nEntries)

    dl = mva.mva(gtr, options.modelxgb, 'xgb', options.year)
    tmva = mva.mva(gtr, options.modeltmva, 'tmva', options.year)
    
    ie = 0

    print('Create datasets ..')
    for ev in gtr:

        ie = ie + 1
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break

        Electrons, Muons, Jets = [], [], []
        
        Event = obj.event(ev)
        
        Jets = obj.jets(ev)

        nElec = ev.__getattr__("_elecN")
        nMuon = ev.__getattr__("_muonN")
        
        for i in range(0,nElec):
            lep = obj.electron(ev,i)
            if lep.passed:
                lep.drMin = obj.findClosestJetDr(lep, Jets)
                Electrons.append(lep)
        for i in range(0,nMuon):
            lep = obj.muon(ev,i)
            if lep.passed:
                lep.drMin = obj.findClosestJetDr(lep, Jets)
                Muons.append(lep)

        obj.removeOverlap(Electrons,Muons)

        for idx, o in enumerate([Electrons,Muons]):
            
            for l in o:
                
                if idx == 0:
                    if options.splitfine:
                        if l.isPrompt and not (l.isChargeFlip or l.fromPromptTau): tr = elecPrompt
                        elif l.fromPromptTau: tr = elecPromptTau
                        elif l.isChargeFlip: tr = elecPromptFlip
                        else:
                            if l.fromBHadron or l.fromDHadron: tr = elecNonpromptHF
                            elif l.fromLightMeson or l.fromOtherHadron or l.fromUnknown: tr = elecNonpromptLF
                            elif l.fromExtConv: tr = elecNonpromptConv
                            else: tr = elecNonpromptPileup
                    elif options.split:
                        if l.isPrompt: tr = elecPrompt
                        else: tr = elecNonprompt
                    else: tr = elecAll
                elif idx == 1:
                    if options.splitfine:
                        if l.isPrompt and not (l.isChargeFlip or l.fromPromptTau): tr = muonPrompt
                        elif l.fromPromptTau: tr = muonPromptTau
                        elif l.isChargeFlip: tr = muonPromptFlip
                        else:
                            if l.fromBHadron or l.fromDHadron: tr = muonNonpromptHF
                            elif l.fromLightMeson or l.fromOtherHadron or l.fromUnknown: tr = muonNonpromptLF
                            else: tr = muonNonpromptPileup
                    elif options.split:
                        if l.isPrompt: tr = muonPrompt
                        else: tr = muonNonprompt
                    else: tr = muonAll
                else:
                    print('Using more collections than expected')
                    sys.exit()

                tr.weightDs.append(Event.weight)
                tr.nvertexDs.append(Event.nvertex)
#                tr.eventNbDs.append(Event.eventNb)
                
                tr.ptDs.append(l.pt)
                tr.etaDs.append(l.eta)
                tr.etaAbsDs.append(l.etaabs)
                tr.trackMultClosestJetDs.append(l.trackMultClosestJet)
                tr.miniIsoDs.append(l.miniIso)
                tr.miniIsoChargedDs.append(l.miniIsoCharged)
                tr.miniIsoNeutralDs.append(l.miniIsoNeutral)
                tr.missHitsDs.append(l.missHits)
                tr.pTRelDs.append(l.pTRel)
                tr.ptRatioDs.append(l.ptRatio)
                tr.relIsoDs.append(l.relIso)
                tr.sip3dDs.append(l.sip3d)
                tr.dxylogDs.append(l.dxylog)
                tr.dxyDs.append(l.dxy)
                tr.dzlogDs.append(l.dzlog)
                tr.dzDs.append(l.dz)
                tr.drMinDs.append(l.drMin)
                tr.POGMediumDs.append(l.POGMedium)
                tr.bTagDeepJetClosestJetDs.append(l.bTagDeepJetClosestJet)
                tr.segmentCompatibilityDs.append(l.segmentCompatibility)
                tr.mvaIdFall17v2noIsoDs.append(l.mvaIdFall17v2noIso)
                
                tr.puppiChargedHadronIsoDs.append(l.puppiChargedHadronIso)
                tr.puppiNeutralHadronIsoDs.append(l.puppiNeutralHadronIso)
                tr.puppiPhotonIsoDs.append(l.puppiPhotonIso)
                tr.puppiNoLeptonsChargedHadronIsoDs.append(l.puppiNoLeptonsChargedHadronIso)
                tr.puppiNoLeptonsNeutralHadronIsoDs.append(l.puppiNoLeptonsNeutralHadronIso)
                tr.puppiNoLeptonsPhotonIsoDs.append(l.puppiNoLeptonsPhotonIso)
                tr.puppiIsoDs.append(l.puppiIso)
                tr.puppiNoLeptonsIsoDs.append(l.puppiNoLeptonsIso)
                tr.puppiCombIsoDs.append(l.puppiCombIso)
                
                tr.passedPreselDs.append(l.passedPresel)
                
                tr.isLeptonMva4TOPDs.append(l.isLeptonMva4TOP)

                if not options.split:
                    tr.nEventDs.append(ie)
                    tr.isPromptDs.append(l.isPrompt)
                    tr.isChargeFlipDs.append(l.isChargeFlip)
                    tr.matchPdgIdDs.append(l.matchPdgId)
                    tr.fromPromptWDs.append(l.fromPromptW)
                    tr.fromPromptTauDs.append(l.fromPromptTau)
                    tr.fromPromptPhotonDs.append(l.fromPromptPhoton)
                    tr.fromBHadronDs.append(l.fromBHadron)
                    tr.fromDHadronDs.append(l.fromDHadron)
                    tr.fromLightMesonDs.append(l.fromLightMeson)
                    tr.fromOtherHadronDs.append(l.fromOtherHadron)
                    tr.fromUnknownDs.append(l.fromUnknown)
                    tr.fromExtConvDs.append(l.fromExtConv)
                    tr.fromNoneDs.append(l.fromNone)
                
#                tr.leptonMvaTTHHNDs.append(l.leptonMvaTTH)
#                tr.leptonMvaTZQHNDs.append(l.leptonMvaTZQ)
#                tr.leptonMvaTOPHNDs.append(l.leptonMvaTOP)
#                tr.isLeptonMva4TOPHNDs.append(l.isLeptonMva4TOP)

    print('Fill output trees ..')
    if options.split: trees = {'elecPrompt':elecPrompt, 'elecNonprompt':elecNonprompt, 'muonPrompt':muonPrompt, 'muonNonprompt':muonNonprompt}
    elif options.splitfine: trees = {'elecPrompt':elecPrompt, 'elecPromptTau':elecPromptTau, 'elecPromptFlip':elecPromptFlip, 'elecNonpromptHF':elecNonpromptHF, 'elecNonpromptLF':elecNonpromptLF, 'elecNonpromptConv':elecNonpromptConv, 'elecNonpromptPileup':elecNonpromptPileup, 'muonPrompt':muonPrompt, 'muonPromptTau':muonPromptTau, 'muonPromptFlip':muonPromptFlip, 'muonNonpromptHF':muonNonpromptHF, 'muonNonpromptLF':muonNonpromptLF, 'muonNonpromptPileup':muonNonpromptPileup}
    else: trees = {'elecAll':elecAll, 'muonAll':muonAll}

    for itr, tr in enumerate(trees.values()):

        flav = 'Elec' if 'elec' in trees.keys()[itr] else 'Muon'
        
        mxgb = options.modelxgb.split(',')
        
        var = {}
        for mva in mxgb: var[mva] = c.var[flav][mva]
        
        nEvents = len(tr.weightDs)

        if dl.isValid:
            
            for mname in mxgb:
                
                data = []
                for i in range(nEvents):
                    data.append([eval('tr.'+v+'Ds['+str(i)+']') for v in var[mname].values()])

                if nEvents > 0:
                    df = pd.DataFrame.from_records(data, columns=var[mname].keys())
                    x = xgb.DMatrix(df)
                    exec('%s = %s' % ('tr.leptonMva'+mname.replace('.','').replace('_','').replace('-','')+'Ds', 'dl.predictXGB(flav, x, mname)'))
                   
                for jj, d in enumerate(data):
                    if flav == 'Elec':
                        print(tr.leptonMvaTOPULTOPv1Ds[jj], d)
#                    if abs(d[0]-36.8431892) < 0.1:

        for i in range(nEvents):
            
            tr.weight[0] = tr.weightDs[i]
            tr.nvertex[0] = tr.nvertexDs[i]
#            tr.eventNb[0] = tr.eventNbDs[i]
            
#            tr.leptonMvaTTHHN[0] = tr.leptonMvaTTHHNDs[i]
#            tr.leptonMvaTZQHN[0] = tr.leptonMvaTZQHNDs[i]
#            tr.leptonMvaTOPHN[0] = tr.leptonMvaTOPHNDs[i]
#            tr.isLeptonMva4TOPHN[0] = tr.isLeptonMva4TOPHNDs[i]
            if dl.isValid:
                for mname in mxgb: exec('%s = %s' % ('tr.leptonMva'+mname.replace('.','').replace('_','').replace('-','')+'[0]', 'tr.leptonMva'+mname.replace('.','').replace('_','').replace('-','')+'Ds[i]'))

            tmva.pt[0] = tr.ptDs[i]
            tmva.etaAbs[0] = tr.etaAbsDs[i]
            tmva.trackMultClosestJet[0] = tr.trackMultClosestJetDs[i]
            tmva.miniIsoCharged[0] = tr.miniIsoChargedDs[i]
            tmva.miniIsoNeutral[0] = tr.miniIsoNeutralDs[i]
            tmva.pTRel[0] = tr.pTRelDs[i]
            tmva.ptRatio[0] = tr.ptRatioDs[i]
            tmva.relIso[0] = tr.relIsoDs[i]
            tmva.sip3d[0] = tr.sip3dDs[i]
            tmva.dxylog[0] = tr.dxylogDs[i]
            tmva.dzlog[0] = tr.dzlogDs[i]
            tmva.bTagDeepJetClosestJet[0] = tr.bTagDeepJetClosestJetDs[i]
            tmva.segmentCompatibility[0] = tr.segmentCompatibilityDs[i]
            tmva.mvaIdFall17v2noIso[0] = tr.mvaIdFall17v2noIsoDs[i]

            tr.pt[0] = tr.ptDs[i]
            tr.eta[0] = tr.etaDs[i]
            tr.etaAbs[0] = tr.etaAbsDs[i]
            tr.trackMultClosestJet[0] = tr.trackMultClosestJetDs[i]
            tr.miniIso[0] = tr.miniIsoDs[i]
            tr.miniIsoCharged[0] = tr.miniIsoChargedDs[i]
            tr.miniIsoNeutral[0] = tr.miniIsoNeutralDs[i]
            tr.missHits[0] = tr.missHitsDs[i]
            tr.pTRel[0] = tr.pTRelDs[i]
            tr.ptRatio[0] = tr.ptRatioDs[i]
            tr.relIso[0] = tr.relIsoDs[i]
            tr.sip3d[0] = tr.sip3dDs[i]
            tr.dxy[0] = tr.dxyDs[i]
            tr.dxylog[0] = tr.dxylogDs[i]
            tr.dz[0] = tr.dzDs[i]
            tr.dzlog[0] = tr.dzlogDs[i]
            tr.drMin[0] = tr.drMinDs[i]
            tr.POGMedium[0] = tr.POGMediumDs[i]
            tr.bTagDeepJetClosestJet[0] = tr.bTagDeepJetClosestJetDs[i]
            tr.segmentCompatibility[0] = tr.segmentCompatibilityDs[i]
            tr.mvaIdFall17v2noIso[0] = tr.mvaIdFall17v2noIsoDs[i]
            
            tr.puppiChargedHadronIso[0] = tr.puppiChargedHadronIsoDs[i]
            tr.puppiNeutralHadronIso[0] = tr.puppiNeutralHadronIsoDs[i]
            tr.puppiPhotonIso[0] = tr.puppiPhotonIsoDs[i]
            tr.puppiNoLeptonsChargedHadronIso[0] = tr.puppiNoLeptonsChargedHadronIsoDs[i]
            tr.puppiNoLeptonsNeutralHadronIso[0] = tr.puppiNoLeptonsNeutralHadronIsoDs[i]
            tr.puppiNoLeptonsPhotonIso[0] = tr.puppiNoLeptonsPhotonIsoDs[i]
            tr.puppiIso[0] = tr.puppiIsoDs[i]
            tr.puppiNoLeptonsIso[0] = tr.puppiNoLeptonsIsoDs[i]
            tr.puppiCombIso[0] = tr.puppiCombIsoDs[i]
            
            tr.passedPresel[0] = tr.passedPreselDs[i]
            
            tr.isLeptonMva4TOP[0] = tr.isLeptonMva4TOPDs[i]
 
            for m in options.modeltmva.split(','):
                pred = tmva.predictTMVA(flav, m)
                if m == 'TOP': tr.leptonMvaTOP[0] = pred
                elif m == 'TOP-UL': tr.leptonMvaTOPUL[0] = pred

            if not (options.split or options.splitfine):
                tr.nEvent[0] = tr.nEventDs[i]
                tr.isPrompt[0] = tr.isPromptDs[i]
                tr.isChargeFlip[0] = tr.isChargeFlipDs[i]
                tr.matchPdgId[0] = tr.matchPdgIdDs[i]
                tr.fromPromptW[0] = tr.fromPromptWDs[i]
                tr.fromPromptTau[0] = tr.fromPromptTauDs[i]
                tr.fromPromptPhoton[0] = tr.fromPromptPhotonDs[i]
                tr.fromBHadron[0] = tr.fromBHadronDs[i]
                tr.fromDHadron[0] = tr.fromDHadronDs[i]
                tr.fromLightMeson[0] = tr.fromLightMesonDs[i]
                tr.fromOtherHadron[0] = tr.fromOtherHadronDs[i]
                tr.fromUnknown[0] = tr.fromUnknownDs[i]
                tr.fromExtConv[0] = tr.fromExtConvDs[i]
                tr.fromNone[0] = tr.fromNoneDs[i]

            tr.fill()
        
    outFile.Write()
    outFile.Close()
    
    print('\033[92mDone\033[0;0m')
