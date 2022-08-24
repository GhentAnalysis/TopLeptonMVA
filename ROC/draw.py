#!/bin/env python3

import os, sys
import pickle
import numpy
from collections import OrderedDict

import settings as s
#from roc import drawEff

import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
pyplot.switch_backend('agg')

#proc = ['ttbar', 'tttt', 'ttw', 'ttz', 'tth', 'tzq']
proc = ['ttbar']
#year = ['2016APV', '2016', '2017', '2018']
year = ['2017']
lep = ['elec', 'muon']
wpd = ['TOP', 'TOPULTOPv1', 'TOPULTOPv2']

pt = '25'
sel = 'pt'+pt+'toInf'
#sel = 'pt10to25'

disc = ['TOP', 'TOPULTOPv1', 'TOPULTOPv2']
tit = ['TOP', 'TOP-UL', 'TOP-UL (v2)']
col = ['blue', 'red', 'green']
sty = ['--', '-', '-']

os.system('rm -rf pics; mkdir pics')

for y in year:
    
    yn = y.replace('20', 'UL')
    
    for pi, p in enumerate(proc):
        
        procd = proc[pi]

        for l in lep:
            
            j = 'rocs/'+yn+'/'+p+'/'+l

            wpsCutBased = OrderedDict()
            with open(j+'/pics/effCutBased_'+sel+'.pkl','rb') as fid:
                wpsCutBased = pickle.load(fid)['eff']
            
            rocs, wps = (OrderedDict() for _ in range(2))

            wps[p], rocs[p] = OrderedDict(), OrderedDict()
        
            for d in disc:
                
                wps[p][d] = OrderedDict()
                
                with open(j+'/pics/roc_'+d+'_'+sel+'.pkl','rb') as fid:
                    rocs[p][d] = pickle.load(fid)

                for wp in s.WPNames[l]:
                    with open(j+'/pics/WP_'+d+'_'+wp+'_'+sel+'.pkl','rb') as fid:
                        wps[p][d][wp] = pickle.load(fid)

            fig, ax = pyplot.subplots()

            rc = [d for d in rocs[p].values()]
            for ir, r in enumerate(rc):
        
                sigEff = [i[1] for i in r]
                bkgEff = [i[2] for i in r]
                
                lab = tit[ir]
                
                ax.plot(bkgEff, sigEff, linewidth=3, label=lab, color=col[ir], linestyle=sty[ir])                
        
            params = {'legend.fontsize': 'x-large', 'axes.titlesize': 72}
            pylab.rcParams.update(params)

            wpc = pylab.rcParams['axes.prop_cycle'].by_key()['color']
            for iw, w in enumerate(wpd):
                for iwp, wp in enumerate(s.WPNames[l]):
                    lab = wp if iw == 1 else ''
                    wpsize = 8 if w != 'TOP' else 4
                    ax.plot(wps[procd][w][wp][l+'Nonprompt'], wps[procd][w][wp][l+'Prompt'], markersize=wpsize, marker="o", label=lab, color=wpc[iwp])
                    print(w, yn, l, wp, 'Nonprompt =', wps[procd][w][wp][l+'Nonprompt'], 'Prompt =', wps[procd][w][wp][l+'Prompt'])
                    
            ax.plot(wpsCutBased['4TOP'][l+'Nonprompt'], wpsCutBased['4TOP'][l+'Prompt'], markersize=wpsize, marker="X", label='EPJC 80 (2020) 75', color='black')

            legend = ax.legend(loc='lower right', fontsize=12, scatterpoints=1, frameon=False, numpoints=1)
            legend.get_frame().set_linewidth(0.0)

            if sel not in ['pt10to25']:
                if l in ['elec']: ax.text(0.05, 0.90, 'Electrons, $\mathrm{p_{T}}$ > '+pt+' GeV', fontsize=12, transform=ax.transAxes)
                else: ax.text(0.05, 0.90, 'Muons, $\mathrm{p_{T}}$ > '+pt+' GeV', fontsize=12, transform=ax.transAxes)
            else:
                if l in ['elec']: ax.text(0.05, 0.90, 'Electrons, 10 < $\mathrm{p_{T}}$ < 25 GeV', fontsize=12, transform=ax.transAxes)
                else: ax.text(0.05, 0.90, 'Muons, 10 < $\mathrm{p_{T}}$ < 25 GeV', fontsize=12, transform=ax.transAxes)
    
            ax.set_xlabel(xlabel='Nonprompt lepton efficiency', fontsize=14)
            ax.set_ylabel(ylabel='Prompt lepton efficiency', fontsize=14)
            ax.set_xticks(numpy.arange(0.001, 1., 0.005))
#            ax.set_yticks(numpy.arange(0.7, 1., 0.05))
            ax.set_yticks(numpy.arange(0.4, 1., 0.05))
            ax.grid(which='both')
    
            ax.set_xscale('log')
            ax.set_xlim(0.001, 1)
#            ax.set_ylim(0.7, 1)
            ax.set_ylim(0.8, 1)
            if sel in ['pt10to25']:
                ax.set_ylim(0.4, 1)
            
            fig.savefig('pics/roc_'+l+'_'+p+'_'+yn+'_'+sel+'.pdf')
            pyplot.close()
    
#            eff = {}

#            for d in disc:
        
#                with open(j+'_'+procd+'/'+sample+'_'+l+'_'+year+'/pics/eff_'+d+'_'+sel+'.pkl','rb') as fid:
#                    eff[l] = pickle.load(fid)
#            
#                fig, ax = pyplot.subplots()
#        
#                drawEff(eff[l]['eff'], eff[l]['err'], l, os.getcwd()+'/pics', sel, d)
