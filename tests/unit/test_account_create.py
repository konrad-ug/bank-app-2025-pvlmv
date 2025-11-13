from src.account import Account, Company_Account, Personal_Account
import pytest

class TestAccount:
    @pytest.fixture
    def john_doe(self):
        return Personal_Account('John','Doe','00210100000','-')
    
    @pytest.fixture
    def betonpol(self):
        return Company_Account("Betonpol","0000000000")
    
    def test_account_creation( self ):
        acc = Account()
        assert acc.balance==0
        assert acc.history==[]
        
    def test_personal_account_creation( self, john_doe ):
        assert john_doe.first_name == "John"
        assert john_doe.last_name == "Doe"
        assert john_doe.balance == 0
    
    @pytest.mark.parametrize( 'test_input,expected', [ ('00210100000', '00210100000'), ( 'not pesel', 'INVALID' ) ])
    def test_personal_account_pesel( self, test_input, expected):
        assert Personal_Account('name','surname',test_input).pesel == expected
    
    @pytest.mark.parametrize( 'test_input,expected', [ ('0021010000', '0021010000'), ( 'not nip', 'INVALID' ) ])
    def test_company_account_creation( self, test_input, expected ):
        acc = Company_Account("company",test_input)
        assert acc.company_name == 'company'
        assert acc.nip==expected
       
    def test_transaction(self):
        acc = Account()
        acc.transaction(10,1)
        assert acc.balance==9
        assert acc.history[-1] == {"value":10,"cost":1}
    
    def test_personal_transaction( self, john_doe ):
        john_doe.transaction( 100 )
        assert john_doe.balance==100
        john_doe.transaction( -10, True )
        assert john_doe.balance == 89
        
    def test_company_transaction( self, betonpol ):
        betonpol.transaction( 100 )
        assert betonpol.balance==100
        betonpol.transaction( -10, True )
        assert betonpol.balance == 85

    @pytest.mark.parametrize( 'test_input,expected', [ ('6032=======', 50), ( '9901=======', 50 ),('6012=======',0) ])
    def test_personal_promo( self, test_input, expected ):
        assert Personal_Account("John","Doe",test_input,"PROMO_XYZ").balance == expected

    def test_personal_loan( self, john_doe ):
        assert john_doe.submit_for_loan( 100 ) == False
        
        john_doe.transaction( 100 )
        john_doe.transaction( 100, True )
        john_doe.transaction( 100, True )
        assert john_doe.submit_for_loan( 1000 ) == True
        assert john_doe.balance == 1298
        
        john_doe.transaction( -10 )
        assert john_doe.submit_for_loan( 1 ) == False
        assert john_doe.balance == 1288
        
        john_doe.transaction( 100 )
        assert john_doe.submit_for_loan( 300 ) == True
        assert john_doe.submit_for_loan( 388 ) == False
        assert john_doe.submit_for_loan( -20 ) == False