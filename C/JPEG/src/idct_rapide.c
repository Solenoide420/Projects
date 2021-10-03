#include "idct_rapide.h"


// IDCT scaling factors
const float m0=2.0*0.9238795325;
const float m1=2.0*0.7071067812;
const float m3=2.0*0.7071067812;
const float m5=2.0*0.3826834324;
const float m2=m0-m5;
const float m4=m0+m5;

const float s0=0.3535533906;
const float s1=0.9807852805/2.0;
const float s2=0.9238795325/2.0;
const float s3=0.8316696123/2.0;
const float s4=0.7071067812/2.0;
const float s5=0.555570233/2.0;
const float s6=0.3826834324/2.0;
const float s7=0.195190322/2.0;

void idct_1_dimension(int16_t* vecteur){
  //colonne a
  const float a0 = vecteur[0]*s0;
  const float a1 = vecteur[4]*s4;
  const float a2 = vecteur[2]*s2;
  const float a3 = vecteur[6]*s6;
  const float a4 = vecteur[5]*s5;
  const float a5 = vecteur[1]*s1;
  const float a6 = vecteur[7]*s7;
  const float a7 = vecteur[3]*s3;
  //colonne b
  const float b0=a0;
  const float b1=a1;
  const float b2=a2;
  const float b3=a3;
  const float b4=a4-a7;
  const float b5=a5+a6;
  const float b6=a5-a6;
  const float b7=a4+a7;
  //colonne c
  const float c0=b0;
  const float c1=b1;
  const float c2=b2-b3;
//  const float c3=b2+b3;
  const float c4=b4;
  const float c5=b5-b7;
  const float c6=b6;
  const float c7=b5+b7;
  const float c8=b4+b6;
  //colonne d
  const float d0=c0;
  const float d1=c1;
  const float d2=c2*m1;
  const float d3=c2;
  const float d4=c4*m2;
  const float d5=c5*m3;
  const float d6=c6*m4;
  const float d7=c7;
  const float d8=c8*m5;
  //clonne e
  const float e0=d0+d1;
  const float e1=d0-d1;
  const float e2=d2-d3;
  const float e3=d3;
  const float e4=d4+d8;
  const float e5=d5+d7;
  const float e6=d6-d8;
  const float e7=d7;
  const float e8=e5-e6;
  //collonne f
  const float f0=e0+e3;
  const float f1=e1+e2;
  const float f2=e1-e2;
  const float f3=e0-e3;
  const float f4=e4-e8;
  const float f5=e8;
  const float f6=e6-e7;
  const float f7=e7;

  vecteur[0]=f0+f7;
  vecteur[1]=f1+f6;
  vecteur[2]=f2+f5;
  vecteur[3]=f3+f4;
  vecteur[4]=f3-f4;
  vecteur[5]=f2-f5;
  vecteur[6]=f1-f6;
  vecteur[7]=f0-f7;
}

//Arai Agui and Nakajima algorithme (appliqué 2 fois sur les colonnes et sur les lignes)
void iDCT_AAN(uint8_t** final_bloc ,int16_t** frequentiel ){

//sur les colonnes-------------------------------
int16_t* vecteur=malloc(sizeof(int16_t)*8);
for (uint8_t i = 0; i < 8; i++) {
    // 1-extraction de la colonne
  for (uint8_t j = 0; j < 8; j++) {
    vecteur[j] = frequentiel[j][i];
  }
    // 2-invertion
  idct_1_dimension(vecteur);
    // 3-cette boucle pour ecrire le resultat ds les colonne de frequentiel
  for (uint8_t j = 0; j < 8; j++) {
     frequentiel[j][i]=vecteur[j] ;
  }}
free(vecteur);

//mnt sur les lignes------------------------------
for (uint8_t i = 0; i < 8; i++) {
    idct_1_dimension(frequentiel[i]);
  }

//former le final_bloc-----------------------------
for (uint8_t i = 0; i < 8; i++) {

  for (uint8_t j = 0; j < 8; j++) {


      frequentiel[i][j] += 128;
      if ((int) (frequentiel[i][j])< 0) {

          final_bloc[i][j] = 0;
      } else if ((int)frequentiel[i][j] > 255) {
          final_bloc[i][j] = 255;
      } else {

          final_bloc[i][j] = (int) (frequentiel[i][j]);

      }
  }
}

}

//__________________________________________________


 float*  get_cos_tab(){
   float* cos_tab=malloc(64*sizeof(float));
   for (int8_t u = 0; u < 8; u++) {
     const float c=(u==0)?(1.0/(sqrt(2.0)*2.0)):1.0/2.0;
     for (int8_t x = 0; x < 8; x++) {
         cos_tab[u * 8 + x]=c*cos((2.0*x+1.0)*u*M_PI/16.0);}
     }
   return (cos_tab);}


void iDCT_plus_rapide(uint8_t** final_bloc,int16_t** frequentiel,const float* const idctMap){
  float result[64];
  //idct pour chaque colonne
  for (uint8_t i = 0; i < 8; i++) {
      for (uint8_t y = 0; y < 8; y++) {
        float sum = 0.0;
        for (uint8_t v = 0; v< 8; v++) {
          sum+=frequentiel[v][i]*idctMap[v*8+y];
        }
        result[y*8+i]=sum;}}
  // et mnt les lignes
  for (uint8_t i = 0; i < 8; i++) {
      for (uint8_t x = 0; x < 8; x++) {
        float sum = 0.0;
        for (uint8_t u = 0; u< 8; u++) {
                sum+=result[i*8+u]*idctMap[u*8+x];
              }
              sum+=128;
              if ((int) roundf(sum) < 0) {
                  final_bloc[i][x] = 0;
              } else if ((int) roundf(sum) > 255) {
                  final_bloc[i][x] = 255;
              } else {
        final_bloc[i][x]=(int) roundf(sum);
      }}}}

void iDCT_meilleur(uint8_t** final_bloc,int16_t** frequentiel,const float* const idctMap){
  float tmp[64];
  for (uint8_t k = 0; k < 64; k++) {
      tmp[k] = 0;
  }

  for (uint8_t i = 0; i < 8; i++) {
      for (uint8_t j = 0; j < 8; j++) {
          for (uint8_t lbda = 0; lbda < 8; lbda++) {
              for (uint8_t mu = 0; mu < 8; mu ++) {
                  tmp[8*i + j] += idctMap[lbda*8+i] * idctMap[mu*8+j]  * frequentiel[lbda][mu];
              }
          }
      }
  }

  for (uint8_t i = 0; i < 8; i++) {
      for (uint8_t j = 0; j < 8; j++) {
          tmp[8*i + j] += 128;
          if (tmp[8*i + j] < 0) {
              final_bloc[i][j] = 0;
          } else if (tmp[8*i + j] > 255) {
              final_bloc[i][j] = 255;
          } else {
              final_bloc[i][j] = (int) roundf(tmp[8*i + j]);
          }
      }
  }}
