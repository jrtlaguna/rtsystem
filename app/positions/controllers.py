from app.accounts.services import get_verifiers
from app.positions.services import check_position_duplicate
from app.positions.services import create_position, create_section_division
from app.positions.services import delete_position_record, delete_secdiv_record
from app.positions.services import get_section_divisions_and_positions, get_verifier
from app.positions.services import update_secdiv_record, update_position_record
from flask import Blueprint, render_template, request
from json import dumps

positionsbp = Blueprint('positions', __name__, template_folder='templates')

@positionsbp.route('/positions')
def positions():
    section_divisions = get_section_divisions_and_positions()
    verifiers = get_verifiers()

    return render_template('positions.html', section_divisions=section_divisions, verifiers=verifiers)


@positionsbp.route('/positions/new-position', methods=['POST'])
def new_position():
    data = {
        'title': request.form['position-title'],
        'section_division': request.form['section-division']
    }

    create_position(data)

    return dumps({'status': 'OK'})


@positionsbp.route('/positions/new-section-division', methods=['POST'])
def new_section_division():
    data = {
        'name': request.form['name'],
        'verifier': request.form['verifier']
    }

    create_section_division(data)

    return dumps({'status': 'OK'})


@positionsbp.route('/positions/get-verifier', methods=['GET'])
def get_sec_div_verifier():
    sec_div = request.args.get('section_division')
    verifier = get_verifier(sec_div)

    data = {
        'verifier': verifier
    }

    return dumps({'status': 'OK', 'data': data})


@positionsbp.route('/positions/delete-secdiv')
def delete_secdiv():
    sec_div = request.args.get('sec_div')
    delete_secdiv_record(sec_div)

    return dumps({'status': 'OK'})


@positionsbp.route('/positions/update-secdiv', methods=['POST'])
def update_secdiv():
    current = request.form['current_name']
    new = request.form['name']
    verifier = request.form['verifier']

    update_secdiv_record(current, new, verifier)
    
    return dumps({'status': 'OK'})


@positionsbp.route('/positions/update-pos', methods=['POST'])
def update_position():
    current = request.form['cur_pos']
    cur_secdiv = request.form['cur_secdiv']
    new = request.form['position']
    secdiv = request.form['secdiv']
    
    if current != new or cur_secdiv != secdiv:
        duplicate = check_position_duplicate(new, secdiv)

        if duplicate:
            return dumps({'status': 'FAILED: DUPLICATE ENTRY'})

    update_position_record(current, new, secdiv)
    return dumps({'status': 'OK'})


@positionsbp.route('/positions/delete-position')
def delete_position():
    pos = request.args.get('pos')
    sec_div = request.args.get('secdiv')

    delete_position_record(sec_div, pos)

    return dumps({'status': 'OK'})