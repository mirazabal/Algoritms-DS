#include <stdio.h>
#include <string.h>

#define MAX(a,b) ((a) > (b) ? a : b)
#define MIN(a,b) ((a) < (b) ? a : b)

/* Computing of the maximal suffix for <= */
int maxSuf(const char *x, int m, int *p) {
   int ms, j, k;
   char a, b;

   ms = -1;
   j = 0;
   k = *p = 1;
   while (j + k < m) {
      a = x[j + k];
      b = x[ms + k];
      if (a < b) {
         j += k;
         k = 1;
         *p = j - ms;
      }
      else
         if (a == b)
            if (k != *p)
               ++k;
            else {
               j += *p;
               k = 1;
            }
         else { /* a > b */
            ms = j;
            j = ms + 1;
            k = *p = 1;
         }
   }
   return(ms);
}


/* Computing of the maximal suffix for >= */
int maxSufTilde(const char *x, int m, int *p) {
   int ms, j, k;
   char a, b;

   ms = -1;
   j = 0;
   k = *p = 1;
   while (j + k < m) {
      a = x[j + k];
      b = x[ms + k];
      if (a > b) {
         j += k;
         k = 1;
         *p = j - ms;
      }
      else
         if (a == b)
            if (k != *p)
               ++k;
            else {
               j += *p;
               k = 1;
            }
         else { /* a < b */
            ms = j;
            j = ms + 1;
            k = *p = 1;
         }
   }
   return(ms);
}

/* Two Way string matching algorithm. */
void TW(const char *x, int m, const char *y, int n) {
   int i, j, ell, memory, p, per, q;

   /* Preprocessing */
   i = maxSuf(x, m, &p);
   j = maxSufTilde(x, m, &q);
   if (i > j) {
      ell = i;
      per = p;
   }
   else {
      ell = j;
      per = q;
   }

   /* Searching */
   if (memcmp(x, x + per, ell + 1) == 0) {
      j = 0;
      memory = -1;
      while (j <= n - m) {
         i = MAX(ell, memory) + 1;
         while (i < m && x[i] == y[i + j])
            ++i;
         if (i >= m) {
            i = ell;
            while (i > memory && x[i] == y[i + j])
               --i;
            if (i <= memory)
               fprintf(stdout, "Found pattern at pos = %d \n" , j);
               //OUTPUT(j);
            j += per;
            memory = m - per - 1;
         }
         else {
            j += (i - ell);
            memory = -1;
         }
      }
   }
   else {
      per = MAX(ell + 1, m - ell - 1) + 1;
      j = 0;
      while (j <= n - m) {
         i = ell + 1;
         while (i < m && x[i] == y[i + j])
            ++i;
         if (i >= m) {
            i = ell;
            while (i >= 0 && x[i] == y[i + j])
               --i;
            if (i < 0)
               fprintf(stdout, "Found pattern at pos = %d \n" , j);
               //OUTPUT(j);
            j += per;
         }
         else
            j += (i - ell);
      }
   }
}


