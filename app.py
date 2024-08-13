from flask import Flask, render_template, request 
from datetime import datetime
import json
from web3 import Web3, HTTPProvider

app = Flask(__name__)

user_id = ""

global details

balance = 0.0

StateGovernment = 'StateGovernment'

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:8545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Fund.json' #counter feit contract code
    deployed_contract_address = '0x8A6d16AdCF0f012aac1263137a6658D70B052A85' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUsers().call()
    if contract_type == 'account':
        details = contract.functions.getBankAccount().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]
     
  

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Fund.json' #Counter feit contract file
    deployed_contract_address = '0x8A6d16AdCF0f012aac1263137a6658D70B052A85' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'account':
        details+=currentData
        msg = contract.functions.bankAccount(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)



def checkPrivacy(userverification):
    readDetails('adduser')
    arr = details.split("\n")
    flag = False
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[0] == userverification:
            flag = True
            break
    return flag   

@app.route('/SendAmountAction', methods=['POST'])
def SendAmountAction():
    if request.method == 'POST':
        sent = request.form['t1']
        name = request.form['t2']
        readDetails("adduser")
        status = checkPrivacy(name)
        if status == True:
            readDetails('account')
            arr = details.split("\n")
            for i in range(len(arr)-1):
                array = arr[i].split("#")
                balance = array[1]
                
                if float(balance) > float(sent):
                    number = float(balance) - float(sent)
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = name+"#"+str(sent)+"#"+str(timestamp)+"#Received from state government\n"
                    saveDataBlockChain(data,"account")
                    data = str(StateGovernment)+"#"+str(number)+"#"+str(sent)+"#"+str(timestamp)+"#"+name+"#Debited\n"
                    saveDataBlockChain(data,"account")
                    context = 'Money Sent Successfully'
                    return render_template('SendAmount.html', msg=context)
                else:
                    context = 'Insufficient balance'
                    return render_template('SendAmount.html', msg=context)
        else:
            context = 'Invalid User Name'
            return render_template('SendAmount.html', msg=context)


@app.route('/ViewTransfer', methods=['GET', 'POST'])
def ViewTransfer():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size=3 color=black>'
        headers = ['Name','Total Balance' ,'Transaction Amount', 'Transaction Date and Time','Organization Name who Received Money', 'Transaction Details']
        
        # Create table headers
        output += "<tr>"
        for header in headers:
            output += "<th>" + font + header + "</th>"
        output += "</tr>"
        
        global details
        readDetails('account')

       
        arr = details.split("\n")
        

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            
            status = checkPrivacy(array[0])
            data = ""
            pos = len(array[0]) - 2
            if status == True:
                for j in range(0, pos):
                    data += "*"
                data += array[0][pos:len(array[0])]
            else:
                data = array[0]

            if array[0] == 'StateGovernment':   
                output += "<tr><td>" + font + array[0] + "</td>"
                output += "<td>" + font + array[1] + "</td>"
                output += "<td>" + font + array[2] + "</td>"
                output += "<td>" + font + array[3] + "</td>"
                output += "<td>" + font + array[4] + "</td>"
                output += "<td>" + font + array[5] + "</td></tr>"
                

        output += "</table><br/><br/><br/>"
       
        return render_template('ViewTransfer.html', msg=output)

@app.route('/ViewTransferAmount', methods=['GET', 'POST'])
def ViewTransferAmount():
    global user_id
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size=3 color=black>'
        headers = ['Name of the organization','Received Amount', 'Transaction Date and Time', 'Transaction Details']
        
        # Create table headers
        output += "<tr>"
        for header in headers:
            output += "<th>" + font + header + "</th>"
        output += "</tr>"
        
        global details
        readDetails('account')

       
        arr = details.split("\n")
        

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            
            status = checkPrivacy(array[0])
            data = ""
            pos = len(array[0]) - 2
            if status == True:
                for j in range(0, pos):
                    data += "*"
                data += array[0][pos:len(array[0])]
            else:
                data = array[0]

            if array[0] == user_id:   
                output += "<tr><td>" + font + array[0] + "</td>"
                output += "<td>" + font + array[1] + "</td>"
                output += "<td>" + font + array[2] + "</td>"
                output += "<td>" + font + array[3] + "</td></tr>"
                
                

        output += "</table><br/><br/><br/>"
       
        return render_template('ViewTransferAmount.html', msg=output)


