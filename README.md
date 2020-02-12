# TopLeptonMVA

Lepton MVA ID for the top quark analyses

Setup for production of training data sets:
```
git clone https://github.com/GhentAnalysis/TopLeptonMVA
cd TopLeptonMVA/TreeMaker
./makeTree.sh
```

Cluster submission:
```
./submit.py
```

Setup for MVA training and optimisation:
```
git clone https://github.com/wverbeke/deepLearning
```
Follow the instructions mentioned on this page.
