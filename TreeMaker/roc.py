#! /usr/bin/env python

import os
import sys
import ROOT

import matplotlib.pyplot as pyplot
pyplot.switch_backend('agg')

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Script to produce ROCs"
                        
    parser = OptionParser(usage)
    parser.add_option("-m","--mva",default="Top,TTH,tZq",help="input list of MVAs [default: %default]")
    parser.add_option("-n","--nmax",default=-1,help="max number of events [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

# ROCs inspired by https://github.com/GhentAnalysis/ttg/blob/playground/fancyPlots/makeROC.py
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
    
    legend = ax.legend(loc='lower right', fontsize=8, scatterpoints=1)        
    legend.get_frame().set_linewidth(0.0)
    
    ax.set(xlabel='background efficiency', ylabel='signal efficiency', title='')
    ax.grid()
    
    ax.set_xscale('log')
    ax.set_xlim(0.0001, 1)
    ax.set_ylim(0.3, 1)
    
    fig.savefig(figDir+'/roc.pdf')
    pyplot.close()
    
if __name__ == '__main__':
    
    options = main()

    tree = {}
    
    for i in ['elecPrompt','elecNonPrompt','muonPrompt','muonNonPrompt']:
        tree[i] = ROOT.TChain(i)
    
    for k, v in tree.iteritems():
        v.Add('input.root')

    pref = 'leptonMva'
    mvas = options.mva.split(',')
        
    hist = {'elecPrompt':{}, 'elecNonPrompt':{}, 'muonPrompt':{}, 'muonNonPrompt':{}}

    for i in mvas:
        for k, v in hist.iteritems():
            v[i] = ROOT.TH1F(i+'_'+k, i+'_'+k, 100000, -1.0, 1.2)

    print 'Fill histograms ..'
    for ktr, tr in tree.iteritems():
        ie = 0
        for ev in tr:
            ie = ie + 1
            if (ie > int(options.nmax) and (int(options.nmax) >= 0)):
                break
            pt = eval('ev.pt')
            if pt < 25: continue
            for i in mvas:
                pred = eval('ev.'+pref+i)
                hist[ktr][i].Fill(pred)

    print 'Produce ROCs ..'
    roc = []
    for i in mvas:
        roc.append(makeRoc(hist['elecPrompt'][i],hist['elecNonPrompt'][i]))

    print 'Plot results ..'
    figDir = 'pics'
    if os.path.isdir(figDir):
        os.system("rm -rf "+figDir)
    os.system("mkdir "+figDir)
        
    drawRoc(roc,mvas,figDir)
    
    print '\033[92mDone\033[0;0m'
