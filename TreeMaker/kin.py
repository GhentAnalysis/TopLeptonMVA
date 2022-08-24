#!/usr/bin/env python

import ROOT
import math
import numpy as np

import style

lep = ['elec', 'muon']
nmax = 100000

var = ['drMin', 'relIso']
tit = ['Minimum #DeltaR(lepton,jet)', 'Relative isolation']

def addbin(h):
    
    x_nbins = h.GetXaxis().GetNbins()
    h.SetBinContent(1, h.GetBinContent(0)+h.GetBinContent(1))
    h.SetBinError(1, ROOT.TMath.Sqrt(ROOT.TMath.Power(h.GetBinError(0), 2)+ROOT.TMath.Power(h.GetBinError(1), 2)))
    h.SetBinContent(x_nbins, h.GetBinContent(x_nbins)+h.GetBinContent(x_nbins+1))
    h.SetBinError(x_nbins, ROOT.TMath.Sqrt(ROOT.TMath.Power(h.GetBinError(x_nbins), 2)+ROOT.TMath.Power(h.GetBinError(x_nbins+1), 2)))
    
    h.SetBinContent(0,0.)
    h.SetBinError(0,0.)
    h.SetBinContent(x_nbins+1, 0.)
    h.SetBinError(x_nbins+1, 0.)

ROOT.gROOT.SetBatch(1)

pstyle = style.SetPlotStyle(1, 'FIT')

hTTTT = {}
hTTZ = {}

hTTTT['drMin'] = ROOT.TH1F('hTTTT_drMin', 'hTTTT_drMin', 100, 0., 5.0)
hTTZ['drMin'] = ROOT.TH1F('hTTZ_drMin', 'hTTZ_drMin', 100, 0., 5.0)

hTTTT['relIso'] = ROOT.TH1F('hTTTT_relIso', 'hTTTT_relIso', 100, 0., 0.5)
hTTZ['relIso'] = ROOT.TH1F('hTTZ_relIso', 'hTTZ_relIso', 100, 0., 0.5)

ftttt = ROOT.TFile.Open('TTTT_2016.root')
trTTTT_elec = ftttt.Get(lep[0]+'Prompt')
trTTTT_muon = ftttt.Get(lep[1]+'Prompt')

fttz = ROOT.TFile.Open('ttZ_2016.root')
trTTZ_elec = fttz.Get(lep[0]+'Prompt')
trTTZ_muon = fttz.Get(lep[1]+'Prompt')

for it, t in enumerate([trTTTT_elec, trTTTT_muon, trTTZ_elec, trTTZ_muon]):
    
    iev = 0

    nL = 0
    evcur = -1
    for ev in t:

        if iev > nmax and nmax >= 0: break
        nL += 1
        
#        eventNb = eval('ev.eventNb')

#        if eventNb != evcur:
        
            if nL > 0:
                for iv, v in enumerate(var):
                
                    vv = eval('ev.'+v)
                
                    if it < 2: hTTTT[v].Fill(vv)
                    else: hTTZ[v].Fill(vv)
                
            iev += 1
                
#            evcur = eventNb
            nL = 0

for iv, v in enumerate(var):
    
    c1 = ROOT.TCanvas()
    
    addbin(hTTTT[v])
    addbin(hTTZ[v])
    
    hTTTT[v].Scale(1./hTTTT[v].Integral())
    hTTZ[v].Scale(1./hTTZ[v].Integral())

    hmax = max(hTTTT[v].GetMaximum(), hTTZ[v].GetMaximum())*1.2
    hTTTT[v].SetMaximum(hmax)

    hTTTT[v].SetMinimum(0.0001)
    
    hTTTT[v].Draw('hist e1')
    hTTTT[v].SetMarkerSize(0.7)
    hTTTT[v].SetMarkerStyle(20)
    hTTTT[v].GetXaxis().SetTitle(tit[iv])
    hTTTT[v].GetYaxis().SetTitle('Normalized to unity')
    hTTZ[v].SetMarkerSize(0.7)
    hTTZ[v].SetMarkerStyle(24)
    hTTZ[v].SetMarkerColor(ROOT.kRed)
    hTTZ[v].SetLineColor(ROOT.kRed)
    hTTZ[v].Draw('hist e1 same')

    leg = ROOT.TLegend(0.82,0.92,0.990,0.75)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(hTTTT[v],"4-top","lp")
    leg.AddEntry(hTTZ[v],"ttZ","lp")
    leg.Draw()
    
    c1.SetLogy(1)

    c1.Print('pics/'+v+'.pdf')
    c1.Clear()
