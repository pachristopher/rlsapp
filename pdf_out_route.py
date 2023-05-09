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
        template_path = os.path.join(os.path.dirname(__file__), 'templates/inadmiss_template.pdf')
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
        fam_mem_name=client['fam_mems'][0]['name']
        fam_mem_dob=client['fam_mems'][0]['dob']
        fam_mem_gender=client['fam_mems'][0]['gender']
        fam_mem_relnship=client['fam_mems'][0]['relnship']
        fam_mem_ipo_no=client['fam_mems'][0]['ipo_no']

        # Fill the form fields with the user's input
        template_pdf.Root.AcroForm.Fields[0].update(pdfrw.PdfDict(V=dob))
        template_pdf.Root.AcroForm.Fields[1].update(pdfrw.PdfDict(V=ipo_no))
        template_pdf.Root.AcroForm.Fields[2].update(pdfrw.PdfDict(V=alias))
        template_pdf.Root.AcroForm.Fields[3].update(pdfrw.PdfDict(V=address))
        template_pdf.Root.AcroForm.Fields[4].update(pdfrw.PdfDict(V=telno))
        template_pdf.Root.AcroForm.Fields[5].update(pdfrw.PdfDict(V=nationality))
        template_pdf.Root.AcroForm.Fields[6].update(pdfrw.PdfDict(V=fam_mem_name))
        template_pdf.Root.AcroForm.Fields[7].update(pdfrw.PdfDict(V=fam_mem_dob))
        template_pdf.Root.AcroForm.Fields[8].update(pdfrw.PdfDict(V=fam_mem_gender))
        template_pdf.Root.AcroForm.Fields[9].update(pdfrw.PdfDict(V=fam_mem_relnship))
        template_pdf.Root.AcroForm.Fields[10].update(pdfrw.PdfDict(V=fam_mem_ipo_no))
        template_pdf.Root.AcroForm.Fields[11].update(pdfrw.PdfDict(V=fam_mem_dob))

        # Write the filled PDF form to a new file
        output_path = os.path.join(os.path.dirname(__file__), 'data/output.pdf')
        pdfrw.PdfWriter().write(output_path, template_pdf)

        # Return the filled PDF form to the user
        return send_file(output_path)

    return render_template('index.html')
