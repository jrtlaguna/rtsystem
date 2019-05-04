from app.positions.services import get_position_list, get_section_division_list
from app.profile.models import Admin, Chief, Employee
from flask import Blueprint, render_template
from flask_login import current_user

profilebp = Blueprint('profile', __name__, template_folder='templates')

@profilebp.route('/profile')
def profile():
    profile = None

    if current_user.account_type.lower() == 'admin':
        profile = Admin(current_user.username)
    elif current_user.account_type.lower() == 'chief':
        profile = Chief(current_user.username)
    else:
        profile = Employee(current_user.username)

    positions = get_position_list()
    sections_divisions = get_section_division_list()

    return render_template('my_profile.html', profile=profile, positions=positions, section_divisions=sections_divisions)