int main()
{
  //const char* pattern = "ABAABABAABAABA";
//  const char* pattern = "AAA";
  //const char* pattern = "ABCD";
  //const char* pattern = "ABABAB";
//  const char* pattern = "CABRON";
//  const char* pattern = "ABCDEF";
//  const char* pattern = "ZMZA";
  //const char* pattern = "ABAABAA";
  //const char* pattern = "GCAGAGAG";
//  const char* pattern = "GCGAGAGAG";
//const char* pattern = "0c5b8f279a64baabbe3400000800450005dc41bb40003f067f43ac100001c0a808641451a468fcae454ec839eaa48010020099ce00000101080aabbe4332af25f32e74fdbb775d6f7dd3a2aa2f0feefce436e601fca0d0b135ccd48229d3cf57a043545bbbb1ca38846ce2b47bd0b060079661033731b46cfd88ee265bbe7dfb01d156bc8320f4078dd7bb08a76c68ae02c9b139fa65a5f7ed941e48529b43536d9910f0ba04f747dbb34f831fb8312181e35b7c4800733694917ee62dc23a9a5b4a8a154e815c2a34acad5364de75e5c1d0610ad0d5406566be4b9380852ddccfb7f11e394e486dfaf5c15ed336439506a59fd67adf3be09d87741e0ca1fadc59ebfa923942ff3337c0910af6d59ffc7a3ed3f41d0ed4bb9548d9a2ead37e43be78d5f8bad42bf195bdfb8b929b880cd95b00f769d4b2ff1d8ba1075e1f4a1c971f1451f3404288fd3d148fd89c9bb2f79ba9606f5b5f8ce60093441fdd60b6fc7507f0b54978b2878c415f28dc111f77ba80e615df73fbe0063fffe4a0b6e015bdd0ca07497c8ed5bdedfe99ff1d10b99df6cf7d69ca5d700a5c54aa1234bfd00589d74e056523c252215b513f6b0bdc61da59cba4b63bae138f5825c317f5c8a0cc16a5313a67845bc2d59a2de0778fbad05a5f87950d9a2466bfe77db5b01e81c6c3b3002b375ced0cf61bed6daaa73e0406c599145fbd7a1ea4f7d35415551bd9081b043f77f14b6e0c38dbb6e019bae6de53fa3d10745cb56c2f098184245a8c405ecbb75017255c4f01132f1acd16f9211036318592e6f1c2f0724614cdd3542b9e0c7bb531d80532eb344db84a46d95b7c0be00ff1d1d1e14317f610ea4a3c8956b73e888f43ba7a780733c24d0c1dca17fdd909ceaaea12c1e022ac2b5e3581167309a5b7c4202fcb53f1195f0fe3770cbc80db666aed274b0fd3766e08f7847c012933c54962909c53a9fc628c736f48f34aae5d37d6a846a91eb4b216382e176261dcabc36c4816164479a2b7e8ebaa329907696fb0af19ce64cbe49cf9fbfe5ad7aa1d44f2335a36acfced94e797c6819e2ff04edf091d43d401dfcdfdde27d48844187a7872b0246f9db956347fd7d2afc8218ed13ed1a63fb0733c8e9b1116df2990579c407c0bdd356111b439e4630105f1d243c2788273ecbf0187d01866f9a8be95e93aa0c66f02d8233bbc873cc1780e043b8786ae7345affa15c7600f701ea45958451fc747f7eb82b372be74eacc782553ffd3c64483c05a4a2169ba3f0d139852335f992a4a1bdebcd952a7a6cbccf9caa0c00e2380686da1d128e1df3b79316ed8cb9923e677dfc0c9866694535f5ef31f6d16a0d58341a7ab2286e79bb7557482ee97696576292ffd8fc350ee22430e8f59ae64dcef0b8812916fad49c421cbb3b834182f5d472cec0b7cdb2dbfe9bc189720f4862c7c98bdeb4606b067d26320067b4f64c37b50cef72bfbb614b7ceabd7c232033fcac12a10c7da78993d98a0b9e7047c62544a5980450f94fcdd40d39f72d7de3c98094d5fe3c5f9215d99da449d56a6f1a0ff71e50e06e1eb46b48ab88b69f42372418355067c76631550a7b2a64da3464c152b5a1b0c4561c1d0194c390d70ab4ff300556f77b984c760366eaed9b4faeee05509ec9a6aad6a83faa3916a4ee05d4f35ccc6ee508d4f86fbfd5fb0f74e904c577ce7c22a514524f5d68e43b6eb92ecb758da07e6298de126ec911e3a216a929e5154c8a399ec98707adb26656e121cc6ed23ac16b08e3d9c1f5bd741c569df17bda7ba569352c60d2ded729bff8e62ecb10e03619c40fdbc9bd4fd603ddc77fa83315116831723b104954c0423aef0d4bdf33559333215ce07122f44eea63f71d890875ba7aa0cac3f59b06207a036c4946b1ec79e3396a546c5e9346b28a643b82d9f60d8ab0c1704bc7a0c5cb0d0f01ceeb8ba224e5f6813489c7e7142c229706189480c955f1151d91dae8aed9ea6dc5660fea4bf66b70702367845f8a2b5592bfd65c15c76123693c0c0815f665db5c65b5a85c1118cc34705083fa7bd98d2bafe931774a64d08660d89c573e67b3941d5be02e64ac52e4fce6df68b06c946045c5d7802aa8069b7092e2aefa963307e2132656b";
  
  
  const char* pattern = "0c54ef30c5";
  int p = 0;
  int ms = maxSuf(pattern, strlen(pattern), &p);
  int q = 0;
  int ms2 = maxSufTilde(pattern, strlen(pattern), &q);
  
  const char* haystack = "WERABCDEFAEWR";

  TW(pattern, strlen(pattern), haystack, strlen(haystack));

  fprintf(stdout, "Pattern = %s with len = %ld,  p = %d, ms = %d, q = %d, ms2 = %d \n", pattern, strlen(pattern), p, ms, q, ms2);
  return 0;
}
