from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request,redirect, url_for, flash, jsonify, session
import CollegeSearch
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import re  # Import the re module for regex operations
from flask_bcrypt import Bcrypt


############# connect with MongoDB database
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.debug = True
app.config['SECRET_KEY'] = 'hester123'
uri = "mongodb+srv://hester123:hester123@schools.rswmjwr.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.myDB
users = db.users
pmInfor = db.pmInfor
stdInfor= db.stdInfor

# Regex pattern for lowercase letters and numbers
username_regex = re.compile(r"^[a-z0-9]+$")

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

user_model = {
    'user_id': str,  # This will be a unique identifier for the user
    'username': str,
    'email': str,
    'password': str,  # Always store hashed passwords
    'user_type': str
}


#Home Page
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return f'You are logged in as {username}'
    return render_template('index.html')


# Function to validate the password
def is_valid_password(password):
    return len(password) >= 6 and any(char.isupper() for char in password)

####################sign up page
@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        user_Name = request.form.get('username')
        _email = request.form.get('email')
        pass_word = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        hashed_password = generate_password_hash(pass_word)
        user_type = request.form.get('userType')
        user_id = str(ObjectId())

        #if found in database showcase that it's found 
        user_Name_found = users.find_one({"username": user_Name})
        _email_found = users.find_one({"email":_email})
     

        # Validate the username using the regex pattern
        if not username_regex.match(user_Name):
            flash('Invalid characters in the username. Please use only lowercase letters and numbers.')
            return redirect(url_for('signup'))
        # Check if the username is already taken 
        elif users.find_one({"username": user_Name.lower()}):
            flash('Username already taken. Please choose a different one.')
            return redirect(url_for('signup'))
        elif user_Name_found:
            flash('Username already exists, please choose another one!')
        elif _email_found:
            flash('This email is already associated with another account!')
        #if didnt fill in necessary information 
        elif not user_Name:
            flash('User name is required!')
        elif not _email:
            flash('Email is Required!')  
        elif not pass_word:
            flash('Password is Required!') 
        elif not confirm_password:
            flash('Confirm Password is Required!')
        elif pass_word != confirm_password:
            flash('Passwords do not match!')
        elif not is_valid_password(pass_word):
            flash('Password must be at least 6 characters long and contain at least one uppercase letter.')
        elif not user_type:
           flash('User Type is Required!')
        
        else:
            #make a dictionary
            req_fields = {'user_id' : user_id, 'username' : user_Name, 'email' :_email, 'pass_word' : hashed_password, 'userType' : user_type}
            
            try:
                #add user to database
                users.insert_one(req_fields)
                print("User successfully added to the database!")
                # #depent on user type to return profile page
                if user_type == 'program manager':
                    return redirect(url_for('PMdashboard'))
                elif user_type == 'student':
                    return redirect(url_for('studentDashboard'))
            except Exception as e:
                print(f"Error inserting user into MongoDB: {e}") 
    all_info = users.find()
    return render_template('signup.html', users=all_info)

# login function already run error message', 'Invalid username or password. Please try again.')
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        user_email = request.form.get('email')
        password = request.form.get('password')

        user = db.users.find_one({"email":user_email})
        if user:
            if check_password_hash(user['pass_word'], password) == True:
            
               # User found and password matches, proceed with login, has problem here
                session['email'] = user['email']   
                # Redirect to the appropriate dashboard based on user type
                if user['userType'] =='program manager':
                    return redirect(url_for('PMdashboard'))
                elif user['userType'] == 'student':
                    return redirect(url_for('studentDashboard'))
            else:
                flash('Invalid Email or Password. Please try again.')
   
        else:
            flash('User not found. Please check your email and try again.')
    return render_template('login.html')


           
############# PM dashboard
@app.route('/PMdashboard')
def PMdashboard():
    return render_template('PMdashboard.html')               
    

