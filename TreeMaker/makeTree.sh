#!/bin/env bash

nmax=1000

xml="test.xml"

python makeTree.py \
--output=output.root \
--xml=${xml} \
--nmax=${nmax} \
--sample=TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 \
--model="weights/elec2016.bin" \
--tag=crab_MiniAOD2016v3_ext1-v2_TopLeptonMVA_2016
