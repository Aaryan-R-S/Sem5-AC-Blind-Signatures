import random
import gmpy2

class Customer:
    def __init__(self, customer_name, bank_pub_key, balance, predicate_r):
        self.name = customer_name
        self.bank_pub_key = bank_pub_key
        self.balance = balance
        self.predicate_r = predicate_r

    def gcd(a, b):
        while b != 0:
            (a, b) = (b, a%b)
        return a

    def decrementBalance(self, note_value):
        self.balance -= note_value
        
    def incrementBalance(self, note_value):
        self.balance += note_value
        
    def blindMessage(self, m):
        self.r = random.randint(2, self.bank_pub_key["n"])

        while Customer.gcd(self.r, self.bank_pub_key["n"]) != 1 or self.predicate_r.checkRedundancy(self.r):
            self.r = random.randint(2, self.bank_pub_key["n"])
        
        return (m * pow(self.r, self.bank_pub_key["e"], self.bank_pub_key["n"])) % self.bank_pub_key["n"]

    def stripSign(self, sign):
        inv_r = gmpy2.invert(self.r, self.bank_pub_key["n"])
        return (sign * inv_r) % self.bank_pub_key["n"]

    def verifySign(self, m, sign):
        m_prime = pow(sign, self.bank_pub_key["e"], self.bank_pub_key["n"])
        return m == m_prime
        
    def getMessage(self, sign):
        m = pow(sign, self.bank_pub_key["e"], self.bank_pub_key["n"])
        return m
    
