from app.accounts.services import create_account
from app.positions.services import get_position_list, get_section_division_list
from flask import Blueprint, render_template, request
from json import dumps

accountsbp = Blueprint('accounts', __name__, template_folder='templates')

@accountsbp.route('/accounts')
def accounts():
    positions = get_position_list()
    section_divisions = get_section_division_list()

    return render_template('accounts.html', positions=positions, section_divisions=section_divisions)


@accountsbp.route('/accounts/create', methods=['POST'])
def create():
    data = {
        'username': request.form['username'],
        'password': request.form['password'],
        'first_name': request.form['first-name'],
        'middle_initial': request.form['middle-initial'],
        'last_name': request.form['last-name'],
        'active': True if 'active' in request.form.keys() else False,
        'account_type': request.form['account-type']
    }
    
    if request.form['account-type'] == 'Employee':
        data['position'] = request.form['position']
        data['contact_number'] = request.form['contact-number']
        data['is_working_sun'] = True if 'is-working-sun' in request.form.keys() else False
        data['is_working_mon'] = True if 'is-working-mon' in request.form.keys() else False
        data['is_working_tue'] = True if 'is-working-tue' in request.form.keys() else False
        data['is_working_wed'] = True if 'is-working-wed' in request.form.keys() else False
        data['is_working_thu'] = True if 'is-working-thu' in request.form.keys() else False
        data['is_working_fri'] = True if 'is-working-fri' in request.form.keys() else False
        data['is_working_sat'] = True if 'is-working-sat' in request.form.keys() else False

    else:
        data['section_division'] = request.form['section-division']

    message = create_account(data)
    

    return dumps({'status': message})