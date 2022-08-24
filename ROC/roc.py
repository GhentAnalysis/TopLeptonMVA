#!/bin/env python3

import os, sys, math
from array import array
import numpy
import pandas as pd
import pickle
import ROOT
import uproot4, glob

import settings as s

wdir = '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Weights/'

sys.path.append('/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/')
import common as c

import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
pyplot.switch_backend('agg')

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]

    usage = "usage: %prog [options]\n Script to produce ROCs"

    parser = OptionParser(usage)
    parser.add_option("--mva", default="TOP,TOPULTOPv1,TOPULTOPv2", help="input list of MVAs [default: %default]")
    parser.add_option("--nmax", type=int, default=1000, help="max number of events [default: %default]")
    parser.add_option("--chan", default="muon", help="channel [default: %default]")
    parser.add_option("--pt", default="pt10toInf", help="pt selection [default: %default]")
    parser.add_option("--year", default="UL16APV", help="year of data taking [default: %default]")
    parser.add_option("--prompt", default="/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/jobs_train_UL16APV_splitfine/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2016APV-v1_UL16APV/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2016APV-v1_UL16APV_0.root", help="channel [default: %default]")
    parser.add_option("--nonprompt", default="/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/jobs_train_UL16APV_splitfine/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2016APV-v1_UL16APV/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD2016APV-v1_UL16APV_0.root", help="channel [default: %default]")
    parser.add_option("--output", default="temp", help="output directory [default: %default]")
    parser.add_option("--presel", action="store_true", help="Apply preselection [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

def computeEff(n1, n2, e1, e2):

    if (n1 + n2) > 0:
        eff = n1 / (n1 + n2)
        err = 1 / (n1 + n2) * math.sqrt(e1 * e1 * n2 * n2 + e2 * e2 * n1 * n1) / (n1 + n2)
    else:
        eff = 0.
        err = 0.
    
    return eff, err

def makeRoc(signal, background, signalAll, backgroundAll):
    
    effPoints = []
    
    totSigAll = signalAll.Integral()
    totBkgAll = backgroundAll.Integral()
    
    totSig = signal.Integral()
    totBkg = background.Integral()
    
    kSig = totSig/totSigAll if (totSigAll > 0) else 1.
    kBkg = totBkg/totBkgAll if (totBkgAll > 0) else 1.
    
    for i in range(1, signal.GetNbinsX()+1):
        effSig = signal.Integral(i, -1)/totSig*kSig
        effBkg = background.Integral(i, -1)/totBkg*kBkg
        effPoints.append((signal.GetBinLowEdge(i), effSig, effBkg))
    
    return effPoints

def drawRoc(roc, name, figDir, eff, sel, effCutBased):

    fig, ax = pyplot.subplots()
    
    for ir, r in enumerate(roc):
        
        sigEff = [i[1] for i in r]
        bkgEff = [i[2] for i in r]

        lab = name[ir]
        if lab in ['TOPUL']: lab = 'TOP-UL'
        elif lab in ['TOP']: lab = 'TOP'
        elif lab in ['TOPULTOPv1']: lab = 'TOP-UL (v1)'
        elif lab in ['TOPULTOPv2']: lab = 'TOP-UL (v2)'
        elif lab in ['TOPUL4TOPv1']: lab = '4TOP-UL (v1)'
        elif lab in ['TOPUL4TOPv2']: lab = '4TOP-UL (v2)'
        elif lab in ['TOPULTOPPUPv1']: lab = 'TOP-UL (PUPv1)'
        elif lab in ['TOPULTOPPUPv2']: lab = 'TOP-UL (PUPv2)'
        elif lab in ['TOPUL4TOPPUPv1']: lab = '4TOP-UL (PUPv1)'
        elif lab in ['TOPUL4TOPPUPv2']: lab = '4TOP-UL (PUPv2)'
        elif lab in ['TOPULTOPTAUFLIPv1']: lab = 'TOP-UL (TAUFLIPv1)'
        elif lab in ['TOPULTOPTAUFLIPv2']: lab = 'TOP-UL (TAUFLIPv2)'
        elif lab in ['TOPUL4TOPTAUFLIPv1']: lab = '4TOP-UL (TAUFLIPv1)'
        elif lab in ['TOPUL4TOPTAUFLIPv2']: lab = '4TOP-UL (TAUFLIPv2)'

        ax.plot(bkgEff, sigEff, linewidth=3, label=lab)
        
    params = {'legend.fontsize': 'x-large'}
    pylab.rcParams.update(params)
 
    for wp in s.WPNames[options.chan]: ax.plot(eff[name[-1]][sel][wp][treeNames[1]], eff[name[-1]][sel][wp][treeNames[0]], markersize=8, marker="o", label=wp)

    if options.chan in ['elec']: ax.text(0.2, 0.9, 'Electrons, p_{T} > 25 GeV', fontsize=13)
    else: ax.text(0.2, 0.9, 'Muons, p_{T} > 25 GeV', fontsize=13)
    
    legend = ax.legend(loc='lower right', fontsize=16, scatterpoints=1, frameon=False, numpoints=1)
    legend.get_frame().set_linewidth(0.0)
    
    ax.set(xlabel='Background efficiency', ylabel='Signal efficiency', title='')
    ax.set_xticks(numpy.arange(0.0001, 1., 0.005))
    ax.set_yticks(numpy.arange(0.5, 1., 0.05))
    ax.grid(which='both')
    
    ax.set_xscale('log')
    ax.set_xlim(0.001, 1)
    ax.set_ylim(0.8, 1)
    
    ax.plot([effCutBased[sel]['4TOP'][treeNames[1]]], [effCutBased[sel]['4TOP'][treeNames[0]]], marker='*', markersize=3, color="red")
    
#    if options.chan in ['elec']: ax.plot([0.005], [0.68], marker='*', markersize=3, color="red")
#    else: ax.plot([0.006], [0.83], marker='*', markersize=3, color="red")

    fig.savefig(figDir+'/roc_'+sel+'.pdf')
    pyplot.close()

def drawEff(effp, errp, chan, figDir, sel, mvaname):

    for p in effp:
        
        fig, ax = pyplot.subplots()
        
        for iwp, wp in enumerate(s.WPNames[chan]):
        
            var, eff, err = [], [], []
            for ib in effp[p][wp][chan+'Prompt']:
                eff.append(effp[p][wp][chan+'Prompt'][ib])
                err.append(errp[p][wp][chan+'Prompt'][ib])
                if ib == 0: bc = s.Bins[p][ib+1]
                else: bc = (s.Bins[p][ib]+s.Bins[p][ib+1])/2.
                var.append(bc)
                
            ax.errorbar(var, eff, err, linewidth=3, label=wp)
        
        params = {'legend.fontsize': 'x-large'}
        pylab.rcParams.update(params)

        xlab = 0.7
        if p in ['eta']: xlab = 0.5
        if chan in ['elec']: ax.text(xlab, 0.7, 'Electrons', fontsize=13, transform=ax.transAxes)
        else: ax.text(xlab, 0.7, 'Muons', fontsize=13, transform=ax.transAxes)
    
        legend = ax.legend(loc='lower right', fontsize=16, scatterpoints=1, frameon=False, numpoints=1)
        legend.get_frame().set_linewidth(0.0)
    
        xlab = ''
        if p in ['pt']: xlab = '$p_{T}$ [GeV]'
        elif p in ['eta']: xlab = 'Preudorapidity'
        elif p in ['nvertex']: xlab = 'Number of reconstucted vertices'
        ax.set(xlabel=xlab, ylabel='Efficiency', title='')
        ax.grid(which='both')
    
        if p in ['pt']:
            ax.set_xlim(0., 100.)
            ax.set_ylim(0., 1.)
        elif p in ['eta']:
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(0., 1.)
        elif p in ['nvertex']:
            ax.set_xlim(0., 60.)
            ax.set_ylim(0., 1.)

        fig.savefig(figDir+'/eff_'+mvaname+'_'+chan+'_'+p+'_'+sel+'.pdf')
        pyplot.close()

def drawDisc(disc, name, figDir, sel):

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
    
    c1.Print(figDir+'/disc_'+name+'_'+sel+'.pdf')
    c1.Clear()
    
if __name__ == '__main__':
    
    options = main()
    
    ROOT.gROOT.SetBatch(1)
    
#    prompt = ['Prompt', 'PromptFlip']
    prompt = ['Prompt']
    if options.chan == 'elec': nonprompt = ['NonpromptHF', 'NonpromptLF', 'NonpromptConv', 'NonpromptPileup']
    else: nonprompt = ['NonpromptHF', 'NonpromptLF', 'NonpromptPileup']
    
    treeNames = [options.chan+'Prompt', options.chan+'Nonprompt']
    finputPrompt = glob.glob(options.prompt)
    finputNonprompt = glob.glob(options.nonprompt)
    fsig, fbkg1 = [], []
    for p in prompt: fsig += [f+':'+options.chan+p for f in finputPrompt]
    for p in nonprompt: fbkg1 += [f+':'+options.chan+p for f in finputNonprompt]
    sig = uproot4.lazy(fsig)
    bkg1 = uproot4.lazy(fbkg1)
    print('Signal='+str(len(sig))+', Background='+str(len(bkg1)))
    tree = {}
    tree[treeNames[0]] = sig[:options.nmax]
    tree[treeNames[1]] = bkg1[:options.nmax]
    
    weight, pt, eta, nvertex = (array( 'f',  [0.]) for _ in range(4))
    leptonMva = [array( 'f',  [0.]) for _ in range(len(options.mva.split(',')))]
    passedPresel = array( 'b',  [False])
    
    chan = options.chan.capitalize()
    
    pref = 'leptonMva'
    mvas = options.mva.split(',')
    vsel = options.pt.split(',')

    hist, histAll = {}, {}
    for sel in vsel:
        hist[sel], histAll[sel] = {}, {}
        for tr in treeNames:
            hist[sel][tr], histAll[sel][tr] = {}, {}

    for i in mvas:
        for sel in vsel:
            for ih, h in enumerate([hist[sel].items(), histAll[sel].items()]):
                for k, v in h:
                    if ih == 0:
                        if 'v1' not in i and 'v2' not in i: v[i] = ROOT.TH1F(i+'_'+sel+'_'+k+'_'+str(ih), i+'_'+sel+'_'+k+'_'+str(ih), 10000, -1.2, 1.2)
                        else: v[i] = ROOT.TH1F(i+'_'+sel+'_'+k+'_'+str(ih), i+'_'+sel+'_'+k+'_'+str(ih), 10000, -0.2, 1.2)
                    else:
                        if 'v1' not in i and 'v2' not in i: v[i] = ROOT.TH1F(i+'_'+sel+'_'+k+'_'+str(ih), i+'_'+sel+'_'+k+'_'+str(ih), 1, 0.5, 1.5)
                        else: v[i] = ROOT.TH1F(i+'_'+sel+'_'+k+'_'+str(ih), i+'_'+sel+'_'+k+'_'+str(ih), 1, 0.5, 1.5)

    eff = {}
    for i in mvas:
        eff[i] = {}
        for sel in vsel:
            eff[i][sel] = {}
            for wp in s.WPNames[options.chan]:
                eff[i][sel][wp] = {}
                for tr in treeNames:
                    eff[i][sel][wp][tr] = 0

    effCutBased = {}
    for sel in vsel:
        effCutBased[sel] = {}
        for wp in ['4TOP']:
            effCutBased[sel][wp] = {}
            for tr in treeNames:
                effCutBased[sel][wp][tr] = 0
                    
    effp, effpErr = {}, {}
    for i in mvas:
        effp[i], effpErr[i] = {}, {}
        for sel in vsel:
            effp[i][sel], effpErr[i][sel] = {}, {}
            for p in ['pt', 'eta', 'nvertex']:
                effp[i][sel][p], effpErr[i][sel][p] = {}, {}
                for wp in s.WPNames[options.chan]:            
                    effp[i][sel][p][wp], effpErr[i][sel][p][wp] = {}, {}
                    for tr in treeNames:
                        effp[i][sel][p][wp][tr], effpErr[i][sel][p][wp][tr] = {}, {}
                        for iv, v in enumerate(s.Bins[p]):
                            if iv == len(s.Bins[p])-1: continue
                            effp[i][sel][p][wp][tr][iv] = 0
                            effpErr[i][sel][p][wp][tr][iv] = 0
                            
    np, npPass = {}, {}
    for i in mvas:
        np[i], npPass[i] = {}, {}
        for sel in vsel:
            np[i][sel], npPass[i][sel] = {}, {}
            for tr in treeNames:
                np[i][sel][tr], npPass[i][sel][tr] = {}, {}
                for p in ['pt', 'eta', 'nvertex']:
                    np[i][sel][tr][p], npPass[i][sel][tr][p] = {}, {}
                    for iv, v in enumerate(s.Bins[p]):
                        if iv == len(s.Bins[p])-1: continue
                        np[i][sel][tr][p][iv] = 0.
                        npPass[i][sel][tr][p][iv] = []
                        for wp in s.WPNames[options.chan]:
                            npPass[i][sel][tr][p][iv].append(0.)
        
    print('Fill histograms ..')
    for ktr, tr in tree.items():

        var = ['weight', 'pt', 'eta', 'nvertex', 'passedPresel', 'isLeptonMva4TOP'] + ['leptonMva'+i for i in mvas]
        trr = tr[var]
        res = dict()
        for sub in trr:
            for v in var: res[v] = trr[v]
        df = pd.DataFrame(res)        
        iw = [0. for i in range(len(vsel))]

        ie = 0        
        for ev in range(0, len(df)):

            dfe = df.iloc[ev]
            weight[0] = dfe['weight']
            pt[0] = dfe['pt']
            eta[0] = dfe['eta']
            nvertex[0] = dfe['nvertex']
            passedPresel[0] = dfe['passedPresel']
            for imva, i in enumerate(mvas): leptonMva[imva][0] = dfe['leptonMva'+i]
            
            w = weight[0]

            for iptcfg, ptcfg in enumerate(vsel):
                        
                if ptcfg == 'pt25toInf' and pt[0] < 25.: continue
                elif ptcfg == 'pt10to25' and pt[0] > 25.: continue
                elif ptcfg == 'pt10toInf' and pt[0] < 10.: continue
                
                iw[iptcfg] += 1

                for iwp, wp in enumerate(['4TOP']):
                    if bool(dfe['isLeptonMva4TOP']):
                        effCutBased[ptcfg][wp][ktr] += 1
                
                for imva, i in enumerate(mvas):
                    
                    pred = leptonMva[imva][0]
                    passSel = bool((('v2' in i) or (options.presel and passedPresel[0]) or (not options.presel)))
                    if passSel: hist[ptcfg][ktr][i].Fill(pred)
                    else: pred = -100
                    histAll[ptcfg][ktr][i].Fill(1.)

                    for iwp, wp in enumerate(s.WPNames[options.chan]):
                        if bool(pred > s.WPs[i][options.chan][iwp]):
                            eff[i][ptcfg][wp][ktr] += 1
                            
                    for ib, b in enumerate(s.Bins['pt']):
                        if ib == len(s.Bins['pt'])-1: continue
                        if pt[0] > s.Bins['pt'][ib] and pt[0] < s.Bins['pt'][ib+1]:
                            np[i][ptcfg][ktr]['pt'][ib] += 1
                            for iwp, wp in enumerate(s.WPs[i][options.chan]):
                                if pred > wp: npPass[i][ptcfg][ktr]['pt'][ib][iwp] += 1
                            break
                    for ib, b in enumerate(s.Bins['eta']):
                        if ib == len(s.Bins['eta'])-1: continue
                        if eta[0] > s.Bins['eta'][ib] and eta[0] < s.Bins['eta'][ib+1]:
                            np[i][ptcfg][ktr]['eta'][ib] += 1
                            for iwp, wp in enumerate(s.WPs[i][options.chan]):
                                if pred > wp: npPass[i][ptcfg][ktr]['eta'][ib][iwp] += 1
                            break
                    for ib, b in enumerate(s.Bins['nvertex']):
                        if ib == len(s.Bins['nvertex'])-1: continue
                        if nvertex[0] > s.Bins['nvertex'][ib] and nvertex[0] < s.Bins['nvertex'][ib+1]:
                            np[i][ptcfg][ktr]['nvertex'][ib] += 1
                            for iwp, wp in enumerate(s.WPs[i][options.chan]):
                                if pred > wp: npPass[i][ptcfg][ktr]['nvertex'][ib][iwp] += 1
                            break

        for mva in mvas:
            for isel, sel in enumerate(vsel):
                for wp in s.WPNames[options.chan]:
                    if iw[isel] > 0: eff[mva][sel][wp][ktr] /= float(iw[isel])
                    else: eff[mva][sel][wp][ktr] = 0.
            
                for p in np[mva][sel][ktr]:
                    for ib in np[mva][sel][ktr][p]:
                        nAll = np[mva][sel][ktr][p][ib]
                        for iwp, wp in enumerate(s.WPNames[options.chan]):
                            effp[mva][sel][p][wp][ktr][ib], effpErr[mva][sel][p][wp][ktr][ib] = computeEff(npPass[mva][sel][ktr][p][ib][iwp], nAll-npPass[mva][sel][ktr][p][ib][iwp], math.sqrt(npPass[mva][sel][ktr][p][ib][iwp]), math.sqrt(nAll-npPass[mva][sel][ktr][p][ib][iwp]))

        for isel, sel in enumerate(vsel):
            for wp in ['4TOP']:
                if iw[isel] > 0: effCutBased[sel][wp][ktr] /= float(iw[isel])
                else: effCutBased[sel][wp][ktr] = 0.
                            
    figDir = options.output+'pics'
    if os.path.isdir(figDir):
        os.system("rm -rf "+figDir)
    os.system("mkdir "+figDir)
        
    print('Produce ROCs ..')
    roc = []
    for sel in vsel:
        roc.append([])
        for mva in mvas:
            roc[-1].append(makeRoc(hist[sel][treeNames[0]][mva], hist[sel][treeNames[1]][mva], histAll[sel][treeNames[0]][mva], histAll[sel][treeNames[1]][mva]))
            pickle.dump(roc[-1][-1], open(figDir+'/roc_'+mva+'_'+sel+'.pkl', 'wb'))
            for wp in s.WPNames[options.chan]: pickle.dump(eff[mva][sel][wp], open(figDir+'/WP_'+mva+'_'+wp+'_'+sel+'.pkl', 'wb'))
            pickle.dump({'eff': effp[mva][sel], 'err': effpErr[mva][sel]}, open(figDir+'/eff_'+mva+'_'+sel+'.pkl', 'wb'))
        pickle.dump({'eff': effCutBased[sel]}, open(figDir+'/effCutBased_'+sel+'.pkl', 'wb'))

    print('Plot results ..')
    for isel, sel in enumerate(vsel):
        drawRoc(roc[isel], mvas, figDir, eff, sel, effCutBased)
        for i in mvas:
            drawEff(effp[i][sel], effpErr[i][sel], options.chan, figDir, sel, i)

    for sel in vsel:
        for i in mvas:
            disc = {}
            disc['prompt'] = hist[sel][treeNames[0]][i]
            disc['nonprompt'] = hist[sel][treeNames[1]][i]
            drawDisc(disc, i, figDir, sel)
    
    print('\033[92mDone\033[0;0m')
