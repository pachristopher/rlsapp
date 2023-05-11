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

            # Get the family members data for this client
            fam_mems_markdown = []
            for fm in client.get('fam_mems', []):
                # check if the family mem is dependent
                if fm.get('dependent', False):
                    # Include the family mem's info in the markdown
                    fm_markdown = f"""| {fm.get('name', '')} | {fm.get('dob', '')} | {fm.get('gender')} | {fm.get('relnship', '')} | {fm.get('ipo_no', '')} |"""
                    fam_mems_markdown.append(fm_markdown)

            # Join the list of fam mem markdowns into a single string
            fam_mems_markdown_str = '\n'.join(fam_mems_markdown)

            # Fill in the template with the client and fam mems info
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
                                        interp=client['interp'],
                                        language=client['language'],
                                        married=client['married'],
                                        fam_mems=fam_mems_markdown_str,
                                        ) 
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

@rlsapp.route('/gen_consult_notes', methods=['GET', 'POST'])
def gen_consult_notes():
    if request.method == 'POST':
        rlsno = request.form['rlsno']

        # Get the client data from the database (assume 'refno' is the client's unique identifier)
        client = collection.find_one({'rlsno': rlsno})
        if client is None:
            return f'Client with RefNo {rlsno} not found', 404
        with open(os.path.join(rlsapp.root_path, 'templates', 'consult_notes_template.md'), 'r') as template_file:
            template = template_file.read()

            # Get the family members data for this client
            fam_mems_markdown = []
            for fm in client.get('fam_mems', []):
                fm_markdown = f"""| {fm.get('name', '')} | {fm.get('dob', '')} | {fm.get('gender')} | {fm.get('relnship', '')} | {fm.get('ipo_no', '')} |"""
                fam_mems_markdown.append(fm_markdown)

            # Join the list of fam mem markdowns into a single string
            fam_mems_markdown_str = '\n'.join(fam_mems_markdown)

            # Generate grounds of appeal
            nar_basis=client['basis']
            prompt = "" + nar_basis

            # Fill in the template with the client and fam mems info
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
                                        interp=client['interp'],
                                        language=client['language'],
                                        married=client['married'],
                                        fam_mems=fam_mems_markdown_str,
                                        doa=client['doa'],
                                        dod=client['dod'],
                                        reasons=client['reasons'],
                                        basis=client['basis'],
                                        travel=client['travel'],

                                        ) 
        filename = f'{rlsno}_consult_notes.md'
        filepath = os.path.join(rlsapp.root_path, 'data', filename)
        with open(filepath, 'w') as file:
            file.write(markdown_text)
        response = make_response(markdown_text)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-Type'] = 'text/markdown'
        return response

    return render_template('index.html')


