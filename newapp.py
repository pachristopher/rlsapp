from flask import Flask, request, render_template, url_for, redirect, make_response

newapp = Flask(__name__)

# Config the app to use a MongoDB database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['rls']
collection = db['users']

# Define the options for the nationality field 
with open('static/country_list.txt', 'r') as f:
    NAT_OPTIONS = [line.strip() for line in f.readlines()]

# Define the options for the language field
with open('static/languages.txt', 'r') as f:
    LANG_OPTIONS = [line.strip() for line in f.readlines()]

# Create a route to handle client info form 
@newapp.route('/form', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get client info from form
        rlsno = request.form.get('rlsno')
        ipo_no = request.form.get('ipo_no')
        solicitor = request.form.get('solicitor')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        alias = request.form.get('alias')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        email = request.form.get('email')
        passport = request.form.get('passport')
        nationality = request.form.get('nationality')
        ethnicity = request.form.get('ethnicity')
        religion = request.form.get('religion')
        language = request.form.get('language')
        married = request.form.get('married')
        num_fam_mems = int(request.form.get('num_fam_mems'))

        # Create a list to store family member info
        fam_mems = []

        # Loop through the number of family members and get their info
        for mem in range(num_fam_mems):
            fam_mem = {}
            fam_mem['name'] = request.form.get('fam_name_' + str(mem))
            fam_mem['ipo_no'] = request.form.get('fam_ipo_no_' + str(mem))
            fam_mem['address'] = request.form.get('fam_address' + str(mem))
            fam_mem['dob'] = request.form.get('fam_dob_' + str(mem))
            fam_mem['gender'] = request.form.get('fam_gender_' + str(mem))
            fam_mem['relnship'] = request.form.get('fam_relnship_' + str(mem))
            fam_mem['nationality'] = request.form.get('fam_nationality_' + str(mem))
            fam_mems.append(fam_mem)

        # Insert client info into db
        client_data = {
            'rlsno': rlsno,
            'ipo_no': ipo_no,
            'solicitor': solicitor,
            'fname': fname,
            'lname': lname,
            'alias': alias,
            'dob': dob,
            'gender': gender,
            'address': address,
            'email': email,
            'passport': passport,
            'nationality': nationality,
            'ethnicity': ethnicity,
            'religion': religion,
            'language': language,
            'married': married,
            'fam_mems': fam_mems,
        }

        result = collection.insert_one(client_data)

        # Redirect to success page
        return render_template('success.html')

    # If the request method is GET, render the form
    else:
        # Render the form template with the nationalities dropdown and default number of family members
        return render_template('form.html', nationality_options=NAT_OPTIONS, language_options=LANG_OPTIONS, num_fam_mems=0)

# Run the app
if __name__ == '__main__':
    newapp.run(port=9003, debug=True)
