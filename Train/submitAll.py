#!/bin/env python

import os

run = ['muon_TOP_2016','elec_TOP_2016']

for r in run:
    
    chan = r.split('_')[0]
    mva = r.split('_')[1]
    year = r.split('_')[2]
    
    path = chan+'_'+mva+'_'+year
    
    os.system('rm -rf '+path)
    os.system('./submit.py --mva='+mva+' --chan='+chan+' --path='+path+' --year='+year)
