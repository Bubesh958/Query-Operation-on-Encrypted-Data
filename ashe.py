import random
import math
#aggregate-salary

def generate_keypair(p,q):
    n = p * q
    phi = (p-1) * (q-1)

    e = phi-1


    g = gcd(e, phi)
    while g != 1:
        e = phi-1
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)
 
    return ((e, n), (d, n))

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def decrypt_lt(pk, ciphertexts):
    plaintexts = []
    for ciphertext in ciphertexts:
        plaintexts.append(decrypt(pk, ciphertext))
    return plaintexts

def decrypt(pk, ciphertext):
   
    key, n = pk
    plain = ciphertext/key
    
    return plain
    



def encrypt(pk, number):
  
    key, n = pk
    cipher = number*key
  
    return cipher

def compare(n1, n2):
    
    if(n1 == n2):
        print"THE NUMBERS ARE EQUAL"
    elif(n1<n2):
        print"THE NUMBER",n1,"IS LESS THAN",n2
    else:
        print"THE NUMBER",n1,"IS GREATER THAN",n2
    
    return


def sum_of_encrypted_numbers(en_lt):
	return sum(en_lt)

def enc_lt(numbers,private):
	en_lt = []
	for i in numbers:
    	    en_lt.append(encrypt(private,i))
        return en_lt;


def ashe(numbers):
    prime1 = random.randrange(1, 100)
    while(not(is_prime(prime1))):
        prime1 = random.randrange(1,100)
    prime2 = random.randrange(1,100)
    while(not(is_prime(prime2)) or prime2 == prime1):
        prime2 = random.randrange(1,100)
    #print"primes ",prime1," ",prime2
    public, private = generate_keypair(prime1,prime2)
    '''print "Your public key is ", public ," and your private key is ", private'''
    #s = raw_input("Enter numbers to encrypt ")
    #numbers = map(int,s.split())
    sm = 0;

    
    en_lt = enc_lt(numbers,private)

    sm = sum_of_encrypted_numbers(en_lt)
    
    return en_lt,[public,private]

    #print " Encrypted Sum and actual sum is ",sm,decrypt(public,sm)

   
