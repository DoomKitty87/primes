import time
import math

def prepare_command():
  tocompute = input("How many primes would you like to compute?: ")
  n = ''
  for i in tocompute:
    if (i.isdigit()):
      n += i
  tocompute = n
  return int(tocompute)

def is_prime_simple(num):
  for x in range(2, num):
    if num % x == 0:
      return False
  return True

def sieve_of_eratosthenes(num):
  primes = []
  for i in range(2, num + 1):
    primes.append(i)
  i = 2
  while i <= int(math.sqrt(num)):
    if i in primes:
      for j in range(i * 2, num + 1, i):
        if j in primes:
          primes.remove(j)
    i += 1
  return primes

def sieve_of_atkin(num):
  if num > 2:
    print(2, end=" ")
  if num > 3:
    print(3, end=" ")

  sieve = [False] * (num + 1)
  for i in range(0, num + 1):
    sieve[i] = False
  x = 1
  while x * x <= num:
    y = 1
    while y * y <= num:
      n = (4 * x * x) + (y * y)
      if (n <= num and (n % 12 == 1 or n % 12 == 5)):
        sieve[n] ^= True
      n = (3 * x * x) + (y * y)
      if n <= num and n % 12 == 7:
        sieve[n] ^= True
      n = (3 * x * x) - (y * y)
      if (x > y and n <= num and n % 12 == 11):
        sieve[n] ^= True
      y += 1
    x += 1
  r = 5
  while r * r <= num:
    if sieve[r]:
      for i in range(r * r, num + 1, r * r):
        sieve[i] = False
    r += 1
  for a in range(5, num + 1):
    if sieve[a]:
      print(a, end=" ")

def atkin_optimized(num):
  P = [2, 3]
  r = range(1, int(math.sqrt(num)) + 1)
  sieve = [False] * (num + 1)
  for x in r:
    for y in r:
      xx = x * x
      yy = y * y
      xx3 = 3 * xx
      n = 4 * xx + yy
      if n < num and (n % 12 == 1 or n % 12 == 5): sieve[n] = not sieve[n]
      n = xx3 + yy
      if n <= num and n % 12 == 7: sieve[n] = not sieve[n]
      n = xx3 - yy
      if x > y and n < num and n % 12 == 11: sieve[n] = not sieve[n]
  for x in range(5, int(math.sqrt(num))):
    if sieve[x]:
      xx = x * x
      for y in range(xx, num + 1, xx):
        sieve[y] = False
  for p in range(5, num):
    if sieve[p]: P.append(p)
  return P

def run_primecalc_simple():
  start = time.time()
  primes = list(filter(is_prime_simple, range(1, prepare_command())))
  end = time.time()
  elapsed = end - start
  print(primes)
  print('Finished in', elapsed, 'seconds.')

def run_eratosthenes():
  start = time.time()
  primes = sieve_of_eratosthenes(prepare_command())
  end = time.time()
  elapsed = end - start
  print(primes)
  print('Finished in', elapsed, 'seconds.')

def run_atkin():
  start = time.time()
  start_cpu = time.process_time()
  sieve_of_atkin(prepare_command())
  end = time.time()
  end_cpu = time.process_time()
  elapsed = end - start
  elapsed_cpu = end_cpu - start_cpu
  print('Finished in', elapsed, 'seconds.')
  print('Used', elapsed_cpu, 'seconds of cpu time.')

def run_atkin_optimized():
  start = time.time()
  start_cpu = time.process_time()
  primes = atkin_optimized(prepare_command())
  end = time.time()
  end_cpu = time.process_time()
  elapsed = end - start
  elapsed_cpu = end_cpu - start_cpu
  print(primes)
  print('Finished in', elapsed, 'seconds.')
  print('Used', elapsed_cpu, 'seconds of cpu time.')

if __name__ == "__main__":
  run_atkin_optimized()