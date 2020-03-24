#! /usr/bin/env python

import os
import sys
from array import array
import ROOT

sys.path.append('/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/')
import common as c

import matplotlib.pyplot as pyplot
pyplot.switch_backend('agg')

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Script to produce ROCs"

    parser = OptionParser(usage)
    parser.add_option("-m","--mva",default="TTH,TZQ,TOP",help="input list of MVAs [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")
    parser.add_option("-c","--chan",default="muon",help="channel [default: %default]")
    parser.add_option("-p","--pt",default="pt25toInf",help="pt selection [default: %default]")
    parser.add_option("-y","--year",default="2016",help="year of data taking [default: %default]")
    parser.add_option("-i","--input",default="/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/test.root",help="channel [default: %default]")
    parser.add_option("-o","--output",default="",help="output directory [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

def makeRoc(signal,background):
    
    effPoints = []
    
    totSig = signal.Integral()
    totBkg = background.Integral()
    
    for i in range(1, signal.GetNbinsX()+1):
        effSig = signal.Integral(i, -1)/totSig
        effBkg = background.Integral(i, -1)/totBkg
        effPoints.append((signal.GetBinLowEdge(i), effSig, effBkg))
        
    return effPoints

def drawRoc(roc,name,figDir):

    fig, ax = pyplot.subplots()
    
    for ir, r in enumerate(roc):
        
        sigEff = [i[1] for i in r]
        bkgEff = [i[2] for i in r]

        ax.plot(bkgEff, sigEff, label=name[ir])
    
    legend = ax.legend(loc='lower right', fontsize=16, scatterpoints=1)
    legend.get_frame().set_linewidth(0.0)
    
    ax.set(xlabel='Background efficiency', ylabel='Signal efficiency', title='')
    ax.grid()
    
    ax.set_xscale('log')
    ax.set_xlim(0.0001, 1)
    ax.set_ylim(0.2, 1)
    
    fig.savefig(figDir+'/roc.pdf')
    pyplot.close()

def drawDisc(disc,name,figDir):

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    
    c1 = ROOT.TCanvas()

    prompt = disc['prompt']
    nonprompt = disc['nonprompt']

    prompt.SetFillColorAlpha(ROOT.kRed,0.5)
    prompt.SetLineColor(ROOT.kRed)
    nonprompt.SetFillColorAlpha(ROOT.kBlue,0.5)
    nonprompt.SetLineColor(ROOT.kBlue)
    
    prompt.Rebin(100)
    nonprompt.Rebin(100)
    
    prompt.Draw()
    nonprompt.Draw('same')
    
    m = max(prompt.GetMaximum(),nonprompt.GetMaximum())
    prompt.SetMaximum(1.2*m)
    
    leg = ROOT.TLegend(0.55,0.80,0.65,0.70)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(prompt,"Prompt","f")
    leg.AddEntry(nonprompt,"Nonprompt","f")
    leg.Draw()
    
    c1.Print(figDir+'/disc_'+name+'.pdf')
    c1.Clear()
    
if __name__ == '__main__':
    
    options = main()

    weight, pt, eta, etaAbs, trackMultClosestJet, miniIsoCharged, miniIsoNeutral, \
    pTRel, ptRatio, relIso, sip3d, dxy, dxylog, dz, dzlog, \
    bTagDeepCSVClosestJet, bTagDeepJetClosestJet, mvaIdSummer16GP, segmentCompatibility, mvaIdFall17v2noIso, \
    = (array( 'f',  [0.]) for _ in range(20))
    
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()

    MVAreader = {}
    MVAreader['TOP'] = {}
    MVAreader['TZQ'] = {}
    MVAreader['TTH'] = {}
    
    chan = options.chan.capitalize()
    
    for k, v in MVAreader.iteritems():
        for lep in [chan]:
            v[lep] = ROOT.TMVA.Reader("!Color:!Silent")
    
    treeNames = [options.chan+'Prompt',options.chan+'NonPrompt']

    tree = {}    
    for i in treeNames:
        tree[i] = ROOT.TChain(i)
    
    for k, tr in tree.iteritems():
        tr.Add(options.input)

    for k, m in MVAreader.iteritems():
        for kl, vl in m.iteritems():
            
            v = c.var[kl][k]
                    
            if k == 'TZQ':
                        
                vl.AddVariable(v['pt'], pt)
                vl.AddVariable(v['eta'], etaAbs)
                vl.AddVariable(v['trackMultClosestJet'], trackMultClosestJet)
                vl.AddVariable(v['miniIsoCharged'], miniIsoCharged)
                vl.AddVariable(v['miniIsoNeutral'], miniIsoNeutral)
                vl.AddVariable(v['pTRel'], pTRel)
                vl.AddVariable(v['ptRatio'], ptRatio)
                vl.AddVariable(v['relIso'], relIso)
                vl.AddVariable(v['bTagClosestJet'], bTagDeepCSVClosestJet)
                vl.AddVariable(v['sip3d'], sip3d)
                vl.AddVariable(v['dxy'], dxylog)
                vl.AddVariable(v['dz'], dzlog)
                if kl == 'Elec':
                    if options.year == '2016':
                        vl.AddVariable(v['idSeg'], mvaIdSummer16GP)
                    else:
                        vl.AddVariable(v['idSeg17'], mvaIdFall17v2noIso)
                else:
                    vl.AddVariable(v['idSeg'], segmentCompatibility)
                    
            elif k == 'TTH':
                            
                vl.AddVariable(v['pt'], pt)
                vl.AddVariable(v['eta'], eta)
                vl.AddVariable(v['trackMultClosestJet'], trackMultClosestJet)
                vl.AddVariable(v['miniIsoCharged'], miniIsoCharged)
                vl.AddVariable(v['miniIsoNeutral'], miniIsoNeutral)
                vl.AddVariable(v['pTRel'], pTRel)
                vl.AddVariable(v['bTagClosestJet'], bTagDeepJetClosestJet)
                vl.AddVariable(v['ptRatio'], ptRatio)
                vl.AddVariable(v['dxy'], dxylog)
                vl.AddVariable(v['sip3d'], sip3d)
                vl.AddVariable(v['dz'], dzlog)
                if kl == 'Elec':
                    vl.AddVariable(v['idSeg'], mvaIdFall17v2noIso)
                else:
                    vl.AddVariable(v['idSeg'], segmentCompatibility)

            if k == 'TOP':
                        
                vl.AddVariable(v['dxy'], dxylog)
                vl.AddVariable(v['miniIsoCharged'], miniIsoCharged)
                vl.AddVariable(v['miniIsoNeutral'], miniIsoNeutral)
                vl.AddVariable(v['pTRel'], pTRel)
                vl.AddVariable(v['sip3d'], sip3d)
                if kl == 'Elec':
                    vl.AddVariable(v['idSeg'], mvaIdFall17v2noIso)
                else:
                    vl.AddVariable(v['idSeg'], segmentCompatibility)
                vl.AddVariable(v['ptRatio'], ptRatio)
                vl.AddVariable(v['bTagClosestJet'], bTagDeepJetClosestJet)
                vl.AddVariable(v['pt'], pt)
                vl.AddVariable(v['trackMultClosestJet'], trackMultClosestJet)
                vl.AddVariable(v['eta'], etaAbs)
                vl.AddVariable(v['dz'], dzlog)
                vl.AddVariable(v['relIso'], relIso)

            mvat = 'cuts200_depth4_trees1000_shrinkage0p1'
            if k == 'TZQ':
                if options.year == '2016':
                    if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_tZqTTV16_BDTG.weights.xml')
                    else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_tZqTTV16_BDTG.weights.xml')
                else:
                    if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_tZqTTV17_BDTG.weights.xml')
                    else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_tZqTTV17_BDTG.weights.xml')                        
            elif k == 'TTH':
                if options.year == '2016':
                    if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH16_BDTG.weights.xml')
                    else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_ttH16_BDTG.weights.xml')
                else:
                    if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/el_ttH17_BDTG.weights.xml')
                    else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/heavyNeutrino/multilep/data/mvaWeights/mu_ttH17_BDTG.weights.xml')
            elif k == 'TOP':
                if kl == 'Elec': vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/elec_TOP_'+options.year+'/'+mvat+'/dataset/weights/TMVAClassification_BDTG_'+mvat+'_elec.weights.xml')
                else: vl.BookMVA('BDTG method', '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/Train/muon_TOP_'+options.year+'/'+mvat+'/dataset/weights/TMVAClassification_BDTG_'+mvat+'_muon.weights.xml')

    pref = 'leptonMva'
    mvas = options.mva.split(',')

    hist = {}
    for tr in treeNames:
        hist[tr] = {}

    for i in mvas:
        for k, v in hist.iteritems():
            v[i] = ROOT.TH1F(i+'_'+k, i+'_'+k, 10000, -1.2, 1.2)
#            if i in ['TTH','tZq']:
#    v[i] = ROOT.TH1F(i+'_'+k, i+'_'+k, 10000, -1.2, 1.2)
#            else:
#                v[i] = ROOT.TH1F(i+'_'+k, i+'_'+k, 10000, -0.5, 1.5)

    print 'Fill histograms ..'
    for ktr, tr in tree.iteritems():

        ie = 0
        for ev in tr:

            pt[0] = eval('ev.pt')
            
            if options.pt == 'pt25toInf' and pt[0] < 25: continue
            if options.pt == 'pt0to25' and pt[0] > 25: continue

            ie = ie + 1
            if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
                break

            weight[0] = eval('ev.weight')
            
            eta[0] = eval('ev.eta')                        
            etaAbs[0] = eval('ev.etaAbs')            
            trackMultClosestJet[0] = eval('ev.trackMultClosestJet')
            miniIsoCharged[0] = eval('ev.miniIsoCharged')
            miniIsoNeutral[0] = eval('ev.miniIsoNeutral')
            pTRel[0] = eval('ev.pTRel')
            ptRatio[0] = eval('ev.ptRatio')
            relIso[0] = eval('ev.relIso')
            bTagDeepCSVClosestJet[0] = eval('ev.bTagDeepCSVClosestJet')
            bTagDeepJetClosestJet[0] = eval('ev.bTagDeepJetClosestJet')
            sip3d[0] = eval('ev.sip3d')
            dxylog[0] = eval('ev.dxylog')
            dxy[0] = eval('ev.dxy')
            dzlog[0] = eval('ev.dzlog')
            dz[0] = eval('ev.dz')
            mvaIdSummer16GP[0] = eval('ev.mvaIdSummer16GP')
            mvaIdFall17v2noIso[0] = eval('ev.mvaIdFall17v2noIso')
            segmentCompatibility[0] = eval('ev.segmentCompatibility')
            
#            print 'eta='+str(eta[0]), 'trackMultClosestJet='+str(trackMultClosestJet[0]), \
#            'miniIsoCharged='+str(miniIsoCharged[0]), 'miniIsoNeutral='+str(miniIsoNeutral[0]), \
#            'pTRel='+str(pTRel[0]), \
#            'ptRatio='+str(ptRatio[0]), 'relIso='+str(relIso[0]), \
#            'bTagDeepCSVClosestJet='+str(bTagDeepCSVClosestJet[0]), \
#            'bTagDeepJetClosestJet='+str(bTagDeepJetClosestJet[0]), \
#            'sip3d='+str(sip3d[0]), 'dxylog='+str(dxylog[0]), 'dzlog='+str(dzlog[0]), \
#            'mvaIdSummer16GP='+str(mvaIdSummer16GP[0]), 'segmentCompatibility='+str(segmentCompatibility[0])
            
            for i in mvas:
                
                pred = MVAreader[i][kl].EvaluateMVA('BDTG method')
#                print 'mva '+i+' = '+str(pred)
#                    pred = eval('ev.'+pref+i)
                hist[ktr][i].Fill(pred)

    print 'Produce ROCs ..'
    roc = []
    for i in mvas:
        roc.append(makeRoc(hist[treeNames[0]][i],hist[treeNames[1]][i]))

    print 'Plot results ..'
    figDir = options.output+'pics'
    if os.path.isdir(figDir):
        os.system("rm -rf "+figDir)
    os.system("mkdir "+figDir)
        
    drawRoc(roc,mvas,figDir)
    
    for i in mvas:
        disc = {}
        disc['prompt'] = hist[treeNames[0]][i]
        disc['nonprompt'] = hist[treeNames[1]][i]
        drawDisc(disc,i,figDir)
    
    print '\033[92mDone\033[0;0m'
