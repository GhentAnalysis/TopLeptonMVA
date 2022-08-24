#include <xgboost/c_api.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <iostream>
#include <iomanip>

int main()
{
   BoosterHandle booster;
   const char *model_path = "../weights/TOP_v1_muon_2017/n_estimators-2000__max_depth-4__eta-0.1__gamma-5__min_child_weight-500/xgb.bin";
   XGBoosterCreate(NULL, 0, &booster);
//   XGBoosterSetParam(booster, "seed", "0");
   XGBoosterLoadModel(booster, model_path);

   unsigned int nrow = 1;
   unsigned int nfeat = 13;
   float feat[nrow][nfeat];
   float pt = 19.666318893432617;
   float eta = -1.1915535926818848;
   float trackMultClosestJet = 2.0;
   float miniIsoCharged = 0.0;
   float miniIsoNeutral = 0.006281548645347357;
   float pTRel = 5.878333568572998;
   float ptRatio = 0.7104586362838745;
   float relIso = 0.0;
   float bTagClosestJet = 0.05092625319957733;
   float sip3d = 0.8536405563354492;
   float dxylog = -6.844289779663086;
   float dzlog = -7.0496039390563965;
   float idSeg = 0.9697104692459106;
   feat[0][0] = pt;
   feat[0][1] = eta;
   feat[0][2] = trackMultClosestJet;
   feat[0][3] = miniIsoCharged;
   feat[0][4] = miniIsoNeutral;
   feat[0][5] = pTRel;
   feat[0][6] = ptRatio;
   feat[0][7] = relIso;
   feat[0][8] = bTagClosestJet;
   feat[0][9] = sip3d;
   feat[0][10] = dxylog;
   feat[0][11] = dzlog;
   feat[0][12] = idSeg;
   
   DMatrixHandle dtest;
   XGDMatrixCreateFromMat(reinterpret_cast<float*>(feat), nrow, nfeat, NAN, &dtest);
   
   bst_ulong out_len;
   const float *f;
//   const char **out;
   
//   XGBoosterGetAttrNames(booster, &out_len, &out);
//   for (const char* c = *out; c; c=*++out)
//   std::cout << *out << std::endl;
   
   XGBoosterPredict(booster, dtest, 0, 0, &out_len, &f);
   assert(out_len == nrow);
   std::cout << std::setprecision(10) << f[0] << std::endl;
   
   XGDMatrixFree(dtest);
   XGBoosterFree(booster);
}
