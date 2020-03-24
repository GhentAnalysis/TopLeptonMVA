#! /usr/bin/env python

import os
import sys
import xml.etree.ElementTree as ET
import subprocess

TreeMaker = '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/'

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
    parser.add_option("-p","--path",default="jobs",help="output directory [default: %default]")
    parser.add_option("-m","--mva",default="TOP",help="MVA name to train [default: %default]")
    parser.add_option("-c","--chan",default="muon",help="lepton type [default: %default]")
    parser.add_option("-y","--year",default="2016",help="year of data taking [default: %default]")
    parser.add_option("-d","--definition",\
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

if __name__ == '__main__':

    options = main()

    os.system('cp /tmp/'+c.proxy+' '+c.proxydir+c.proxy)

    home = os.getcwd()

    outpath = home+'/'+options.path

    if os.path.isdir(outpath):
        os.system('rm -rf '+outpath)

    os.system('mkdir '+outpath)
    
    walltime = '36:00:00'
    
    sets = options.definition.split(',')
    
    for i in sets:
        print i
        os.system('mkdir '+outpath+'/'+i)
        outname = outpath+'/'+i+'/'
        outlog = outname+i+'.log'
        
        NoErrors = False
        while NoErrors is False:
            try:
                res = subprocess.Popen(('qsub',\
                '-N','TopLeptonMVATrain',\
                '-q',c.batchqueueHighMem,\
                '-o',outlog,'-j','oe','job.sh',\
                '-l','walltime='+walltime,\
                '-v','dout='+home+',outname='+outname+',definition='+i+',year='+options.year+',mva='+options.mva+',chan='+options.chan+',proxy='+c.proxydir+c.proxy+',arch='+c.arch), \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = res.communicate()
                NoErrors = ('Invalid credential' not in err)
                if not NoErrors: print '.. Resubmitted'
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
