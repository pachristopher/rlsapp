from flask import render_template_string, request, make_response, send_file
from rlsapp import rlsapp, collection

import os
from bson import ObjectId
import markdown

@rlsapp.route('/gen_ipat_appeal', methods=['GET', 'POST'])
def gen_ipat_appeal():
    if request.method == 'POST':
        rlsno = request.form['rlsno']

        # Get the client data from the database (assume 'refno' is the client's unique identifier)
        client = collection.find_one({'rlsno': rlsno})
        if client is None:
            return f'Client with RefNo {rlsno} not found', 404
        with open(os.path.join(rlsapp.root_path, 'templates', 'ipat_appeal_template.md'), 'r') as template_file:
            template = template_file.read()
            markdown_text = template.format(rlsno=client['rlsno'],
                                        ipo_no=client['ipo_no'],
                                        solicitor=client['solicitor'],
                                        fname=client['fname'],
                                        lname=client['lname'],
                                        alias=client['alias'],
                                        dob=client['dob'],
                                        gender=client['gender'],
                                        address=client['address'],
                                        telno=client['telno'],
                                        email=client['email'],
                                        passport=client['passport'],
                                        nationality=client['nationality'],
                                        ethnicity=client['ethnicity'],
                                        religion=client['religion'],
                                        language=client['language'],
                                        married=client['married'],) 
        filename = f'{rlsno}_ipat_appeal.md'
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
