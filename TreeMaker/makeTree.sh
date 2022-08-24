#!/bin/env bash

nmax=20

#xml="test.xml"
xml="local.xml"
#split="--splitfine"
split=""
#split="--split"
modelxgb="TOP-UL.TOP_v1,TOP-UL.TOP_v2"
#modelxgb=""
modeltmva="TOP"
year="2018"

python makeTree.py \
--output=output.root \
${split} \
--xml=${xml} \
--nmax=${nmax} \
--year=${year} \
--sample=TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8 \
--modelxgb=${modelxgb} \
--modeltmva=${modeltmva} \
--tag=crab_MiniAOD2017-v2_UL17
