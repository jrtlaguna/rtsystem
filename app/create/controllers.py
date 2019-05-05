from flask import Blueprint, render_template, request, url_for
from datetime import datetime
from app.profile.models import Employee
from app.create.services import create_task, create_report, create_taskInstance, create_weeklyEntry
from flask_login import current_user
from json import dumps

createbp = Blueprint('create', __name__, template_folder='templates')


# profile = Employee(current_user.username)


# @createbp.route('create')
# def create():
#   return render_template('create.html')

@createbp.route('/')
def index():
  return render_template('create.html')

@createbp.route('/task_post', methods=['POST'])
def task_post():
  profile = None



  profile = Employee(current_user.username)
  data = request.get_json()



  taskData = {
    'taskDescription': data['name'],
    'isRecurring': bool(data['isRecurring']),
    'hasQuantity': bool(data['hasQuantity']),
    'accountId': profile.id,
    'employeePosition': profile.position_id
  }


  weekId = create_task(taskData)


  return 'task added.'


@createbp.route('/submit', methods=['POST'])
def submit():

  profile = None

  profile = Employee(current_user.username)

  taskDict = {}

  i = 0

  data = request.get_json()
  tasks = data['tasks']
  submitData = data['data']
  period = data['period']
  weeks = data['weeks']

# task/s insert to db
  for task in tasks:
    taskData = {
    'taskDescription': task['name'],
    'isRecurring': bool(task['isRecurring']),
    'hasQuantity': bool(task['hasQuantity']),
    'accountId': profile.id,
    'employeePosition': profile.position_id
    }

    taskId = create_task(taskData)
    taskDict[i] = taskId
    i+= 1


# report insert to db
  reportData = {
    'employeeId': profile.employeeId,
    'periodId': period
  }

  reportId = create_report(reportData)

  entryIds = {}

  weekInstance = []

  for week in submitData:
    weekInstance.append(week['week'])

  weekInstance = list(set(weekInstance))


# weekly entry insert to db
  for instance in weekInstance:
    weekPeriod = weeks[instance]['week'].replace(',', '').replace('-', '')
    weekPeriod = weekPeriod.split(" ")

    if(len(weekPeriod) == 3):
      startDate = weekPeriod[0] + ' ' + weekPeriod[1] + ' ' + weekPeriod[2]
      startDate = stringToDate(startDate)
      weekData = {
      'startDate': startDate,
      'endDate': startDate,
      'reportId': reportId
      }
      entryIds[instance] = create_weeklyEntry(weekData)
    elif(len(weekPeriod) == 5):
      weekPeriod.remove('')
      startDate = weekPeriod[0] + ' ' + weekPeriod [1] + ' ' + weekPeriod[3]
      endDate = weekPeriod[0] + ' ' + weekPeriod [2] + ' ' + weekPeriod[3]
      weekData = {
      'startDate': stringToDate(startDate),
      'endDate':  stringToDate(endDate),
      'reportId': reportId
      }
      entryIds[instance] = create_weeklyEntry(weekData)
    elif(len(weekPeriod) == 6):
      weekPeriod.remove('')
      startDate = weekPeriod[0] + ' ' + weekPeriod[1] + ' ' + weekPeriod[4]
      endDate = weekPeriod[2] + ' ' + weekPeriod[3] + ' ' + weekPeriod[4]
      weekData = {
      'startDate': stringToDate(startDate),
      'endDate':  stringToDate(endDate),
      'reportId': reportId
      }
      entryIds[instance] = create_weeklyEntry(weekData)

  for instance in submitData:
    instanceData = {
      'taskId': taskDict[instance['task_id']],
      'week': entryIds[instance['week']],
      'reportId': reportId
    }
    create_taskInstance(instanceData)

  return dumps({'redirect': url_for('index.create')})


def stringToDate(str):
  return datetime.strptime(str, '%B %d %Y').date()
