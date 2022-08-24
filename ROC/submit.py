#!/usr/bin/env python

import os
import sys
import subprocess
import htcondor

TreeMaker = '/user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/TreeMaker/'

sys.path.append(TreeMaker)
import common as c

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    home = os.getcwd()

    usage = "usage: %prog [options]\n Script to submit ROC jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("--dir", default="jobs", help="output directory [default: %default]")
    parser.add_option("--mva", default="TOPUL,TOP", help="MVA name to train [default: %default]")
    parser.add_option("--nmax", default="100000", help="max number of events [default: %default]")
    parser.add_option("--chan", default="muon", help="lepton type [default: %default]")
    parser.add_option("--pt", default="pt25toInf", help="pt selection [default: %default]")
    parser.add_option("--prompt", default="test", help="test file [default: %default]")
    parser.add_option("--nonprompt", default="test", help="test file [default: %default]")
    parser.add_option("--year", default="2017", help="year of data taking [default: %default]")
    parser.add_option("--dry", action="store_true", help="dry run [default: %default]")
    parser.add_option("--presel", action="store_true", help="Apply preselection [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

def job(home, outpath, fsh):

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
    
    j += "source /user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/setup.sh\n"

    j += "cd "+outpath+"\n"

    j += "time "+home+"/./roc.py --output "+outpath+" --pt "+options.pt+" --mva "+options.mva+" --chan "+options.chan+" --nmax "+options.nmax+" --prompt \""+options.prompt+"\" --nonprompt \""+options.nonprompt+"\" --year "+options.year+(" --presel" if options.presel else "")
    
    with open(fsh, 'w') as f:
        f.write(j)
        
    os.system('chmod u+x '+fsh)

if __name__ == '__main__':

    options = main()
    
    home = os.getcwd()

    outpath = home+'/'+options.dir+'/'

    if os.path.isdir(outpath):
        os.system('rm -rf '+outpath)

    os.system('mkdir '+outpath)

    outname = outpath+'job'
    
    schedd = htcondor.Schedd()

    job(home, outpath, outname+'.sh')

    if not options.dry:
        
        js = htcondor.Submit({\
        "executable": outname+'.sh', \
        "output": outname+'.out', \
        "error": outname+'.err', \
        "log": outname+'.log' \
        })
        
        with schedd.transaction() as shd:
            cluster_id = js.queue(shd)
            
