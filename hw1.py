"""
Write a function in Python that takes a list as input and 
repeatedly appends the sum of the last three elements of 
the list to the end of the list. Your function should loop 
for 25 times.
"""

def appendsums(lst):
    n = 0
    while True:
        newnum = lst[-1] + lst[-2] + lst [-3]
        lst.append(newnum)
        n = n + 1 
        if n>25: break
    return lst

sum_three = [0,1,2]
appendsums(sum_three)
print sum_three[20]







"""
The deposit and withdraw methods each change the account balance. 
The withdraw method also deducts a fee of 5 dollars from the balance 
if the withdrawal (before any fees) results in a negative balance. 
Since we also have the method get_fees, you will need to have a 
variable to keep track of the fees paid.
"""

class BankAccount:
    """ Class definition modeling the behavior of a simple bank account """

    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self.bal = initial_balance
        self.fee = 0
    
    def deposit(self, amount):
        """Deposits the amount into the account."""
        self.bal = self.bal + amount
        
    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        self.bal = self.bal - amount
        if self.bal<0: 
            self.bal = self.bal - 5
            self.fee = self.fee + 5
        
    def get_balance(self):
        """Returns the current balance in the account."""
        return self.bal
        
    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self.fee
        
my_account = BankAccount(10)
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(5)
my_account.withdraw(15)
my_account.deposit(20)
my_account.withdraw(5) 
my_account.deposit(10)
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(30)
my_account.withdraw(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(50) 
my_account.deposit(30)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(10) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(10)
my_account.deposit(20)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
print my_account.get_balance(), my_account.get_fees()
