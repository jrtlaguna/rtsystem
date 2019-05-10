from flask import Blueprint, render_template, request, url_for
from app.profile.models import Chief, Employee
from app.reports.services import *
from app.pending.controllers import get_week_name, period_to_object, get_period_name
from app.pending.services import get_weeks_report, get_tasks_week
from json import dumps
from flask_login import current_user
from datetime import datetime


reportsbp = Blueprint('reports', __name__, template_folder='templates', url_prefix='/reports')



@reportsbp.route('/')
def index():
  employees = []
  if current_user.account_type.lower() == 'employee':
    profile = Employee(current_user.username)

    employee = get_employee_details(profile.employeeId)



    reports = get_employee_reports(profile.employeeId)

    for rp in reports:
      weeks = get_weeks_report(rp['id'])
      period = period_to_object(rp['period'])
      rp['periodName'] = get_period_name(period)
      rp['weeks'] = weeks
      for w in weeks:
        w['weekName'] = get_week_name(w)
        data = {
        'week': w['id'],
        'report': rp['id']
        }
        tasks = get_tasks_week(data)
        w['tasks'] = tasks

    employee['firstName'] = employee['firstName'].upper()
    employee['lastName'] = employee['lastName'].upper()
    employee['middleInitial'] = employee['middleInitial'].upper()
    employee['reports'] = reports
    employees.append(employee)
    data['employees'] = employees
    print(employee)

    return render_template('reports.html', data=data)

# chief account type

  elif  current_user.account_type.lower() == 'chief':

    profile = Chief(current_user.username)

    employees = get_chief_employees(profile.divisionId)

    for em in employees:
      reports = get_employee_reports(em['employeeId'])
      em['firstName'] = em['firstName'].upper()
      em['lastName'] = em['lastName'].upper()
      em['middleInitial'] = em['middleInitial'].upper()
      em['reports'] = reports
      for rp in reports:
        period = period_to_object(rp['period'])
        rp['periodName'] = get_period_name(period)
        weeks = get_weeks_report(rp['id'])
        rp['weeks'] = weeks
        for w in weeks:
          w['weekName'] = get_week_name(w)
          data = {
          'week': w['id'],
          'report': rp['id']
          }
          tasks = get_tasks_week(data)
          w['tasks'] = tasks

    data['employees'] = employees


    return render_template('reports.html', data=data)