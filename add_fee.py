from flask import render_template, render_template_string, request, make_response, send_file
from rlsapp import rlsapp, collection

import os

FEE_CATS = {"Case Stage 1": {"Applicant": 300, "Spouse": 150, "Child": 85},
    "Case Stage 2": {"Applicant": 300, "Spouse": 150, "Child": 85},
    "Case Stage 3": {"Applicant": 400, "Spouse": 200, "Child": 80},
    "Case Stage 3 accelerated": {"Applicant": 250, "Spouse": 175, "Child": 80},
    "Case Stage 4": {"Applicant": 100, "Spouse": 100, "Child": 80},
    "Case Stage 5": {"Applicant": 250, "Spouse": 175, "Child": 80},
    "Case Stage 1A": {"Applicant": 195, "Spouse": 100, "Child": 80},
    "Case Stage 1B": {"Applicant": 300, "Spouse": 150, "Child": 80},
    "Inadmissible": {"Applicant": 300, "Spouse": 150, "Child": 80},
    "Reception Conditions": {"Applicant": 400, "Spouse": 200, "Child": 80},
    "Reception Conditions, no oral hearing": {"Applicant": 150, "Spouse": 75, "Child": 50} }


@rlsapp.route('/add_fee', methods=['GET', 'POST'])
def add_fee():
    if request.method == 'POST':
        rlsno = request.form['rlsno']

        # Get the client data from the database (assume 'refno' is the client's unique identifier)
        client = collection.find_one({'rlsno': rlsno})
        if client is None:
            return f'Client with RefNo {rlsno} not found', 404
        else:
            # Get fees info for this client from form data
            fee_cat = request.form['fee_cat']
            date_invoiced = request.form['date_invoiced']
            date_paid = request.form['date_paid']
            vat = request.form['vat']
            hold_tax = request.form['hold_tax']

            # Create a query to find the existing document by rlsno
            query = {'rlsno': rlsno}

            # Append fee_item into db
            new_fee = {
                '$push': {
                    'fees': {
                        'fee_cat': fee_cat,
                        'date_invoiced': date_invoiced,
                        'date_paid': date_paid,
                        'vat': vat,
                        'hold_tax': hold_tax,
                    }    
                }
            }

            collection.update_one(query, new_fee)
            return 'Fee item added successfully'
            
            # If the request method is GET, render the form
    else:
        # Render the fees template with the fee_cats dropdown
        return render_template('add_fee.html', fee_cats=FEE_CATS)

