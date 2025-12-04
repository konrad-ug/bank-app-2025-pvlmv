from flask import Flask, request, jsonify
from src.account import AccountRegistry, Personal_Account

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    pesel = data['pesel']
    promo = data['promo']
    if registry.find(pesel)!='none' :
        return jsonify({ 'message' : 'Account already exists' }), 409
    if pesel and first_name and last_name and registry.find(pesel)=='none':
        acc = Personal_Account( first_name, last_name, pesel, promo )
        registry.add_account(acc)
        return jsonify( { 'message' : 'Account created' } ), 201
    else:
        return jsonify({ 'message' : 'Incorrect data' } ), 400

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.access()
    accounts_data = [ {
        "first_name" : acc.first_name,
        "last_name" : acc.last_name,
        "pesel" : acc.pesel,
        "balance" : acc.balance
    } for acc in accounts ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    c = registry.size()
    return jsonify({"count" : c}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc : Personal_Account = registry.find(pesel)
    if(acc=='none'): return jsonify({'message' : 'Account not found'}), 404
    return jsonify( {
        'first_name' : acc.first_name,
        'last_name' : acc.last_name,
        'pesel' : acc.pesel,
        'balance' : acc.balance
    } ), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data : dict = request.get_json()
    acc = registry.find(pesel)
    
    if(acc=='none'): return jsonify({'message' : 'Account not found'}), 404
    
    if data.keys().__contains__('last_name'):
        acc.last_name=data['last_name']
        
    if data.keys().__contains__('first_name'):
        acc.first_name=data['first_name']
        
    if data.keys().__contains__('balance'):
        acc.balance=data['balance']
        
    if data.keys().__contains__('pesel'):
        acc.pesel=data['pesel']
        
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    acc = registry.find(pesel)
    if(acc=='none'): return jsonify({'message' : 'Account not found'}), 404
    registry.accounts.remove(acc)
    return jsonify({"message": "Account deleted"}), 200

@app.route('/api/accounts/<pesel>/transfer', methods=['POST'])
def transfer(pesel):
    acc = registry.find(pesel)
    if(acc=='none'): return jsonify({'message' : 'Account not found'}), 404
    
    data = request.get_json()
    if( not isinstance( data['amount'], int ) or
    data['amount'] < 0 or
    not ['incoming','outgoing','express'].__contains__(data['type']) ):
        return jsonify({'message' : 'Incorrect parameters'}), 400
    
    if data['type'] == 'incoming' :
        acc.balance += data['amount']
        
    if data['type'] == 'outgoing':
        if data['amount'] <= acc.balance: acc.balance -= data['amount']
        else: return jsonify({'message' : 'Not enough funds'}), 422

    if data['type'] == 'express':
        if ( data['amount'] + 1 ) <= acc.balance: acc.balance -= (data['amount'] + 1)
        else: return jsonify({'message' : 'Not enough funds'}), 422
    
    return jsonify({'message' : 'Transfer successfull'}), 200