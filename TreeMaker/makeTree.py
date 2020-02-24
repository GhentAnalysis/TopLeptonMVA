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

    dl = mva.mva(gtr, options.model)
    
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
                lep = obj.electron(ev,i,dl)
                if lep.passed:
                    Electrons.append(lep)
            elif lepType == 1:
                lep = obj.muon(ev,i,dl)
                if lep.passed:
                    Muons.append(lep)
            
        obj.removeOverlap(Electrons,Muons)
                
        for idx, o in enumerate([Electrons,Muons]):
            
            for l in o:
                
                if idx == 0:
                    if l.isPrompt: tr = elecPrompt
                    elif l.isNonPrompt: tr = elecNonPrompt
                    else: continue 
                else:
                    if l.isPrompt: tr = muonPrompt
                    elif l.isNonPrompt: tr = muonNonPrompt
                    else: continue

                tr.weightDs.append(Event.weight)
                tr.ptDs.append(l.pt)
                tr.etaDs.append(l.eta)
                tr.jetNDauChargedMVASelDs.append(l.jetNDauChargedMVASel)
                tr.miniRelIsoChargedDs.append(l.miniRelIsoCharged)
                tr.miniRelIsoNeutralDs.append(l.miniRelIsoNeutral)
                tr.jetPtRelv2Ds.append(l.jetPtRelv2)
                tr.jetPtRatioDs.append(l.jetPtRatio)
                tr.jetBTagDs.append(l.jetBTag)
                tr.jetBTagCSVDs.append(l.jetBTagCSV)
                tr.sip3dDs.append(l.sip3d)
                tr.dxyDs.append(l.dxylog)
                tr.dzDs.append(l.dzlog)
                tr.relIso0p3Ds.append(l.relIso0p3)
                tr.mvaIDsegCompDs.append(l.mvaIDsegComp)
                
                tr.leptonMvaTTHDs.append(l.leptonMvaTTH)
                tr.leptonMvatZqDs.append(l.leptonMvatZq)

    print 'Fill output trees ..'
    for tr in [elecPrompt,elecNonPrompt,muonPrompt,muonNonPrompt]:
        
        nEvents = len(tr.weightDs)

        if dl.isValid:
            
            data = []
            for i in range(nEvents):
                data.append([eval('tr.'+v+'Ds['+str(i)+']') for v in c.variables])
            
            if nEvents > 0:
                x = xgb.DMatrix(data, feature_names=c.variables)
                tr.leptonMvaTopDs = dl.predict(x)

        for i in range(nEvents):
            
            tr.weight[0] = tr.weightDs[i]    
            tr.pt[0] = tr.ptDs[i]
            tr.eta[0] = tr.etaDs[i]
            tr.jetNDauChargedMVASel[0] = tr.jetNDauChargedMVASelDs[i]
            tr.miniRelIsoCharged[0] = tr.miniRelIsoChargedDs[i]
            tr.miniRelIsoNeutral[0] = tr.miniRelIsoNeutralDs[i]
            tr.jetPtRelv2[0] = tr.jetPtRelv2Ds[i]
            tr.jetPtRatio[0] = tr.jetPtRatioDs[i]
            tr.jetBTag[0] = tr.jetBTagDs[i]
            tr.jetBTagCSV[0] = tr.jetBTagCSVDs[i]
            tr.sip3d[0] = tr.sip3dDs[i]
            tr.dxy[0] = tr.dxyDs[i]
            tr.dz[0] = tr.dzDs[i]
            tr.relIso0p3[0] = tr.relIso0p3Ds[i]
            tr.mvaIDsegComp[0] = tr.mvaIDsegCompDs[i]
                
            tr.leptonMvaTTH[0] = tr.leptonMvaTTHDs[i]
            tr.leptonMvatZq[0] = tr.leptonMvatZqDs[i]
            if dl.isValid: tr.leptonMvaTop[0] = tr.leptonMvaTopDs[i]

            tr.fill()
        
    outFile.Write()
    outFile.Close()
    
    print '\033[92mDone\033[0;0m'
