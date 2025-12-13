import pytest
import requests

# python3 -m coverage run --source=src -m pytest ; python3 -m coverage report

class TestApi:
    url = 'http://127.0.0.1:5000/api/accounts'
    
    @pytest.fixture
    def john_doe(self):
        return {
            'first_name' : 'John',
            'last_name' : 'Doe',
            'pesel' : '00210100000',
            'promo' : '-'
        }
    
    @pytest.mark.parametrize( 'code, msg', [ ( 201, 'Account created'), ( 409, 'Account already exists' ) ])
    def test_create_account(self,john_doe,code,msg):
        response = requests.post( url = self.url, json = john_doe )
        assert response.status_code == code
        assert response.json()['message'] == msg
    
    def test_get_account_count(self):
        response = requests.get(self.url+'/count')
        assert response.status_code == 200
        assert str(response.json()['count']).isnumeric()
    
    def test_get_accounts(self,john_doe):
        if( requests.get(self.url+'/count').json()['count'] == 0 ): requests.post( self.url, json = john_doe )
        response = requests.get(self.url)
        assert response.status_code == 200
        assert isinstance( response.json(), list )
    
    def test_get_account_by_pesel(self,john_doe):
        if( requests.get(self.url+'/count').json()['count'] == 0 ): requests.post( self.url, json = john_doe )
        acc = requests.get(self.url).json()[0]
        
        response = requests.get(self.url+'/'+acc['pesel'])
        assert response.status_code == 200
        assert response.json() == {
            'balance' : acc['balance'],
            'last_name' : acc['last_name'],
            'first_name' : acc['first_name'],
            'pesel' : acc['pesel']
        }
    
    def test_update_account(self,john_doe):
        if( requests.get(self.url+'/count').json()['count'] == 0 ): requests.post( self.url, json = john_doe )
        acc = requests.get(self.url).json()[0]
        
        response = requests.patch( self.url+'/'+acc['pesel'], json = {
            'last_name' : 'Johnson',
        })
        
        assert response.status_code == 200
        assert response.json()['message'] == 'Account updated'
        
        compare = requests.get(self.url+'/'+acc['pesel'])
        assert compare.json()['last_name'] == 'Johnson'
        
    @pytest.mark.parametrize(
        'input_amount, input_type, status_code, status_msg', [
            ( 500, 'incoming', 200, 'Transfer successfull'),
            ( 100, 'outgoing', 200, 'Transfer successfull'),
            ( 200, 'express', 200, 'Transfer successfull'),
            ( 500, 'outgoing', 422, 'Not enough funds'),
            ( 500, 'express', 422, 'Not enough funds'),
            ( 150, 'jakiś_typ', 400, 'Incorrect parameters'),
            ( -120, 'incoming', 400, 'Incorrect parameters'),
            ( 2100, 'incoming', 404, 'Account not found'),
        ]
    )
    def test_transfer(self,john_doe,input_amount,input_type,status_code,status_msg):
        if( requests.get(self.url+'/count').json()['count'] == 0 ): requests.post( self.url, json = john_doe )
        acc = requests.get(self.url+'/'+john_doe['pesel']).json()
        
        pesel = acc['pesel']
        if input_amount==2100: pesel='-'
        mult = -1
        if input_type == 'incoming': mult = 1
        price = 0
        if input_type == 'express': price = 1
        
        response = requests.post(f"{self.url}/{pesel}/transfer", json = {
            'amount' : input_amount,
            'type' : input_type
        })
        
        assert response.status_code == status_code
        assert response.json()['message'] == status_msg
        
        if status_code == 200:
            compare = requests.get(self.url+'/'+pesel).json()
            assert compare['balance'] == acc['balance']-price+mult*input_amount
            
    
    def test_delete_account(self,john_doe):
        if( requests.get(self.url+'/count').json()['count'] == 0 ): requests.post( self.url, json = john_doe )
        acc = requests.get(self.url).json()[0]
        
        response = requests.delete(self.url+'/'+acc['pesel'])
        assert response.status_code == 200
        assert response.json()['message'] == 'Account deleted'
        response = requests.get(self.url+'/'+acc['pesel'])
        assert response.status_code == 404
        assert response.json()['message'] == 'Account not found'
