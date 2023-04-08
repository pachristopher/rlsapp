from flask import Flask, request, render_template, url_for, redirect

newapp = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['rls']
collection = db['users']

@newapp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        address = request.form['address']
        family = []
        num_family_members = int(request.form['num_family_members'])
        for i in range(num_family_members):
            family_member = {}
            family_member['name'] = request.form.get('family_name_' + str(i))
            family_member['age'] = request.form.get('family_age_' + str(i))
            family_member['reln'] = request.form.get('family_reln_' + str(i))
            family.append(family_member)
        collection.insert_one({
            'name': name,
            'age': age,
            'address': address,
            'family': family
        })
        return redirect(url_for('form'))
    return render_template('form.html', num_family_members=1)

if __name__ == '__main__':
    newapp.run(port=9003, debug=True)