############# PM Profile page, after eidt return back to dashboard
@app.route('/Profile_PM', methods=['GET','POST'])
def Profile_PM():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number= request.form.get('phone_number')
        state = request.form.get('state')
        city=request.form.get('city')
        
        if not first_name:
            flash('First Name is required!')
        elif not last_name:
            flash('Last name is Required!') 
        elif not phone_number:
            flash('phone number is Required!') 
        elif not state:
            flash('State is Required!') 
        elif not city:
           flash('City is Required!')
        else:
            #make a dictionary
            req_fields = {'first_name' : first_name, 'last_name' : last_name,'phone_number' : phone_number, 'state' : state, 'city' : city}
           
            pmInfor.insert_one(req_fields)
            return redirect(url_for('PMdashboard'))
    all_info = pmInfor.find()
    return render_template('Profile_PM.html', pmInfor=all_info)


@app.route('/studentDashboard')
def studentDashboard():
    return render_template('studentDashboard.html')

#############student Profile page, after eidt return back to dashboard
@app.route('/Profile_student', methods=['GET','POST'])
def Profile_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number= request.form.get('phone_number')
        state = request.form.get('state')
        city=request.form.get('city')
        ResidencyStatus = request.form.get('ResidencyStatus')
        birthday= request.form.get("birthday")
        desiredMajor= request.form.get("desiredMajor")
        AcademicInterests= request.form.get("AcademicInterests")
        ProgramPerferences=request.form.get("ProgramPerferences")
        schoolType=request.form.get("schoolType")
        preferredTuition=request.form.get("preferredTuition")
        graduationYear=request.form.get("graduationYear")
        
        if not first_name:
            flash('First name is required!')
        elif not last_name:
            flash('Last name is Required!') 
        elif not phone_number:
            flash('Phone Number is Required!') 
        elif not state:
            flash('State is Required!') 
        elif not city:
           flash('City is Required!')
        elif not ResidencyStatus:
           flash('ResidencyStatus is Required!')
        elif not birthday:
           flash('Birthday is Required!')
        elif not desiredMajor:
           flash('Major is Required!')
        elif not  preferredTuition:
           flash('Choose Preferred Tuition is Required!')
       
        else:
            #make a dictionary
            req_fields = {'first_name' : first_name, 'last_name' : last_name,'phone_number' :phone_number, 'state' : state, 'city' : city,'ResidencyStatus': ResidencyStatus, 'birthday':birthday, 'desiredMajor':desiredMajor, 'schoolType' :schoolType, 'preferredTuition':preferredTuition,'AcademicInterests': AcademicInterests, 'ProgramPerferences':ProgramPerferences,'graduationYear': graduationYear}
            #add user to database
            stdInfor.insert_one(req_fields)
            return redirect(url_for('studentDashboard'))
       
   
    all_info = stdInfor.find()

    return render_template('Profile_student.html', stdInfor=all_info)


@app.route('/regsuc')
def regSuc():
        #depent on user type to return profile page
        return render_template('RegisterSuccess.html')

@app.route('/Notifications')
def Notifications():
    # Your logic for the Notifications page
    return render_template('Notifications.html')

@app.route('/Favorites')
def Favorites():
    return render_template('Favorites.html')


@app.route('/go_back')
def go_back():
    # Implement any logic here if needed
    return redirect(url_for('index'))  # Redirect to the desired location 

@app.route('/signout')
def signout():
    # Clear the session data
    session.clear()
    flash('You have been logged out.', 'success')
    return render_template('signout.html')

############
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

#############
# @app.route('/response')
# def query():
#     db2 = client.Schools 
#     schoolsList = db2.Schools
  
#     cursor = schoolsList.find()
#     for scho in cursor:
#         name = scho["college_name"]
#         city = scho["city"]
#         state = scho["state"]
#         tuition= scho["tuition"]
#         major = scho["major"]
#         program = scho["program"]
#         print(scho)
      
#     return render_template("response.html", res = name, res1 = city, res3 = state, res4 = tuition, res5 = major, res6 = program)

  



#only if you run this file will webserver run
if __name__=="__main__":
    #anything we make a change, it will rerun server
    app.run(debug=True)



