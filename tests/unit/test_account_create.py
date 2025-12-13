from src.account import Account, Company_Account, Personal_Account, AccountRegistry
import pytest

# python3 -m coverage run --source=src -m pytest ; python3 -m coverage report

class TestAccount:
    @pytest.fixture
    def john_doe(self):
        return Personal_Account('John','Doe','00210100000','-')
    
    @pytest.fixture
    def mock_api(self, mocker):
        # Create a mock API client
        mock_api_client = mocker.Mock()
        # Mock the response of the API client
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result':{'subject':{'statusVat':'Czynny'}}}
        # Set the mock API client to return the mocked response
        mock_api_client.get.return_value = mock_response
        return mock_api_client
    
    @pytest.fixture
    def betonpol(self, mock_api):
        return Company_Account("Betonpol", "8461627563", mock_api)
  
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
    
    @pytest.mark.parametrize( 'test_input,expected', [ ('8461627563', '8461627563'), ( 'not nip', 'INVALID' ) ])
    def test_company_account_creation( self, mock_api, test_input, expected ):
        acc = Company_Account("company",test_input, mock_api)
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
    
    def test_company_loan( self, betonpol ):
        assert betonpol.submit_for_loan( 100 ) == False
        betonpol.transaction( 10000 ) 
        assert betonpol.submit_for_loan( 100 ) == False
        betonpol.transaction( -1775 )
        assert betonpol.submit_for_loan( 100 ) == True
        assert betonpol.submit_for_loan( 100000 ) == False
        
    @pytest.mark.parametrize( 'test_input,expected', [ ('6032=======', 50), ( '9901=======', 50 ),('6012=======',0) ])
    def test_personal_promo( self, test_input, expected ):
        assert Personal_Account("John","Doe",test_input,"PROMO_XYZ").balance == expected

    def test_account_registry(self, john_doe):
        reg = AccountRegistry()
        assert reg.find(john_doe.pesel)=='none'
        reg.add_account(john_doe)
        assert reg.accounts.__contains__(john_doe)
        assert reg.find(john_doe.pesel)==john_doe
        assert reg.access() == reg.accounts
        assert reg.size() == len(reg.accounts)
        