@app.route('/UserLogin', methods=['POST'])
def UserLogin():
    global user_id
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == username and array[1] == password:
                user_id = username
                status = "success"  
                break
        if status == 'success':
            user_id = username
            context = 'Welcome ' + username
            return render_template('UserScreen.html', msg=context) 
        if status == 'none':
            context = 'Invalid login details'
            return render_template('Login.html', msg=context)





@app.route('/AddFundsAction', methods=['GET', 'POST'])
def AddFundsAction():
    if request.method == 'POST':
        balance = 0.0
        amount = request.form['t1']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        readDetails('account')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            balance = array[1]
        money = float(balance) + float(amount)
        data = str(StateGovernment)+"#"+str(money)+"#"+str(amount)+"#"+str(timestamp)+"#"+"-"+"#Self Deposit\n"
        
        saveDataBlockChain(data,"account")
        output = 'Amount added successfully to blockchain.'
        return render_template('AddFunds.html', msg=output)


@app.route('/AdminScreen', methods=['GET', 'POST'])
def AdminScreen1():
    if request.method == 'GET':
       return render_template('AdminScreen.html', msg='')


@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
    if request.method == 'GET':
       return render_template('AdminLogin.html', msg='')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/UserScreen', methods=['GET', 'POST'])
def UserScreen():
    if request.method == 'GET':
       return render_template('UserScreen.html', msg='')


@app.route('/ViewTransferAmounts', methods=['GET', 'POST'])
def ViewTransferAmounts():
    if request.method == 'GET':
       return render_template('ViewTransferAmounts.html', msg='')


@app.route('/ViewTransfer', methods=['GET', 'POST'])
def ViewTransfer1():
    if request.method == 'GET':
       return render_template('ViewTransfer.html', msg='')

@app.route('/SendAmount', methods=['GET', 'POST'])
def SendAmount():
    if request.method == 'GET':
       return render_template('SendAmount.html', msg='')

@app.route('/Register', methods=['GET', 'POST'])
def Register():
    if request.method == 'GET':
       return render_template('Register.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/ViewUser', methods=['GET', 'POST'])
def ViewUser():
    if request.method == 'GET':
       return render_template('ViewUsers.html', msg='')

@app.route('/AddFunds', methods=['GET', 'POST'])
def AddFunds():
    if request.method == 'GET':
       return render_template('AddFunds.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
       return render_template('Login.html', msg='')

@app.route('/ViewUsers', methods=['GET', 'POST'])
def ViewUsers():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Organization Username', 'Password', 'Phone No', 'Email ID', 'Address']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewUsers.html', msg=output) 


        
@app.route('/RegisterAction', methods=['POST'])
def RegisterAction():
    if request.method == 'POST':
        orgname = request.form['t1']
        password = request.form['t2']
        contact = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == orgname:
                status = user+ "Username already exists"
                break
        if status == "none":
            data = orgname+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "Organization SignUp Completed and details are saved to blockchain"
            return render_template('Register.html', msg=context)
        else:
            context= 'Error in signup process'
            return render_template('Register.html', msg=context)     
    
@app.route('/AdminLoginAction', methods=['POST'])
def AdminLoginAction():
    if request.method == 'POST':
        user = request.form['t1']
        password = request.form['t2']
        if user == 'admin' and password == 'admin':
            context= 'Welcome '+user
            return render_template('AdminScreen.html', msg=context)
        else:
            context= 'Invalid login'
            return render_template('AdminLogin.html', msg=context)
            
        
if __name__ == '__main__':
    app.run()       
