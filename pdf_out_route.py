from flask import render_template_string, request, make_response, send_file
from rlsapp import rlsapp, collection

import os
import pdfrw 

@rlsapp.route('/fill_pdf', methods=['GET', 'POST'])
def fill_pdf():
    if request.method == 'POST':
        rlsno = request.form['rlsno']

        # Get the client data from the database (assume 'refno' is the client's unique identifier)
        client = collection.find_one({'rlsno': rlsno})
        if client is None:
            return f'Client with RefNo {rlsno} not found', 404
        # Load the pdf form template
        template_path = os.path.join(os.path.dirname(__file__), 'inadmiss_template.pdf')
        template_pdf = pdfrw.PdfReader(template_path)

        # Fill in the template with the client info
        rlsno=client['rlsno'],
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

        # Fill the form fields with the user's input
        template_pdf.Root.AcroForm.Fields[0].update(pdfrw.PdfDict(V=rlsno))
        template_pdf.Root.AcroForm.Fields[1].update(pdfrw.PdfDict(V=ipo_no))
        template_pdf.Root.AcroForm.Fields[2].update(pdfrw.PdfDict(V=fname))

        # Write the filled PDF form to a new file
        output_path = os.path.join(os.path.dirname(__file__), 'output.pdf')
        pdfrw.PdfWriter().write(output_path, template_pdf)

        # Return the filled PDF form to the user
        return send_file(output_path)

    return render_template('index.html')
