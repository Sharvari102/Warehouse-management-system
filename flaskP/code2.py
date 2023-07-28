from logging import debug 
from flask import Flask, render_template,request,session,redirect,url_for,flash
from flask_pymongo import PyMongo
import bcrypt

from random import randint

app=Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/Warehouse'
mongo=PyMongo(app)

@app.route('/',methods=['GET','POST'])
def home(): 

    return render_template('home1.html')

@app.route('/loginfail',methods=['GET','POST'])
def loginfail():
    return render_template('loginfail.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        users=mongo.db.users.find_one({'username':request.form.get('username')})
        if users is None :
            if request.form.get('password') == request.form.get('confirmpassword') : 
                
                mongo.db.users.insert_one({'username' : request.form.get('username'),'password':request.form.get('password')})
                return redirect(url_for('signin'))
            else :
                return render_template('signup1.html')
        else : 
            return render_template('signup2.html')
    else: 
        return render_template ('signup.html')


@app.route('/signup1',methods=['GET','POST'])
def signup1():
    return render_template('signup1.html')

@app.route('/signup2',methods=['GET','POST'])
def signup2():
    return render_template('signup2.html')

@app.route('/signin',methods=['GET','POST'])
def signin():
    
    if request.method=='POST':
        users=mongo.db.users.find_one({'username':request.form.get('username')})
        print(users['username'])
        if users :
            if users['password'] == request.form.get('password') : 
                return redirect(url_for('dashboard'))
            return render_template('loginfail.html')
        return render_template('loginfail.html')    
    else :        
        return render_template ('login.html')

@app.route('/aboutus',methods=['GET','POST'])
def aboutus():
    return render_template('about.html')

@app.route('/contactus',methods=['GET','POST'])
def contactus():
    return render_template('contact.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    
    return render_template('dashnew.html')

@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    if request.method=="POST": 
        product = request.form.get('productname')
        id=randint(111,999)
        company=request.form.get('company')
        stock=request.form.get('stock')
        location=request.form.get('location')
        mongo.db.product.insert_one({'product_name':product,'product_id':id,'company':company,'stock':stock,'location':location})
        
        print(product)
        print(id)
        print(company)
        print(stock)
        print(location)
        flash(" Product Added Successfully!")

        

        return redirect(url_for('addproduct'))
    return render_template('add product.html')

@app.route('/addcustomer',methods=['GET','POST'])
def addcustomer():
    if request.method=="POST": 
        name= request.form.get('customername')
        id=request.form.get('phono')
        email=request.form.get('email')
        address=request.form.get('address')
        
        mongo.db.customer.insert_one({'customer_name':name,'phone_no':id,'email_id':email,'Address':address})
        
        print(name)
        print(id)
        print(email)
        print(address)
        
        flash(" Customer Added Successfully!")
        return redirect(url_for('addcustomer'))

    return render_template('add customer.html')

@app.route('/addsupplier',methods=['GET','POST'])
def addsupplier():

    if request.method=="POST": 
        name= request.form.get('suppliername')
        id=request.form.get('phono')
        email=request.form.get('email')
        address=request.form.get('address')
        
        mongo.db.supplier.insert_one({'supplier_name':name,'phone_no':id,'email_id':email,'Address':address})
        
        print(name)
        print(id)
        print(email)
        print(address)
        
        flash(" Supplier Added Successfully!")
        return redirect(url_for('addsupplier'))

    
    return render_template('add supplier.html')

@app.route('/productreport',methods=['GET','POST'])
def productreport():
    report=mongo.db.product.find()

    return render_template('productreport.html',report=report)

@app.route('/update/<int:product_id>',methods=['GET','POST'])
def update(product_id):
     
    if request.method == "POST" :
        product = request.form.get('productname')
        
        company=request.form.get('company')
        stock=request.form.get('stock')
        location=request.form.get('location')

        mongo.db.product.update_one({'product_id': product_id},{'$set':{'product_name':product,'company':company,'stock':stock,'location':location}})
        
        return redirect(url_for('productreport'))

    report=mongo.db.product.find_one({'product_id': product_id})

    return render_template('update.html',report=report)

@app.route('/delete/<int:product_id>',methods=['GET','POST'])
def delete(product_id):
    report=mongo.db.product.delete_one({'product_id':product_id})

    return redirect(url_for('productreport'))










if __name__ == '__main__':
    app.secret_key="mysecret"
    app.run(debug=True)

    