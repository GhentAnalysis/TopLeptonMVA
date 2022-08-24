#!/bin/env python

import os, sys

year = ['2016APV', '2016', '2017', '2018']
#year = ['2016APV']
nmax = 200000
#proc = ['ttbar', 'tttt', 'ttw', 'ttz', 'tth', 'tzq']
proc = ['ttbar']

#mva = ['TOP', 'TOPULTOPv1', 'TOPULTOPv2', 'TOPUL4TOPv1', 'TOPUL4TOPv2']
mva = ['TOP', 'TOPULTOPv1', 'TOPULTOPv2']

sel = 'pt10toInf,pt25toInf,pt10to25'

dry = False
presel = True

outdir = 'rocs'
os.system('rm -rf '+outdir+'; mkdir '+outdir)

for y in year:

    yn = y.replace('20', 'UL')
    
    outdir = 'rocs/'+yn
    os.system('rm -rf '+outdir+'; mkdir '+outdir)

#    fpath = '/pnfs/iihe/cms/store/user/kskovpen/LeptonIDTrain/jobs_train_'+yn+'_splitfine'
    fpath = '/pnfs/iihe/cms/store/user/kskovpen/LeptonIDTrainCutBased/jobs_train_'+yn+'_splitfine'
    ttbarn = 'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_crab_MiniAOD'+y
    ttbarv = 'v1' if yn in ['UL16', 'UL16APV'] else 'v2'
    ttttv = 'v2'
    ttwv = 'v2' if yn in ['UL16APV'] else 'v1'
    ttzv = 'v2' if yn in ['UL18'] else 'v1'
    tthv = 'v2'
    tzqv = 'v2' if yn in ['UL18'] else 'v1'
    
    for p in proc:
        
        outdir = 'rocs/'+yn+'/'+p
        os.system('rm -rf '+outdir+'; mkdir '+outdir)
    
        if p == 'ttbar':
            testPrompt = '\"'+fpath+'/'+ttbarn+'-'+ttbarv+'_'+yn+'/'+ttbarn+'-'+ttbarv+'_'+yn+'_*.root\"'
        elif p == 'tttt': 
            ttttn = 'TTTT_TuneCP5_13TeV-amcatnlo-pythia8_crab_MiniAOD'+y
            testPrompt = '\"'+fpath+'/'+ttttn+'-'+ttttv+'_'+yn+'/'+ttttn+'-'+ttttv+'_'+yn+'_*.root\"'
        elif p == 'ttz':
            ttzn = 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_crab_MiniAOD'+y
            testPrompt = '\"'+fpath+'/'+ttzn+'-'+ttzv+'_'+yn+'/'+ttzn+'-'+ttzv+'_'+yn+'_*.root\"'
        elif p == 'ttw':
            ttwn = 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_crab_MiniAOD'+y
            testPrompt = '\"'+fpath+'/'+ttwn+'-'+ttwv+'_'+yn+'/'+ttwn+'-'+ttwv+'_'+yn+'_*.root\"'
        elif p == 'tth':
            tthn = 'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_crab_MiniAOD'+y
            testPrompt = '\"'+fpath+'/'+tthn+'-'+tthv+'_'+yn+'/'+tthn+'-'+tthv+'_'+yn+'_*.root\"'
        elif p == 'tzq':
            tzqn = 'tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8_crab_MiniAOD'+y
            testPrompt = '\"'+fpath+'/'+tzqn+'-'+tzqv+'_'+yn+'/'+tzqn+'-'+tzqv+'_'+yn+'_*.root\"'
        testNonprompt = '\"'+fpath+'/'+ttbarn+'-'+ttbarv+'_'+yn+'/'+ttbarn+'-'+ttbarv+'_'+yn+'_*.root\"'
    
        for l in ['elec', 'muon']:
            
            rname = 'test_'+l+'_'+p+'_'+yn
            odir = outdir+'/'+l
            print rname
        
            os.system('rm -rf '+odir+'; mkdir '+odir)
            os.system('./submit.py --mva='+','.join(mva)+' --chan='+l+' --nmax='+str(nmax)+' --dir='+odir+' --pt='+sel+' --prompt='+testPrompt+' --nonprompt='+testNonprompt+' --year='+y+(' --dry' if dry else '')+(' --presel' if presel else ''))
