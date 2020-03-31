import os
import sys
import math
import operator
from array import array
import xml.etree.ElementTree as ET
import xgboost as xgb
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
    parser.add_option("-s","--sample",default="sample",help="input sample [default: %default]")
    parser.add_option("-t","--tag",default="tag",help="production tag [default: %default]")
    parser.add_option("-x","--xml",default="samples.xml",help="input xml configuration [default: %default]")
    parser.add_option("-o","--output",default="output.root",help="output file name [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")
    parser.add_option("-m","--model",default="model.bin",help="model file [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    ROOT.gROOT.SetBatch()
    
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    outFile = ROOT.TFile.Open(options.output,"RECREATE")

    files=[]
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        if s.get('id') == options.sample and s.get('tag') == options.tag:
            for child in s:
                files.append(child.text)
                
    elecPrompt = tr.tree('elecPrompt')
    elecNonPrompt = tr.tree('elecNonPrompt')
    muonPrompt = tr.tree('muonPrompt')
    muonNonPrompt = tr.tree('muonNonPrompt')

    gtr = ROOT.TChain(c.treeName)

    for f in files:
        print f
        gtr.Add(f)

    nEntries = gtr.GetEntries()
    print 'Number of events:', nEntries

#    dl = mva.mva(gtr, options.model, 'xgb')
#    tmva = mva.mva(gtr, options.model, 'tmva')
    
    ie = 0

    print 'Create datasets ..'
    for ev in gtr:

        ie = ie + 1
        if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
            break

        Electrons, Muons = [], []
        
        Event = obj.event(ev)

        nLep = ev.__getattr__("_nL")
        for i in range(0,nLep):
            lepType = ev.__getattr__("_lFlavor")[i]
            if lepType == 0:
                lep = obj.electron(ev,i)
                if lep.passed:
                    Electrons.append(lep)
            elif lepType == 1:
                lep = obj.muon(ev,i)
                if lep.passed:
                    Muons.append(lep)

        obj.removeOverlap(Electrons,Muons)
                
        for idx, o in enumerate([Electrons,Muons]):
            
            for l in o:
                
                if idx == 0:
                    if l.isPrompt: tr = elecPrompt
                    elif l.isNonPrompt: tr = elecNonPrompt
                    else: continue 
                elif idx == 1:
                    if l.isPrompt: tr = muonPrompt
                    elif l.isNonPrompt: tr = muonNonPrompt
                    else: continue
                else:
                    print 'Using more collections than expected'
                    sys.exit()

                tr.weightDs.append(Event.weight)
                
                tr.ptDs.append(l.pt)
                tr.etaDs.append(l.eta)
                tr.etaAbsDs.append(l.etaabs)
                tr.trackMultClosestJetDs.append(l.trackMultClosestJet)
                tr.miniIsoChargedDs.append(l.miniIsoCharged)
                tr.miniIsoNeutralDs.append(l.miniIsoNeutral)
                tr.pTRelDs.append(l.pTRel)
                tr.ptRatioDs.append(l.ptRatio)
                tr.relIsoDs.append(l.relIso)
                tr.relIsoDeltaBetaDs.append(l.relIsoDeltaBeta)
                tr.sip3dDs.append(l.sip3d)
                tr.dxylogDs.append(l.dxylog)
                tr.dxyDs.append(l.dxy)
                tr.dzlogDs.append(l.dzlog)
                tr.dzDs.append(l.dz)
                tr.bTagDeepCSVClosestJetDs.append(l.bTagDeepCSVClosestJet)
                tr.bTagDeepJetClosestJetDs.append(l.bTagDeepJetClosestJet)
                tr.mvaIdSummer16GPDs.append(l.mvaIdSummer16GP)
                tr.segmentCompatibilityDs.append(l.segmentCompatibility)
                tr.mvaIdFall17v2noIsoDs.append(l.mvaIdFall17v2noIso)
                
                tr.leptonMvaTTHHNDs.append(l.leptonMvaTTH)
                tr.leptonMvaTZQHNDs.append(l.leptonMvaTZQ)
                tr.leptonMvaTOPHNDs.append(l.leptonMvaTOP)

    print 'Fill output trees ..'
    for itr, tr in enumerate([elecPrompt,elecNonPrompt,muonPrompt,muonNonPrompt]):

        isElec = True
        
#        var = {}
#        for mva in ['TZQ','TTH']: var[mva] = c.var['Elec'][mva]
#        if itr > 1:
#            isElec = False
#            for mva in ['TZQ','TTH']: var[mva] = c.var['Muon'][mva]
        
        nEvents = len(tr.weightDs)

#        if dl.isValid:
            
#            data = []
#            for i in range(nEvents):
#                data.append([eval('tr.'+v+'Ds['+str(i)+']') for v in var])

#            if nEvents > 0:
#                x = xgb.DMatrix(data, feature_names=var)
#                tr.leptonMvaTopDs = dl.predictXGB(x)

        for i in range(nEvents):
            
            tr.weight[0] = tr.weightDs[i]
            
            tr.leptonMvaTTHHN[0] = tr.leptonMvaTTHHNDs[i]
            tr.leptonMvaTZQHN[0] = tr.leptonMvaTZQHNDs[i]
            tr.leptonMvaTOPHN[0] = tr.leptonMvaTOPHNDs[i]
#            if dl.isValid: tr.leptonMvaTop[0] = tr.leptonMvaTopDs[i]

#            tmva.pt[0] = tr.ptDs[i]
#            tmva.eta[0] = tr.etaDs[i]
#            tmva.etaAbs[0] = tr.etaAbsDs[i]
#            tmva.trackMultClosestJet[0] = tr.trackMultClosestJetDs[i]
#            tmva.miniIsoCharged[0] = tr.miniIsoChargedDs[i]
#            tmva.miniIsoNeutral[0] = tr.miniIsoNeutralDs[i]
#            tmva.pTRel[0] = tr.pTRelDs[i]
#            tmva.ptRatio[0] = tr.ptRatioDs[i]
#            tmva.relIso[0] = tr.relIsoDs[i]
#            tmva.sip3d[0] = tr.sip3dDs[i]
#            tmva.dxy[0] = tr.dxyDs[i]
#            tmva.dxylog[0] = tr.dxylogDs[i]
#            tmva.dz[0] = tr.dzDs[i]
#            tmva.dzlog[0] = tr.dzlogDs[i]
#            tmva.bTagDeepCSVClosestJet[0] = tr.bTagDeepCSVClosestJetDs[i]
#            tmva.bTagDeepJetClosestJet[0] = tr.bTagDeepJetClosestJetDs[i]
#            tmva.mvaIdSummer16GP[0] = tr.mvaIdSummer16GPDs[i]
#            tmva.segmentCompatibility[0] = tr.segmentCompatibilityDs[i]
#            tmva.mvaIdFall17v2noIso[0] = tr.mvaIdFall17v2noIsoDs[i]

            tr.pt[0] = tr.ptDs[i]
            tr.eta[0] = tr.etaDs[i]
            tr.etaAbs[0] = tr.etaAbsDs[i]
            tr.trackMultClosestJet[0] = tr.trackMultClosestJetDs[i]
            tr.miniIsoCharged[0] = tr.miniIsoChargedDs[i]
            tr.miniIsoNeutral[0] = tr.miniIsoNeutralDs[i]
            tr.pTRel[0] = tr.pTRelDs[i]
            tr.ptRatio[0] = tr.ptRatioDs[i]
            tr.relIso[0] = tr.relIsoDs[i]
            tr.relIsoDeltaBeta[0] = tr.relIsoDeltaBetaDs[i]
            tr.sip3d[0] = tr.sip3dDs[i]
            tr.dxy[0] = tr.dxyDs[i]
            tr.dxylog[0] = tr.dxylogDs[i]
            tr.dz[0] = tr.dzDs[i]
            tr.dzlog[0] = tr.dzlogDs[i]
            tr.bTagDeepCSVClosestJet[0] = tr.bTagDeepCSVClosestJetDs[i]
            tr.bTagDeepJetClosestJet[0] = tr.bTagDeepJetClosestJetDs[i]
            tr.mvaIdSummer16GP[0] = tr.mvaIdSummer16GPDs[i]
            tr.segmentCompatibility[0] = tr.segmentCompatibilityDs[i]
            tr.mvaIdFall17v2noIso[0] = tr.mvaIdFall17v2noIsoDs[i]
            
#            tr.leptonMvaTTH[0] = tmva.predictTMVA('Elec','TTH') if isElec else tmva.predictTMVA('Muon','TTH')
#            tr.leptonMvaTZQ[0] = tmva.predictTMVA('Elec','TZQ') if isElec else tmva.predictTMVA('Muon','TZQ')
#            tr.leptonMvaTOP[0] = tmva.predictTMVA('Elec','TOP') if isElec else tmva.predictTMVA('Muon','TOP')
            
            tr.fill()
        
    outFile.Write()
    outFile.Close()
    
    print '\033[92mDone\033[0;0m'
