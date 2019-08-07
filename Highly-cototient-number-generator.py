import math

primes = [2]
primeFactor = [{},{},{2},{3}]
totients = [0,1,1]
coTotients = []
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
	coList = []
	count = 0
	prev = 0
	num = 2
	while count < n:
		li = []
		for i in range((num-1)**2+1,num**2+1):
			val = int(i-EulerTotient(i))
			while len(coTotients) <= val:
				coTotients.append([])
			coTotients[val].append(i)
		# print(coTotients[num])
		if len(coTotients[num]) > prev:
			prev = len(coTotients[num])
			count += 1
			coList.append(num)
			print("----------------------------------------------------------------------------------------------------")
			print(str(len(coList))+" : "+str(num)+" "+str(coTotients[num]))
			print("----------------------------------------------------------------------------------------------------")
		else: print(num,str(coTotients[num]))
		num+=1
	return coList

length = int(input("Length : "))
print("\nHighly Cototient Numbers : "+str(GetHighlyCotetientList(length)))
