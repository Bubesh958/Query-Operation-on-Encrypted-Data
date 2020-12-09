import random
import csv
import math
import rsa
import ashe
import time
import socket
import sys
#range-age

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

def encrypt(pk, number):
  
    key, n = pk
    cipher = number*key
    return cipher

def sum1(n1,n2):
    
    return(n1+n2)

def find_range(lt,en_lt):
    ans = []
    for i in en_lt:
        if( i >= lt[0] and i <= lt[1]):
            ans.append((i,decrypt(ope_public,i)))
    return ans

def enc_lt(numbers,private):
    en_lt = [];
    for i in numbers:
        en_lt.append(encrypt(private,i))
    return en_lt


def ope(data):
	prime1 = random.randrange(1, 100)
	while(not(is_prime(prime1))):
		prime1 = random.randrange(1, 100)
	prime2 = random.randrange(1,100)
	while(not(is_prime(prime2)) or prime2 == prime1):
		prime2 = random.randrange(1,100)
	ope_public, ope_private = generate_keypair(prime1,prime2)
	encrypted_list = enc_lt(data,ope_private)
	return encrypted_list,[ope_public,ope_private]