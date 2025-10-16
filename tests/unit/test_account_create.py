from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "00000000000")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.pesel == "00000000000"
        assert len(account.pesel) == 11
        account2 = Account("Jan","Kowalski","pesel? to nawet nie jest on")
        assert account2.pesel == "INVALID"
        assert account2.balance == 0
        account3 = Account("Coolaid","Man", "0123456789X","Promocja?")
        assert account3.balance == 0
        
    def test_limited_promo(self):
        acc = Account("Stary","Człowiek","6012=======","PROMO_XYZ")
        assert acc.balance == 0
        acc1 = Account("Typ","Z przyszłości","6032=======","PROMO_XYZ")
        assert acc1.balance == 50
        acc2 = Account("Młody","Człowiek","9901=======","PROMO_XYZ")
        assert acc2.balance == 50