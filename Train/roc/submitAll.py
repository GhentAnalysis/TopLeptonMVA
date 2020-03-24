#!/bin/env python

import os

year = ['2016', '2017', '2018']
test = ['tZq','ttZ','ttW','ttg','ttH']

run = []
for y in year:
    run.extend(['elec_TOP_pt25toInf_'+y,'elec_TOP_pt0to25_'+y,'muon_TOP_pt25toInf_'+y,'muon_TOP_pt0to25_'+y])

for t in test:
    for r in run:
    
        chan = r.split('_')[0]
        mva = r.split('_')[1]
        pt = r.split('_')[2]
        year = r.split('_')[3]
        
        outdir = t+'_'+r
        print outdir
        
        os.system('rm -rf '+outdir)
        os.system('./submit.py --mva='+mva+' --chan='+chan+' --dir='+outdir+' --pt='+pt+' --test='+t+'_'+year+' --year='+year)
