from Bank import Bank

class PaymentSystem:
    def __init__(self, bank_name, security_parameter, init_balance, note_value):
        self.bank = Bank(bank_name, security_parameter, init_balance, note_value)
        
if __name__ == "__main__":
    name = input("\nEnter the name of your bank (e.g. Anonymous Bank): ")
    security_parameter = int(input("Enter security parameter in bits (e.g. 1024): "))
    init_balance = int(input("Enter the initial bank balance in dollars (e.g. 1000): "))
    note_value = int(input("Enter the value of one signed note in dollars (e.g. 1): "))
    myPaymentSystem = PaymentSystem(name, security_parameter, init_balance, note_value)

    curr_idx = -1

    line = "------------------------------------------------"

    menu = f'''\nWelcome to {myPaymentSystem.bank.name}!\nEnter:\n1 -> Add Customer\n2 -> Switch Customer\n3 -> Customer Details \n4 -> Sign Note \n5 -> Submit Note \n6 -> Exit'''

    while True:    
        print(line)
        print(menu)
        print("")
        print(line)
        
        try:
            inp = int(input("\nEnter your choice: "))

            print("")
            
            if inp == 1:
                name = input("Enter customer name: ")
                myPaymentSystem.bank.addCustomer(name)            
                print(f"Customer added with id {len(myPaymentSystem.bank.customers)}.")
        
            elif inp == 2:
                if len(myPaymentSystem.bank.customers) < 2:
                    print("Less than two customers found. Please add atleast two customers to the bank!")
                    continue

                idx = int(input(f"Enter customer ID from 1 to {len(myPaymentSystem.bank.customers)}: "))
                if idx >= 1 and idx <= len(myPaymentSystem.bank.customers):
                    curr_idx = idx
                    print(f"Your current balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")

                else:
                    print("Invalid ID provided!")
                
            elif inp == 3:
                if curr_idx == -1:
                    print("Choose a customer first and then come to this option!")
                    continue

                print(f"Name: {myPaymentSystem.bank.customers[curr_idx-1].name}")
                print(f"Bank balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")

            elif inp == 4:
                if curr_idx == -1:
                    print("Choose a customer first and then come to this option!")
                    continue

                message = int(input("Enter your message representing some bill number or order id. It can also be binary string representing some data (must be int): "))
                
                verdict = myPaymentSystem.bank.customers[curr_idx-1].predicate_r.checkRedundancy(message)

                if verdict == True:
                    print("Message entered by you has already been used. Please use some other message!")
                    continue 
                
                myPaymentSystem.bank.customers[curr_idx-1].predicate_r.setRedundancy(message)
                
                m_prime = myPaymentSystem.bank.customers[curr_idx-1].blindMessage(message)
                
                sign_prime = myPaymentSystem.bank.signMessage(curr_idx-1, m_prime)

                if sign_prime == False:
                    print("Signing process failed!")
                    print(f"Your current balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")
                    continue
                
                sign = myPaymentSystem.bank.customers[curr_idx-1].stripSign(sign_prime)

                verdict = myPaymentSystem.bank.customers[curr_idx-1].verifySign(message, sign)
                
                if verdict:
                    print(f"Here is your signed note: \n{sign}")
                    print(f"Your new balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")
                
                else:
                    print("Signature given by bank has failed the verification process!")
                    print(f"Your current balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")

            elif inp == 5:
                if curr_idx == -1:
                    print("Choose a customer first and then come to this option!")
                    continue

                sign = int(input("Enter the signed note signature (must be int): "))

                message = myPaymentSystem.bank.customers[curr_idx-1].getMessage(sign)
                verdict = myPaymentSystem.bank.customers[curr_idx-1].predicate_r.checkRedundancy(message)

                if verdict == False:
                    print("Signature given by the payer has failed the verification process!")
                    continue
                    
                verdict = myPaymentSystem.bank.submitSignatue(curr_idx-1, sign)

                if verdict:
                    print("Signed note submitted successfully!")
                    print(f"Your new balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")
                
                else:
                    print("Signed note can't be submitted!")
                    print(f"Your current balance: {myPaymentSystem.bank.customers[curr_idx-1].balance}")
            
            elif inp == 6:
                break

            else:
                print("\nInvalid input provided!")

        except Exception as e:
            print(e)
            
    print("Thanks for using our payment system!\n")