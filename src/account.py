class Account:
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        
        self.balance = 0
        if promo_code == "PROMO_XYZ" and ( int(pesel[0:2])>60 or int(pesel[2])>1 ):
            self.balance += 50
            
        if len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "INVALID"