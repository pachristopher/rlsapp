from flask import Flask, request, render_template, url_for, redirect, make_response
import json

rlsapp = Flask(__name__)

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

# Home Page
@rlsapp.route("/")
def index():
    return render_template("index.html")

# Client Input Page
# Create a route to handle client info form 
@rlsapp.route('/per_details', methods=['GET', 'POST'])
def per_details():
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
        telno = request.form.get('telno')
        email = request.form.get('email')
        occupation = request.form.get('occupation')
        pol = request.form.get('pol')
        passport = request.form.get('passport')
        nationality = request.form.get('nationality')
        ethnicity = request.form.get('ethnicity')
        religion = request.form.get('religion')
        interp = request.form.get('interp') == 'on'
        language = request.form.get('language')
        doa = request.form.get('doa')
        dod = request.form.get('dod')
        prior = request.form.get('prior')
        prior_state = request.form.get('prior_state')
        travel = request.form.get('travel')
        smuggler = request.form.get('smuggler')
        asylum = request.form.get('asylum')
        reasons = request.form.getlist('reasons')
        sub_prot = request.form.get('sub_prot')
        basis = request.form.get('basis')
        med = request.form.get('med')
        married = request.form.get('married') == 'on'
        num_fam_mems = int(request.form.get('num_fam_mems'))

        # Create a list to store family member info
        fam_mems = []

        # Loop through the number of family members and get their info
        for mem in range(num_fam_mems):
            fam_mem = {}
            fam_mem['name'] = request.form.get('fam_name_' + str(mem))
            fam_mem['ipo_no'] = request.form.get('fam_ipo_no_' + str(mem))
            fam_mem['address'] = request.form.get('fam_address_' + str(mem))
            fam_mem['dob'] = request.form.get('fam_dob_' + str(mem))
            fam_mem['gender'] = request.form.get('fam_gender_' + str(mem))
            fam_mem['relnship'] = request.form.get('fam_relnship_' + str(mem))
            fam_mem['dependent'] = request.form.get('fam_dependent_' + str(mem)) == 'on'
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
            'telno': telno,
            'passport': passport,
            'nationality': nationality,
            'ethnicity': ethnicity,
            'religion': religion,
            'pol': pol,
            'occupation': occupation,
            'language': language,
            'interp': interp,
            'doa': doa,
            'dod': dod,
            'prior': prior,
            'prior_state': prior_state,
            'travel': travel,
            'smuggler': smuggler,
            'asylum': asylum,
            'reasons': reasons,
            'sub_prot': sub_prot,
            'basis': basis,
            'med': med,
            'married': married,
            'fam_mems': fam_mems,
        }

        result = collection.insert_one(client_data)

        # Redirect to success page
        return render_template('success.html')

    # If the request method is GET, render the form
    else:
        # Render the form template with the nationalities dropdown and default number of family members
        return render_template('per_details.html', nationality_options=NAT_OPTIONS, language_options=LANG_OPTIONS, num_fam_mems=0)

# Custom jinja2 filter to convert Python object to JSON
@rlsapp.template_filter('jsonify')
def jsonify_filter(obj):
    return json.dumps(obj)

# Print Form Page
# Import the routes from out_routes.py
from out_routes import *
from pdf_out_route import *
from add_fee import *

# Run the app
if __name__ == '__main__':
    rlsapp.run(port=9003, debug=True)
