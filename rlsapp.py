import os
from flask import Flask, render_template, url_for, request, make_response
from pymongo import MongoClient

# Connect to the MongoDB database:
client = MongoClient('mongodb://localhost:27017/')
db = client['rls']

# Create a collection in the database:
collection = db['users']

# Create a route for the web form and render the template with the input fields:
rlsapp = Flask(__name__)

# Define the options for the nationality and coi fields
with open(os.path.join(rlsapp.root_path, 'static', 'country_list.txt')) as f:
    NATIONALITY_OPTIONS = [line.strip() for line in f.readlines()]

# Define the options for the language field
with open(os.path.join(rlsapp.root_path, 'static', 'languages.txt')) as f:
    LANGUAGE_OPTIONS = [line.strip() for line in f.readlines()]

# Define the routes for the app

@rlsapp.route("/")
def index():
    return render_template("index.html")


@rlsapp.route('/per_details', methods=['GET', 'POST'])
def per_details():
    if request.method == 'POST':
        family = []
        for i in range(int(request.form['num_fam_mems'])):
            fam_mem = {}
            fam_mem['name'] = request.form['fam_name_' + str(i)]
            fam_mem['dob'] = request.form['fam_dob_' + str(i)]
            fam_mem['gender'] = request.form['fam_mem_' + str(i)]
            fam_mem['relnship'] = request.form['fam_mem_' + str(i)]
            fam_mem['refno'] = request.form['fam_mem_' + str(i)]
            fam_mem['nationality'] = request.form['fam_mem-' + str(i)]
            family.append(fam_mem)
        data = {
            'refno': request.form['refno'],
            'ipono': request.form['ipono'],
            'solicitor': request.form['solicitor'],
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'alias': request.form['alias'],
            'dob': request.form['dob'],
            'gender': request.form.get('gender'),
            'address': request.form['address'],
            'telno': request.form['telno'],
            'passport': request.form['passport'],
            'nationality': request.form['nationality'],
            'ethnicity': request.form['ethnicity'],
            'religion': request.form['religion'],
            'coi': request.form['coi'],
            'language': request.form['language'],
            'married': request.form.get('married'),
            'family': family,
        }
        collection.insert_one(data)
        return 'Data saved to database'
    else:
        return render_template('per_details.html', nationality_options=NATIONALITY_OPTIONS, language_options=LANGUAGE_OPTIONS)


"""	To create a page that queries the MongoDB database and displays the data, 
	you can create a new route in your Flask app. 
	Here's an example of how you can create a new route that queries the database and displays the data:
	In this example, the data_markdown function queries the MongoDB database using the find method, 
	which returns a cursor that can be used to iterate over the documents in the collection. 
	The results variable is passed to the data.html template as a parameter.
	
	To create a markdown file that places the data in the markdown file, 
	you can use the pandoc command-line tool to convert the HTML output of the data route to markdown format. 
	Here's an example of how you can create a new route that generates the markdown file:
	In this example, the RefNo is obtained from the first document in the results cursor, 
	or set to 'unknown' if the cursor is empty. 
	The filename is then constructed using the RefNo and the .md extension. 
	The file is saved to the data directory in the Flask app root directory using the open function.

	The make_response object is still returned as before to download the file, 
	but with the filename set to the constructed filename.
"""

from bson import ObjectId
import markdown

@rlsapp.route('/gen_ipat_appeal', methods=['GET', 'POST'])
def gen_ipat_appeal():
    if request.method == 'POST':
        refno = request.form['refno']

        # Get the client data from the database (assume 'refno' is the client's unique identifier)
        client = collection.find_one({'refno': refno})
        if client is None:
            return f'Client with RefNo {refno} not found', 404
        with open(os.path.join(rlsapp.root_path, 'templates', 'user_template.md'), 'r') as template_file:
            template = template_file.read()
            markdown_text = template.format(refno=client['refno'],
                                        ipono=client['ipono'],
                                        solicitor=client['solicitor'],
                                        fname=client['fname'],
                                        lname=client['lname'],
                                        alias=client['alias'],
                                        dob=client['dob'],
                                        gender=client['gender'],
                                        address=client['address'],
                                        telno=client['telno'],
                                        passport=client['passport'],
                                        nationality=client['nationality'],
                                        ethnicity=client['ethnicity'],
                                        religion=client['religion'],
                                        coi=client['coi'],
                                        language=client['language'],
                                        married=client['married'],) 
        filename = f'{refno}_ipat_appeal.md'
        filepath = os.path.join(rlsapp.root_path, 'data', filename)
        with open(filepath, 'w') as file:
            file.write(markdown_text)
        response = make_response(markdown_text)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-Type'] = 'text/markdown'
        return response

    return render_template('index.html')


"""
# Same as above function but for latex instead of markdown

@rlsapp.route('/data/latex')
def data_latex():
    results = collection.find()
    html = render_template('data.html', results=results)
    latex = subprocess.check_output(['pandoc', '-f', 'html', '-t', 'latex'], input=html.encode('utf-8')).decode('utf-8')
    refno = results[0]['refno'] if results.count() > 0 else 'unknown'
    filename = f'{refno}.tex'
    filepath = os.path.join(rlsapp.root_path, 'data', filename)
    with open(filepath, 'w') as file:
        file.write(latex)
    response = make_response(latex)
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-Type'] = 'application/x-latex'
    return response
"""

# Run the Flask app:
if __name__ == '__main__':
    rlsapp.run(debug=True, port=9003) # In macos, you can't use the default 5000 port as that is already in use.
