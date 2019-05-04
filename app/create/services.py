from app import get_db_connection
from datetime import datetime


def create_task(data):
  connection = get_db_connection()
  try:
    with connection.cursor() as cursor:
      sql = ('INSERT INTO task(taskDescription, isRecurring, hasQuantity, employeePosition, accountId)'
              'VALUES(%s, %s, %s, %s, %s)'
        )
      cursor.execute(sql, (data['taskDescription'], data['isRecurring'], data['hasQuantity'], data['employeePosition'], data['accountId']))
      taskId = connection.insert_id()
      connection.commit()


  finally:

    connection.close()
  return taskId



def create_report(data):
  connection = get_db_connection()
  now = datetime.now()
  try:
    with connection.cursor() as cursor:
      sql = ('INSERT INTO report(status, year, employeeId, attendancePeriod) '
        'VALUES(%s, %s, %s, %s)'
        )
      cursor.execute(sql, ("PENDING",now.year, data['employeeId'], data['periodId']))
      reportId = connection.insert_id()
      connection.commit()

  finally:
    connection.close()

  return reportId


def create_taskInstance(data):
  connection = get_db_connection()
  try:
    with connection.cursor() as cursor:
      sql = ('INSERT INTO taskInstance(taskId, weekId, reportId)'
          'VALUES(%s, %s, %s)'
        )
      cursor.execute(sql, (data['taskId'], data['week'], data['reportId']))
      connection.commit()

  finally:
    connection.close()

  return 'success'


def create_weeklyEntry(data):
  connection = get_db_connection()
  try:
    with connection.cursor() as cursor:
      sql = ('INSERT INTO weeklyEntry(dateStart_week, dateFinish_week, reportId) '
        'VALUES(%s, %s, %s)'
        )
      cursor.execute(sql, (data['startDate'], data['endDate'], data['reportId']))
      weekId = connection.insert_id()
      connection.commit()

  finally:
    connection.close()

  return weekId
