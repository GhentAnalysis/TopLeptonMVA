#! /usr/bin/env python

import os
import sys
import ROOT

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
                    
    usage = "usage: %prog [options]\n Script to produce plots with MVA overtraining checks"

    parser = OptionParser(usage)
    parser.add_option("-m","--mva",default="TOP",help="MVA name [default: %default]")
    parser.add_option("-n","--nmax",default=100000,help="max number of events [default: %default]")
    parser.add_option("-c","--chan",default="elec",help="channel [default: %default]")
    parser.add_option("-y","--year",default="2016",help="year of data taking [default: %default]")
    parser.add_option("-d","--definition",default="cuts200_depth4_trees1000_shrinkage0p1",help="hyperparameters [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])
    
    return options

if __name__ == '__main__':
    
    options = main()

    f = ROOT.TFile.Open('../'+options.chan+'_'+options.mva+'_'+options.year+'/'+options.definition+'/output.root')

    train = f.Get("dataset/TrainTree")
    test = f.Get("dataset/TestTree")

    h_train = ROOT.TH1F('h_train', 'h_train', 100, -1.2, 1.2)
    h_test = ROOT.TH1F('h_test', 'h_test', 100, -1.2, 1.2)

    for idx, tr in enumerate([train,test]):
        for iev, ev in enumerate(tr):
            if iev > options.nmax and options.nmax > 0: break
            disc = eval('ev.BDTG_'+options.definition+'_'+options.chan)
            if idx == 0: h_train.Fill(disc)
            else: h_test.Fill(disc)

    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
                
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    c1 = ROOT.TCanvas()

    h_train.SetLineColor(ROOT.kRed)
    h_train.SetFillColorAlpha(ROOT.kRed,0.5)
    h_test.SetLineColor(ROOT.kBlue)
    h_test.SetFillColorAlpha(ROOT.kBlue,0.5)
    
    h_train.Draw()
    h_test.Draw('same hist e1p')
    
    h_train.GetXaxis().SetTitle('Discriminant')
    
    leg = ROOT.TLegend(0.55,0.80,0.65,0.70)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(h_train,"Train","f")
    leg.AddEntry(h_test,"Test","f")
    leg.Draw()

    c1.Print('pics/overtrain.pdf')
