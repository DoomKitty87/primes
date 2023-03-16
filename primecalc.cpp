class PrimeCalculator {

  public:
    int * atkin_optimized(int num) {
      bool sieve[num];
      for (int i = 0; i <= num; i++)
        sieve[i] = false;
 
      if (num > 2)
        sieve[2] = true;
      if (num > 3)
        sieve[3] = true;

      for (int x = 1; x * x <= num; x++) {
        for (int y = 1; y * y <= num; y++) {
 
            int n = (4 * x * x) + (y * y);
            if (n <= num
                && (n % 12 == 1 || n % 12 == 5))
                sieve[n] ^= true;
 
            n = (3 * x * x) + (y * y);
            if (n <= num && n % 12 == 7)
                sieve[n] ^= true;
 
            n = (3 * x * x) - (y * y);
            if (x > y && n <= num
                && n % 12 == 11)
                sieve[n] ^= true;
        }
      }

      for (int r = 5; r * r <= num; r++) {
        if (sieve[r]) {
            for (int i = r * r; i <= num; i += r * r)
                sieve[i] = false;
        }
      }
      int outsize = 0;
      for (int a = 1; a <= num; a++)
        if (sieve[a])
          outsize++;
      
      int output[outsize];
      int i = 0;
      for (int a = 1; a <= num; a++)
        if (sieve[a])
          output[i] = a;
          i++;
      
      return output;
    }
};