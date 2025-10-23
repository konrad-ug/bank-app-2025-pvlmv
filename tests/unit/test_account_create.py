from src.account import Account, Company_Account, Personal_Account


class TestAccount:
    def test_account_creation(self):
        account = Personal_Account("John", "Doe", "00000000000")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "00000000000"
        assert len(account.pesel) == 11
        account2 = Personal_Account("Jan","Kowalski","pesel? to nawet nie jest on")
        assert account2.pesel == "INVALID"
        assert account2.balance == 0
        account3 = Personal_Account("Coolaid","Man", "0123456789X","Promocja?")
        assert account3.balance == 0
        
    def test_limited_promo(self):
        acc = Personal_Account("Stary","Człowiek","6012=======","PROMO_XYZ")
        assert acc.balance == 0
        acc1 = Personal_Account("Typ","Z przyszłości","6032=======","PROMO_XYZ")
        assert acc1.balance == 50
        acc2 = Personal_Account("Młody","Człowiek","9901=======","PROMO_XYZ")
        assert acc2.balance == 50
        
    def test_transaction(self):
        acc = Personal_Account("John", "Doe", "00000000000")
        acc.transaction( 100 )
        assert acc.balance==100
        acc.transaction( -10, True )
        assert acc.balance == 89
        
    def test_company_Personal_account(self):
        acc = Company_Account("Betonpol","0000000000")
        assert acc.company_name == "Betonpol"
        assert acc.nip == "0000000000"
        acc.transaction( 100 )
        assert acc.balance==100
        acc.transaction( -10, True )
        assert acc.balance == 85