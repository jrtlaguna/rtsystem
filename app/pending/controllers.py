from flask import Blueprint, render_template, request, url_for
from app.profile.models import Admin, Chief
from app.pending.services import *
from flask_login import current_user
from datetime import datetime
import calendar



pendingbp = Blueprint('pending', __name__, template_folder='templates', url_prefix='/pending')
now = datetime.now()
year = now.year

@pendingbp.route('/')
def index():
  if current_user.account_type.lower() == 'chief':
    profile = Chief(current_user.username)
    division = (profile.divisionId)


    positionArray = []

    positions = get_positions(division)

    for po in positions:
      periodIndex = []
      periods = []
      employees = get_employees_position(po['id'])
      for em in employees:
        reports = get_employee_reports(em['id'])
        for r in reports:
          periodIndex.append(r['period'])
      periodIndex = list(set(periodIndex))
      for p in periodIndex:
        period = period_to_object(p)
        periods.append(period)
      po['periods'] = periods
      for pr in periods:
        data = {
          'period': pr['id'],
          'position': po['id']
        }
        employees = get_employees_period(data)
        # pr['employees'] = employees
        pr['employees'] = employees
        for em in employees:
          data = {
            'employee': em['employeeId'],
            'period': pr['id']
          }
          em['firstName'] = em['firstName'].upper()
          em['lastName'] = em['lastName'].upper()
          reports =  get_reports_employee(data)
          em['reports'] = reports
          for rp in reports:
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

  print(positions)
  return render_template('pending.html', data=positions, division=division)








def period_to_object(id):

  period = get_attendance_period(id)

  period['name'] = get_period_name(period)



  return period

def get_period_name(period):
  month1 = calendar.month_name[period['monthStart']]
  month2 = calendar.month_name[period['monthEnd']]
  day1 = str(period['dayStart'])
  day2 = str(period['dayEnd'])
  currentYear = str(year)

  date1 = month1 + " " + day1 + ", " + currentYear
  date2 = month2 + " " + day2  + ", " + currentYear

  name = date1 + ' - ' + date2
  return name

def get_week_name(w):
  date1 = datetime.strftime(w['dateStart'], '%B %d, %Y - ')
  date2 = datetime.strftime(w['dateEnd'], '%B %d, %Y')
  return date1 + date2