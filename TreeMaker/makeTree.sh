#!/bin/env bash

nmax=1000

python makeTree.py \
--output=output.root \
--nmax=${nmax} \
--sample=TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8 \
--model="weights/elec2016.bin" \
--tag=crab_MiniAOD2016v3-v1_leptonMVA_2016
