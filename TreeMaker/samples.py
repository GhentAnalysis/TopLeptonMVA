#!/usr/bin/env python

import os
import sys
import ROOT

from optparse import OptionParser

def main(argv = None):
    
    if argv == None:
        argv = sys.argv[1:]
        
    usage = "usage: %prog [options]\n Script to create a list of ntuples"

    parser = OptionParser(usage)
    parser.add_option('--path', default='maite.iihe.ac.be/pnfs/iihe/cms/store/user/kskovpen/LeptonID', help='storage path [default: %default]')
    parser.add_option('--year', default='UL16APV', help='year of data taking [default: %default]')

    (options, args) = parser.parse_args(sys.argv[1:])

    return options                                            

if __name__ == '__main__':
    
    options = main()

    fout = open('samples_'+options.year+'.xml','w+')
    fout.write('<data>\n')

    ntPath = options.path+'/'+options.year
    
    gfal = 'eval `scram unsetenv -sh`; '

    dlist = os.popen(gfal+'gfal-ls srm://'+ntPath+'/').read().splitlines()

    for i in dlist:
        cpath = gfal+'gfal-ls srm://'+ntPath+'/'+i
        d1 = os.popen(cpath).read().splitlines()
        for i1 in d1:
            if options.year not in i1: continue
            d2 = os.popen(cpath+'/'+i1).read().splitlines()
            if len(d2) != 1:
                print('Several runs found in', i)
                exit
            files = []
            stats = 0
            for i2 in d2:
                d3 = os.popen(cpath+'/'+i1+'/'+i2).read().splitlines()
                for i3 in d3:
                    d3 = os.popen(cpath+'/'+i1+'/'+i2+'/'+i3).read().splitlines()
                    for i4 in d3:
                        if i4.find('.root') != -1:
                            fname = "root://"+ntPath+'/'+i+'/'+i1+'/'+i2+'/'+i3+'/'+i4
                            files.append("        <file>"+fname+"</file>\n")
            fout.write("    <sample id=\""+i+"\" tag=\""+i1+"\">\n")
            for f in files:
                fout.write(f)
            fout.write("    </sample>\n")

    fout.write("</data>")

    fout.close()
