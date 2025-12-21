from functools import reduce
from datetime import datetime
from src.smtp.smtp import SMTPClient
import requests
BANK_APP_MF_URL = 'https://wl-api.mf.gov.pl/api/search/nip/'
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
    
    def send_history_via_email( self, email : str, acc_type : str ):
        if email.__contains__('@') and not email.__contains__(' '):
            return SMTPClient.send(
                'Account Transfer History' + str(datetime.now()).split(' ')[0],
                acc_type + ' account history ' + str(self.history),
                email
            )
        return False


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
    
    def send_history_via_email(self, email : str):
        return super().send_history_via_email(email, "Personal")
    
class Company_Account(Account):
    def __init__( self, company_name, nip, api = requests):
        res = api.get(BANK_APP_MF_URL+nip+'?date='+datetime.now().strftime('%Y-%m-%d'))
        if len(nip) < 10:
            self.nip='INVALID'        
        elif res.status_code==200 and res.json()['result']['subject']['statusVat']=='Czynny':
            self.nip=nip
        else:
            raise ValueError('Company not registered!')
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
    
    def send_history_via_email(self, email : str):
        return super().send_history_via_email(email, 'Company')
        
        
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