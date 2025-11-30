import pytest
import requests

class TestApi:
    url = 'http://127.0.0.1:5000/api/accounts'
    def test_create_account(self):
        payload = {
            'first_name' : 'John',
            'last_name' : 'Doe',
            'pesel' : '00210100000',
            'promo' : '-'
        }
        response = requests.post( url = self.url, json = payload )
        assert response.status_code == 201
        assert response.json()['message'] == 'Account created'
    
    def test_get_account_count(self):
        response = requests.get(self.url+'/count')
        assert response.status_code == 200
        assert str(response.json()['count']).isnumeric()
    
    def test_get_accounts(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        assert isinstance( response.json(), list )
    
    def test_get_account_by_pesel(self):
        if( requests.get(self.url+'/count') == 0 ):
            requests.post( self.url, json = {
                'first_name' : 'John',
                'last_name' : 'Doe',
                'pesel' : '00210100000',
                'promo' : '-'
            } )
        acc = requests.get(self.url).json()[0]
        response = requests.get(self.url+'/'+acc['pesel'])
        assert response.status_code == 200
        assert response.json() == {
            'balance' : acc['balance'],
            'last_name' : acc['last_name'],
            'first_name' : acc['first_name'],
            'pesel' : acc['pesel']
        }
        
    def test_update_account(self):
        if( requests.get(self.url+'/count') == 0 ):
            requests.post( self.url, json = {
                'first_name' : 'John',
                'last_name' : 'Doe',
                'pesel' : '00210100000',
                'promo' : '-'
            } )
            
        acc = requests.get(self.url).json()[0]
        response = requests.patch( self.url+'/'+acc['pesel'], json = {
            'last_name' : 'Johnson',
        })
        
        assert response.status_code == 200
        assert response.json()['message'] == 'Account updated'
        
    def test_delete_account(self):
        if( requests.get(self.url+'/count') == 0 ):
            requests.post( self.url, json = {
                'first_name' : 'John',
                'last_name' : 'Doe',
                'pesel' : '00210100000',
                'promo' : '-'
            } )
        acc = requests.get(self.url).json()[0]
        response = requests.delete(self.url+'/'+acc['pesel'])
        assert response.status_code == 200
        assert response.json()['message'] == 'Account deleted'
        response = requests.get(self.url+'/'+acc['pesel'])
        assert response.status_code == 404
        assert response.json()['message'] == 'Account not found'