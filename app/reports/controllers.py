from flask import Blueprint, render_template, request, url_for, make_response, redirect
from app.profile.models import Chief, Employee
from app.reports.services import *
from app.pending.controllers import get_week_name, period_to_object, get_period_name
from app.pending.services import get_weeks_report, get_tasks_week
from json import dumps
import pdfkit
from flask_login import current_user
from datetime import datetime
from os.path import join, dirname, realpath

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


@reportsbp.route('/print', methods=['POST'])
def printReport():

  reportId = request.form['reportId']
  css = ['pdf.css']

  report = get_report_details(reportId)
  chief = get_chief_details(report['divisionId'])

  report['firstName'] = report['firstName'].upper()
  report['lastName'] = report['lastName'].upper()
  report['middleInitial'] = report['middleInitial'].upper()


  chief['firstName'] = chief['firstName'].upper()
  chief['lastName'] = chief['lastName'].upper()
  chief['middleInitial'] = chief['middleInitial'].upper()

  payrollId = report['period'] + 1

  report['periodName'] = period_to_object(report['period'])
  report['payroll'] = period_to_object(payrollId)

  weeks = get_weeks_report(reportId)

  for w in weeks:
    w['weekName'] = get_week_name(w)
    data = {
      'week': w['id'],
      'report': reportId
    }
    tasks = get_tasks_week(data)
    w['taskCount'] = len(tasks)
    w['tasks'] = tasks

  report['weeks'] = weeks

  data['chief'] = chief
  data['report'] = report


  rendered = render_template('report_template.html', data=data)


  pdf = pdfkit.from_string(rendered, False, css=css)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = "attachment; filename=report.pdf"

  return response
