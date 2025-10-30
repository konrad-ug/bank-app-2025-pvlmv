class Account:
    def __init__(self):
        self.balance=0
    
    def transaction(self, value, price=0):
        if self.balance+value>0:
            self.balance+=(value-price)

class Personal_Account(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        
        self.balance = 0
        if promo_code == "PROMO_XYZ" and ( int(pesel[0:2])>60 or int(pesel[2])>1 ):
            self.balance += 50
            
        if len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "INVALID"
    
    def transaction(self, value, express=False):
        price=0
        if express : price=1
        return super().transaction(value,price)    

class Company_Account(Account):
    def __init__( self, company_name, nip):
        if len(nip) == 10 : self.nip=nip
        else: self.nip = "INVALID"
        self.company_name = company_name
        self.balance = 0
    
    def transaction(self, value, express=False):
        price=0
        if express : price=5
        return super().transaction(value,price)
    
    def uncovered_method(self):
        print("I'm off the hook")