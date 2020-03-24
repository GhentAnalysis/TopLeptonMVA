#! /usr/bin/env python

import os
import sys
import subprocess

TreeMaker = '/user/kskovpen/analysis/LeptonMVA/CMSSW_10_2_20/src/TopLeptonMVA/TreeMaker/'

sys.path.append(TreeMaker)
import common as c

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    home = os.getcwd()

    usage = "usage: %prog [options]\n Script to submit ROC jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("-d","--dir",default="jobs",help="output directory [default: %default]")
    parser.add_option("-m","--mva",default="TTH,TZQ,TOP",help="MVA name to train [default: %default]")
    parser.add_option("-n","--nmax",default="1000000",help="max number of events [default: %default]")
    parser.add_option("-c","--chan",default="muon",help="lepton type [default: %default]")
    parser.add_option("-p","--pt",default="pt25toInf",help="pt selection [default: %default]")
    parser.add_option("-t","--test",default="test",help="test file [default: %default]")
    parser.add_option("-y","--year",default="2016",help="year of data taking [default: %default]")

    (options, args) = parser.parse_args(sys.argv[1:])

    return options

if __name__ == '__main__':

    options = main()

    os.system('cp /tmp/'+c.proxy+' '+c.proxydir+c.proxy)

    home = os.getcwd()

    outpath = home+'/'+options.dir+'/'

    if os.path.isdir(outpath):
        os.system('rm -rf '+outpath)

    os.system('mkdir '+outpath)

    walltime = '03:00:00'

    outlog = outpath+'roc.log'
        
    NoErrors = False
    while NoErrors is False:
        try:
            res = subprocess.Popen(('qsub',\
            '-N','TopLeptonMVAROC',\
            '-q',c.batchqueue,\
            '-o',outlog,'-j','oe','job.sh',\
            '-l','walltime='+walltime,\
            '-v','dout='+home+',outpath='+outpath+',year='+options.year+',testt='+options.test+',pt='+options.pt+',mva='+options.mva+',chan='+options.chan+',nmax='+options.nmax+',proxy='+c.proxydir+c.proxy+',arch='+c.arch), \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = res.communicate()
            NoErrors = ('Invalid credential' not in err)
            if not NoErrors: print '.. Resubmitted'
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass
