import math

primes = [2]
primeFactor = [{},{},{2},{3}]
totients = [0,1,1]

def GeneratePrimes(n):
	cur = primes[len(primes)-1]+1
	while cur <= n:
		isPrime = True
		for i in range(len(primes)):
			if primes[i]**2 > cur:
				break
			if cur%primes[i] == 0:
				isPrime = False
				break
		if isPrime:
			primes.append(cur)
		cur+=1

def LeastPrimeFactor(n):
	GeneratePrimes(int(math.sqrt(n)))
	for i in range(len(primes)):
		if n%primes[i]==0:
			return primes[i]
		if primes[i]**2 > n:
			return n
	return n
def GeneratePrimeFactor(n):
	if n >= len(primeFactor):
		if LeastPrimeFactor(n)==n:
			primeFactor.append({n})
		else:
			LPF = LeastPrimeFactor(n)
			# print(n/LPF)
			primeFactor.append(primeFactor[int(n/LPF)].copy())
			primeFactor[n].add(LPF)

def EulerTotient(n):
	if n >= len(totients):
		totient = n
		for i in range(len(primeFactor),n+1):
			GeneratePrimeFactor(i)
		for factor in primeFactor[n]:
			totient/=factor
			totient*=factor-1
		totients.append(totient)
		return int(totient)
	else:
		return totients[n]

def GetHighlyCotetientList(n):
	cNum = 0
	count = 0
	num = 2
	coLi = []
	while cNum < n:
		lCount = 0
		li = []
		for i in range(num+1,num**2+1):
			if num == i-EulerTotient(i):
				lCount+=1
				li += [i]
				# print(num,i,i-EulerTotient(i))
		if lCount > count:
			count = lCount
			cNum+=1
			coLi.append(num)
			print("----------------------------------------------------------------------------------------------------")
			print(str(len(coLi))+" : "+str(num)+" "+str(li))
			print("----------------------------------------------------------------------------------------------------")
		else: print(num,li)
		num+=1
	return coLi

length = int(input("Length : "))
print("\nHighly Cototient Numbers : "+str(GetHighlyCotetientList(length)))
