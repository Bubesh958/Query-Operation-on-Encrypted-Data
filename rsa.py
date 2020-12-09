import random
#string-name

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True
    

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


def decrypt_lt(pk, ciphertexts):
   
    key, n = pk
    plaintexts = []
    for ciphertext in ciphertexts:
        ciphertext = map(int,ciphertext.split('?'))
    	plain = [chr((char ** key) % n) for char in ciphertext]
        plain = ''.join(map(lambda x: str(x), plain))
        plaintexts.append(plain)
    return plaintexts

def rsa_find(en_list,enc_value):
	return en_list.index(enc_value)

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

def encrypt_lt(pk, plaintexts):
	key,n=pk
	ciphers = []
	for plaintext in plaintexts:
		cipher = [(ord(char) ** key) % n for char in plaintext]
		cipher = '?'.join(map(lambda x: str(x), cipher))
		ciphers.append(cipher)
	return ciphers

def encrypt_word(pk, plaintext):
	key,n=pk
	cipher = [(ord(char) ** key) % n for char in plaintext]
	cipher = '?'.join(map(lambda x: str(x), cipher))
	return cipher

def rsa(message):
    # print "Generating your public/private keypairs now . . ."
    public, private = generate_keypair(13,17)
    # print "Your public key is ", public ," and your private key is ", private
    #message = raw_input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt_lt(private, message)
    # print "Your encrypted message is: "
    # print ''.join(map(lambda x: str(x), encrypted_msg))
    # print "Decrypting message with public key ", public ," . . ."
    # print "Your message is:"
    
    return encrypted_msg,[public,private]
    
    # #message = raw_input("Enter a message to encrypt with your private key: ")
    # encrypted_msg = encrypt(private, message)
    # print "Your encrypted message is: "
    # print ''.join(map(lambda x: str(x), encrypted_msg))
    # print "Decrypting message with public key ", public ," . . ."
    # print "Your message is:"
    # print decrypt_word(public, encrypted_msg)

# rsa("gi")