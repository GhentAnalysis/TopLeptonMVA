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

    usage = "usage: %prog [options]\n Script to submit xgboost jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("--path", default="jobs", help="output directory [default: %default]")
    parser.add_option("--chan", default="elec", help="lepton type [default: %default]")
    parser.add_option("--year", default="2017", help="year of data taking [default: %default]")
    parser.add_option("--cpu", default=1, help="number of cpus [default: %default]")
    parser.add_option("--definition", default="n_estimators-2000__max_depth-4__eta-0.1__gamma-5__min_child_weight-500", help="BDT definition [default: %default]")
    parser.add_option("--cv", action="store_true", help="Perform cross validation [default: %default]")
    parser.add_option("--presel", action="store_true", help="Apply preselection [default: %default]")
    parser.add_option("--version", default="v1", help="Version to train (v1, v2, PUPv1, PUPv2, TAUv1, TAUv2, TAUPUPv1, TAUPUPv2) [default: %default]")
    parser.add_option("--objective", default="logitraw", help="Logistic response (logistic, logitraw) [default: %default]")
    parser.add_option("--config", default="4TOP", help="Training configuration (TOP, 4TOP) [default: %default]")
    parser.add_option("--nmax", type=int, default=100000, help="Maximum number of events to be used either for training or testing [default: %default]")

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
    
    j += "source /user/kskovpen/analysis/LeptonID/CMSSW_10_6_28/src/LeptonID/TopLeptonMVA/Train/xgboost/setup.sh\n"

    j += "cd "+output+"\n"
    j += "python3 "+home+"/./train.py --path "+output+" --config "+options.config+" --nmax "+str(options.nmax)+" --version "+options.version+" --objective "+options.objective+" --definition "+definition+" --chan "+options.chan+" --year "+options.year+(" --cv " if options.cv else "")+(" --presel " if options.presel else "")+"\n"

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
    
    sets = options.definition.split(',')
    
    schedd = htcondor.Schedd()
    
    for i in sets:

        print options.chan+':', options.config, options.version, i
        os.system('mkdir '+outpath+'/'+i)
        outname = outpath+'/'+i+'/'+i
        outlog = outname+'.log'

        job(i, outname, home, outpath+'/'+i+'/', i, outname+'.sh')
        
        js = htcondor.Submit({\
        "executable": outname+'.sh', \
        "request_cpus": options.cpu, \
        "output": outname+'.out', \
        "error": outname+'.err', \
        "log": outname+'.log' \
        })
        
        with schedd.transaction() as shd:
            cluster_id = js.queue(shd)
