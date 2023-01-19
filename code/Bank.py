from Signature import Signature
from Signature import Predicate_R
from Customer import Customer

class Bank:
    def __init__(self, bank_name, security_parameter, init_balance, note_value):
        self.name = bank_name
        self.signature = Signature(security_parameter)
        self.pubKey = self.signature.pubKey
        self.privKey = self.signature.privKey
        self.init_balance = init_balance
        self.note_value = note_value
        self.predicate_r = Predicate_R()
        self.customers = []
        self.deposited_signatures = []
        
    def addCustomer(self, name):
        self.customers.append(Customer(name, self.pubKey, self.init_balance, self.predicate_r))
    
    def signMessage(self, customer_idx, m_prime):
        try:
            sign_prime = self.signature.signMessage(m_prime)
            self.customers[customer_idx].decrementBalance(self.note_value)
            return sign_prime

        except Exception as e:
            print(e)
            return False
    
    def submitSignatue(self, customer_idx, sign):
        try:
            message = self.signature.getMessage(sign)

            verdict = self.predicate_r.checkRedundancy(message) 
            
            if verdict:
                if sign in self.deposited_signatures:
                    raise ValueError("[BAD REQUEST] Signature already submitted!")

                else:
                    self.deposited_signatures.append(sign)
                    self.customers[customer_idx].incrementBalance(self.note_value)
            else:
                raise ValueError("[BAD REQUEST] Signature verification failed!")
            
        except Exception as e:
            print(e)
            return False

        return True
