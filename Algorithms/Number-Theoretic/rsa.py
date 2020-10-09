'''
    Naive implementation of RSA
'''

import pdb

def find_prime(): 
    
    return 3

def extended_euclid(a,b):
    if b == 0:
        return a,1,0
    else:
        d1,x1,y1,= extended_euclid(b,a%b)
        d,x,y = d1,y1, x1 - (a/b)*y1
        return d,x,y

def rsa_encrypt(data, e, n): 
    return (data**e) % n

def rsa_decrypt(data, d, n): 
   return data**d % n 

def generate_rsa():
    p = 11
    q = 29
    e = 3 # co-prime to (p-1),(q-1)
    n = p*q
    phi_n = (p-1)*(q-1)

    d,x,y = extended_euclid(phi_n, e)
    if y < 0:
        y = phi_n + y
    return e,y,n

if __name__ == "__main__":


    e,d,n = generate_rsa()
    data = 500
    pdb.set_trace()
    r = rsa_encrypt(data,e,n)
    s = rsa_decrypt(r,d,n)
    pdb.set_trace()
    assert(data == s)
    print 'RSA succeed!'



