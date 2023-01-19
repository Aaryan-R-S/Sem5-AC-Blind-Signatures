from Crypto.Util import number
import gmpy2
import random

class Signature:
    def __init__(self, security_parameter):
        self.security_parameter = security_parameter
        ((n,e),(p,q,d)) = self.generateKeyPair() 
        self.pubKey = {"n": n, "e": e}
        self.privKey = {"p": p, "q": q, "d": d}

    def gcd(a, b):
        while b != 0:
            (a, b) = (b, a%b)
        return a

    def generateKeyPair(self):
        p = number.getPrime(self.security_parameter)
        q = number.getPrime(self.security_parameter)

        while p == q:
            q = number.getPrime(self.security_parameter)
        
        n = p * q
        
        phi_n = (p-1) * (q-1)
        
        e = random.randint(2, phi_n-1)

        while Signature.gcd(e, phi_n) != 1:
            e = random.randint(2, phi_n-1)
    
        d = gmpy2.invert(e, phi_n)

        return ((n,e),(p,q,d))
    
    def signMessage(self, m):
        if type(m) != int:
            raise ValueError("[ERROR] Message to be signed must be an integer type!")
            
        signature = pow(m, self.privKey["d"], self.privKey["p"] * self.privKey["q"])
        return signature

    def validateSignature(self, m, sign):
        if type(m) != int :
            raise ValueError("[ERROR] Message to be signed must be an integer type!")
            
        if type(sign) != int:
            raise ValueError("[ERROR] Signature to be verified must be an integer type!")
            
        m_prime = pow(sign, self.pubKey["e"], self.pubKey["n"])
        return m == m_prime
    
    def getMessage(self, sign):
        m = pow(sign, self.pubKey["e"], self.pubKey["n"])
        return m
    
class Predicate_R:
    def __init__(self):
        self.dump = []
    
    def setRedundancy(self, x):
        self.dump.append(x)
    
    def checkRedundancy(self, x):
        return x in self.dump
