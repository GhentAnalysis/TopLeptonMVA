#!/usr/bin/env python

import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import htcondor
import common as c

from optparse import OptionParser

def main(argv = None):

    if argv == None:
        argv = sys.argv[1:]

    home = os.getcwd()

    usage = "usage: %prog [options]\n Script to submit Analyzer jobs to batch"

    parser = OptionParser(usage)
    parser.add_option("--files", default="10", help="number of files per job [default: %default]")
    parser.add_option("--xml", default="samples_UL18.xml", help="input xml configuration [default: %default]")
    parser.add_option("--out", default="jobs_train_UL18_splitfine", help="output directory [default: %default]")
#    parser.add_option("--out", default="jobs_train_UL17_all", help="output directory [default: %default]")
#    parser.add_option("--nmax", default="20000", help="number of processed events per job [default: %default]")
    parser.add_option("--nmax", default="-1", help="number of processed events per job [default: %default]")
    parser.add_option("--year", default="2018", help="year of the data taking [default: %default]")
    parser.add_option("--split", action="store_true", help="split into prompt and nonprompt [default: %default]")
    parser.add_option("--splitfine", action="store_true", help="split into classes [default: %default]")
    parser.add_option("--modelxgb",
    default="TOP-UL.TOP_v1,\
TOP-UL.4TOP_v1,\
TOP-UL.TOP_v2,\
TOP-UL.4TOP_v2,\
TOP-UL.TOP_TAUFLIPv1,\
TOP-UL.4TOP_TAUFLIPv1,\
TOP-UL.TOP_TAUFLIPv2,\
TOP-UL.4TOP_TAUFLIPv2", 
    help="model file (xgboost) [default: %default]")
    parser.add_option("--modeltmva", default="TOP", help="model file (TMVA) [default: %default]")
    
    (options, args) = parser.parse_args(sys.argv[1:])

    return options

def job(sample, tag, xml, output, home, wdir, fsh):

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
    
    j += "cd "+wdir+"\n"
    j += "python "+home+"/makeTree.py --sample "+sample+" --year "+options.year+" --tag "+tag+" --xml "+xml+" --output "+output+" --nmax "+options.nmax+(" --split " if options.split else "")+(" --splitfine " if options.splitfine else "")+(" --modelxgb="+options.modelxgb if options.modelxgb != "" else "")+(" --modeltmva="+options.modeltmva if options.modeltmva != "" else "")+"\n"
    
    with open(fsh, 'w') as f:
        f.write(j)
            
    os.system('chmod u+x '+fsh)
            
if __name__ == '__main__':

    options = main()

    home = os.getcwd()

    outpath = home+"/"+options.out

    if os.path.isdir(outpath):
        os.system("rm -rf "+outpath)

    os.system("mkdir "+outpath)

    year = options.year
    
    submitList = c.submit2016
    if year == '2016APV': submitList = c.submit2016APV
    elif year == '2017': submitList = c.submit2017
    elif year == '2018': submitList = c.submit2018

    nJobs = 0
    
    xmlTree = ET.parse(options.xml)
    for s in xmlTree.findall('sample'):
        for s0, t0, sig, lep, process, channel, train, test in submitList:
            sname = s.get('id')
            stag = s.get('tag')
            if sname == s0 and stag == t0:
                files=[]
                for child in s:
                    files.append(child.text)

                jname = sname+'_'+stag
                
                nj = 0
                fjobname = []
                fjobtag = []
                fjobid = []
                fjobxml = []

                if os.path.isdir(outpath+"/"+jname):
                    os.system("rm -rf "+outpath+"/"+jname)
                os.system("mkdir "+outpath+"/"+jname)

                xml = outpath+"/"+jname+"/"+jname+"_"+str(nj)+".xml"
                fout = open(xml,"w+")
                fjobname.append(jname)
                fjobtag.append(stag)
                fjobid.append(str(nj))
                fjobxml.append(xml)
                fout.write('<data>\n')
                fout.write("<sample id=\""+jname+"\" tag=\""+stag+"\">\n")
                nc = 0
#                files2read = int(frac*len(files))
                files2read = int(len(files))
                for i in range(files2read):

                    nc = nc + 1

                    fout.write("    <file>"+files[i]+"</file>\n")

                    if (nc > int(options.files)-1):
                        fout.write("</sample>\n")
                        fout.write("</data>")
                        fout.close()

                        if (i != (len(files)-1)):
                            nc = 0
                            nj = nj + 1

                            xml = outpath+"/"+jname+"/"+jname+"_"+str(nj)+".xml"
                            fout = open(xml,"w+")
                            fjobname.append(jname)
                            fjobtag.append(stag)
                            fjobid.append(str(nj))
                            fjobxml.append(xml)
                            fout.write('<data>\n')
                            fout.write("<sample id=\""+jname+"\" tag=\""+stag+"\">\n")
                            
                if (nc <= int(options.files)-1):
                    fout.write("</sample>\n")
                    fout.write("</data>")
                    fout.close()
                    
                schedd = htcondor.Schedd()
                jid = 0
                
                for fidx, f in enumerate(fjobname):
                    print f, fjobid[jid]
                    outname = outpath+'/'+f+'/'+f+'_'+fjobid[jid]
                    outdir = outpath+'/'+f+'/'
                    outlog = outname+'.log'
                    output = outname+'.root'

                    job(fjobname[jid], fjobtag[jid], fjobxml[jid], output, home, outdir, outname+'.sh')
                
                    js = htcondor.Submit({\
                    "executable": outname+'.sh', \
                    "output": outname+'.out', \
                    "error": outname+'.err', \
                    "log": outname+'.log' \
                    })
                
                    with schedd.transaction() as shd:
                        cluster_id = js.queue(shd)

                    jid = jid + 1

                nJobs += jid
                
    print 'Total number of jobs submitted =', nJobs

