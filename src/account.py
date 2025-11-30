from functools import reduce
class Account:
    def __init__(self):
        self.balance=0
        self.history=[]
    
    def transaction(self, value, price=0):
        if self.balance+value>0:
            self.balance+=(value-price)
            self.history.append({"value":value,"cost":price})
            
    def submit_for_loan(self, value):
        self.balance+=value
        return True

class Personal_Account(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.history=[]
        
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
    
    def submit_for_loan( self, value ):
        if value <= 0: return False
        if len(self.history) < 3 :
            return False
        
        last_three = self.history[-3:]
        if reduce( lambda acc, val: acc and val['value'] > 0, last_three):
            return super().submit_for_loan(value)
        
        if len(self.history) < 5 :
            return False
        
        sum_of_last_five = reduce( lambda acc, val: acc + val, list( map( lambda x: x['value']-x['cost'], self.history[-5:] ) ) )
        if sum_of_last_five > value:
            return super().submit_for_loan(value)
        
        return False
    
class Company_Account(Account):
    def __init__( self, company_name, nip):
        if len(nip) == 10 : self.nip=nip
        else: self.nip = "INVALID"
        self.company_name = company_name
        self.balance = 0
        self.history=[]
    
    def transaction(self, value, express=False):
        price=0
        if express : price=5
        return super().transaction(value,price)
    
    def submit_for_loan(self, value):
        if( value*2 <= self.balance and
        self.history.__contains__( { 'value':-1775, 'cost':0 } ) ):
            return super().submit_for_loan(value)
        else:
            return False
        
        
class AccountRegistry:
    def __init__(self):
        self.accounts : list[Personal_Account] = []
        
    def add_account(self, account: Personal_Account):
        self.accounts.append(account)
        
    def find( self, pesel ):
        for acc in self.accounts:
            if acc.pesel==pesel:
                return acc
        return 'none'
    
    def access(self):
        return self.accounts
    
    def size(self):
        return len(self.accounts)