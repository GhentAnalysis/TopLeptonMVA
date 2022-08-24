#!/usr/bin/env python

import ROOT
import math
import numpy as np

import style

lep = 'muon' # elec or muon
nmax = 100000

var = ['miniIso', 'missHits', 'sip3d', 'dxy', 'dz', 'POGMedium']
cut = [0.4, 1.5, 8, 0.05, 0.1, 1.]

prompteff, nonprompteff, prompttot, nonprompttot = (np.zeros(len(cut)) for _ in range(4))

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

hPrompt = {}
hNonPrompt = {}

hPrompt['miniIso'] = ROOT.TH1F('hPrompt_miniIso', 'hPrompt_miniIso', 100, 0., 1.0)
hNonPrompt['miniIso'] = ROOT.TH1F('hNonPrompt_miniIso', 'hNonPrompt_miniIso', 100, 0., 1.0)

hPrompt['missHits'] = ROOT.TH1F('hPrompt_missHits', 'hPrompt_missHits', 5, -0.5, 4.5)
hNonPrompt['missHits'] = ROOT.TH1F('hNonPrompt_missHits', 'hNonPrompt_missHits', 5, -0.5, 4.5)

hPrompt['sip3d'] = ROOT.TH1F('hPrompt_sip3d', 'hPrompt_sip3d', 100, 0., 20.0)
hNonPrompt['sip3d'] = ROOT.TH1F('hNonPrompt_sip3d', 'hNonPrompt_sip3d', 100, 0., 20.0)

hPrompt['dxy'] = ROOT.TH1F('hPrompt_dxy', 'hPrompt_dxy', 100, 0., 0.1)
hNonPrompt['dxy'] = ROOT.TH1F('hNonPrompt_dxy', 'hNonPrompt_dxy', 100, 0., 0.1)

hPrompt['dz'] = ROOT.TH1F('hPrompt_dz', 'hPrompt_dz', 100, 0., 0.3)
hNonPrompt['dz'] = ROOT.TH1F('hNonPrompt_dz', 'hNonPrompt_dz', 100, 0., 0.3)

hPrompt['POGMedium'] = ROOT.TH1F('hPrompt_POGMedium', 'hPrompt_POGMedium', 2, 0., 2.)
hNonPrompt['POGMedium'] = ROOT.TH1F('hNonPrompt_POGMedium', 'hNonPrompt_POGMedium', 2, 0., 2.)

f = ROOT.TFile.Open('tZq_2016_nocuts.root')
trPrompt = f.Get(lep+'Prompt')
trNonPrompt = f.Get(lep+'NonPrompt')

for it, t in enumerate([trPrompt, trNonPrompt]):
    
    iev = 0
    
    for ev in t:

        if iev > nmax and nmax >= 0: break
        
        for iv, v in enumerate(var):
            
            vv = eval('ev.'+v)
            
            if v in ['sip3d', 'dxy', 'dz']: vv = math.fabs(vv)
            
            if v not in ['POGMedium']:
                
                if it == 0:
                    if vv < cut[iv]: prompteff[iv] += 1
                    prompttot[iv] += 1
                else:
                    if vv < cut[iv]: nonprompteff[iv] += 1
                    nonprompttot[iv] += 1

            else:
                
                if it == 0:
                    if vv == cut[iv]: prompteff[iv] += 1
                    prompttot[iv] += 1
                else:
                    if vv == cut[iv]: nonprompteff[iv] += 1
                    nonprompttot[iv] += 1
                    
            if it == 0: hPrompt[v].Fill(vv)
            else: hNonPrompt[v].Fill(vv)
    
            iev += 1

for iv, v in enumerate(var):
    
    c1 = ROOT.TCanvas()
    
    addbin(hPrompt[v])
    addbin(hNonPrompt[v])
    
    hPrompt[v].Scale(1./hPrompt[v].Integral())
    hNonPrompt[v].Scale(1./hNonPrompt[v].Integral())

    hmax = max(hPrompt[v].GetMaximum(), hNonPrompt[v].GetMaximum())*1.2
    hPrompt[v].SetMaximum(hmax)
    
    hPrompt[v].SetMinimum(0.)
    
    hPrompt[v].Draw('hist e1')
    hPrompt[v].SetMarkerSize(0.7)
    hPrompt[v].SetMarkerStyle(20)
    hPrompt[v].GetXaxis().SetTitle(v)
    hPrompt[v].GetYaxis().SetTitle('Normalized to unity')
    hNonPrompt[v].SetMarkerSize(0.7)
    hNonPrompt[v].SetMarkerStyle(24)
    hNonPrompt[v].SetMarkerColor(ROOT.kRed)
    hNonPrompt[v].SetLineColor(ROOT.kRed)
    hNonPrompt[v].Draw('hist e1 same')
    
    c = ROOT.TLine(cut[iv], 0., cut[iv], hmax)
    c.SetLineStyle(2)
    c.SetLineWidth(2)
    c.SetLineColor(ROOT.kRed)
    c.Draw()

    leffprompt = ROOT.TLatex(0.45,0.85,"#varepsilon_{pass}(prompt) = %.2f %%" % (float(prompteff[iv])/float(prompttot[iv])*100.))
    leffprompt.SetNDC(); leffprompt.SetTextFont(43); leffprompt.SetTextSize(20); leffprompt.Draw()
    leffnonprompt = ROOT.TLatex(0.45,0.75,"#varepsilon_{pass}(nonprompt) = %.2f %%" % (float(nonprompteff[iv])/float(nonprompttot[iv])*100.))
    leffnonprompt.SetNDC(); leffnonprompt.SetTextFont(43); leffnonprompt.SetTextSize(20); leffnonprompt.Draw()

    leg = ROOT.TLegend(0.82,0.92,0.990,0.75)
    leg.SetFillColor(253)
    leg.SetBorderSize(0)
    leg.AddEntry(hPrompt[v],"Prompt","lp")
    leg.AddEntry(hNonPrompt[v],"Nonprompt","lp")
    leg.Draw()

    c1.Print('pics/'+v+'.pdf')
    c1.Clear()
