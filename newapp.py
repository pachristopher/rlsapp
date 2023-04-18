from flask import Flask, request, render_template, url_for, redirect, make_response

newapp = Flask(__name__)

# Config the app to use a MongoDB database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['rls']
collection = db['users']

# Define the options for the nationalities field 
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
        name = request.form.get('name')
        per_id = request.form.get('per_id')
        address = request.form.get('address')
        religion = request.form.get('religion')
        nationality = request.form.get('nationality')
        language = request.form.get('language')
        num_fam_mems = int(request.form.get('num_fam_mems'))

        # Create a list to store family member info
        fam_mems = []

        # Loop through the no of amily members and get their info
        for mem in range(num_fam_mems):
            fam_mem = {}
            fam_mem['name'] = request.form.get('fam_name_' + str(mem))
            fam_mem['per_id'] = request.form.get('fam_per_id_' + str(mem))
            fam_mem['address'] = request.form.get('fam_address' + str(mem))
            fam_mems.append(fam_mem)

        # Insert client info into db
        client_data = {
            'name': name,
            'per_id': per_id,
            'address': address,
            'religion': religion,
            'nationality': nationality,
            'language': language,
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
