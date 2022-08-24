#!/bin/env python

import os

#cv = ' --cv'
cv = ''
nmax = 4000000
presel = ''
vers = ['v1', 'v2', 'PUPv1', 'PUPv2', 'TAUFLIPv1', 'TAUFLIPv2']
objective = 'logistic'
#objective = 'logitraw'

run = ['muon_2016APV','elec_2016APV']
configs = ['TOP', '4TOP']

os.system('rm -rf jobs; mkdir jobs')

for r in run:
    
    chan = r.split('_')[0]
    year = r.split('_')[1]
    
    for t in configs:

        for v in vers:
        
            path = 'jobs/'+t+'_'+v+'_'+chan+'_'+year+'/'
            
            os.system('rm -rf '+path)
            os.system('./submit.py --chan='+chan+' --config='+t+' --nmax='+str(nmax)+' --version='+v+' --objective='+objective+' --path='+path+' --year='+year+cv+presel)
