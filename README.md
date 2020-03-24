# TopLeptonMVA

Lepton MVA ID for top quark analyses

Install code:
```
git clone https://github.com/GhentAnalysis/TopLeptonMVA
```

Setup for production of training data sets:
```
cd TopLeptonMVA/TreeMaker
./makeTree.sh
```

Setup for MVA training and optimisation:
```
cd TopLeptonMVA/Train
./train.py
```

Cluster submission for tree production and training is implemented in
respective package:
```
./submit.py
```

