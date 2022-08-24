#! /usr/bin/env python

import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import htcondor

TreeMaker = '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/'

import sys
sys.path.append(TreeMaker)
import common as c

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    home = os.getcwd()

    usage = "usage: %prog [options]\n Script to submit MVA jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("--path", default="jobs", help="output directory [default: %default]")
    parser.add_option("--mva", default="TOP", help="MVA name to train [default: %default]")
    parser.add_option("--chan", default="muon", help="lepton type [default: %default]")
    parser.add_option("--year", default="2017", help="year of data taking [default: %default]")
    parser.add_option("--definition",\
    default="cuts100_depth3_trees100_shrinkage0p1,\
cuts200_depth3_trees200_shrinkage0p1,\
cuts200_depth4_trees200_shrinkage0p1,\
cuts200_depth3_trees500_shrinkage0p1,\
cuts200_depth4_trees500_shrinkage0p1,\
cuts200_depth4_trees1000_shrinkage0p1,\
cuts100_depth4_trees1000_shrinkage0p1\
",help="BDT definition [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

def job(jname, outname, home, output, definition, fsh):

    j = "#!/bin/bash\n\n"
    
    j += "export X509_USER_PROXY="+c.proxy+"\n"
    
    j += "echo \"Start: $(/bin/date)\"\n"
    j += "echo \"User: $(/usr/bin/id)\"\n"
    j += "echo \"Node: $(/bin/hostname)\"\n"
    j += "echo \"CPUs: $(/bin/nproc)\"\n"
    j += "echo \"Directory: $(/bin/pwd)\"\n"
    
    j += "source /cvmfs/cms.cern.ch/cmsset_default.sh\n"
    
    j += "cd "+home+"\n"
    
    j += "export SCRAM_ARCH=slc7_amd64_gcc820\n"
    j += "eval `scramv1 runtime -sh`\n"

    j += "cd "+output+"\n"
    j += "python "+home+"/./train.py --path "+output+" --definition "+definition+" --mva "+options.mva+" --chan "+options.chan+" --input train_"+options.year+".root"+"\n"
    
    with open(fsh, 'w') as f:
        f.write(j)
        
    os.system('chmod u+x '+fsh)

if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    outpath = home+'/'+options.path

    if os.path.isdir(outpath):
        os.system('rm -rf '+outpath)

    os.system('mkdir '+outpath)
    
    walltime = '36:00:00'
    
    sets = options.definition.split(',')
    
    schedd = htcondor.Schedd()
    
    for i in sets:
        
        print i
        os.system('mkdir '+outpath+'/'+i)
        outname = outpath+'/'+i+'/'+i
        outlog = outname+'.log'

        job(i, outname, home, outpath+'/'+i, i, outname+'.sh')
        
        js = htcondor.Submit({\
        "executable": outname+'.sh', \
        "output": outname+'.out', \
        "error": outname+'.err', \
        "log": outname+'.log' \
        })
        
        with schedd.transaction() as shd:
            cluster_id = js.queue(shd)
