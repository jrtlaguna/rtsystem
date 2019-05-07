from app import get_db_connection

def get_divisions(id):
  connection = get_db_connection()
  divisions = []

  try:
    with connection.cursor() as cursor:
      sql = ('SELECT * FROM sectionDivision where id = %s')
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        division = {
          'id': r[0],
          'name': r[1],
          'verfier': r[2]
        }
        divisions.append(division)

  finally:
    connection.close()
  return divisions

def get_all_divisions():
  connection = get_db_connection()
  divisions = []
  try:
    with connection.cursor() as cursor:
      sql = ('SELECT * from sectionDivision')
      cursor.execute(sql)
      result = cursor.fetchall()
      for r in result:
        division = {
          'id': r[0],
          'name': r[1]
        }
        divisions.append(division)

  finally:
    connection.close()
  return divisions



def get_positions(division):
  connection = get_db_connection()
  positions = []
  try:
    with connection.cursor() as cursor:
      sql = ('SELECT * from employeePosition where sectionDivision = %s')
      cursor.execute(sql, (division))
      result = cursor.fetchall()
      for r in result:
        position = {
          'id': r[0],
          'title': r[1]
        }
        positions.append(position)

  finally:
    connection.close()

  return positions


def get_employees_position(position):
  connection = get_db_connection()
  employees = []
  try:
    with connection.cursor() as cursor:
      sql = ('SELECT * from employee where employeePosition = %s')
      cursor.execute(sql, (position))
      result = cursor.fetchall()
      for r in result:
        employee = {
          'id': r[0],
          'accountId': r[1]
        }
        employees.append(employee)

  finally:
    connection.close()

  return employees

def get_attendance_period(id):
  try:
    connection = get_db_connection()
    with connection.cursor() as cursor:
      sql = ('SELECT * FROM attendancePeriod where id = %s')
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        period = {
          'id': r[0],
          'monthStart': r[1],
          'dayStart': r[2],
          'monthEnd': r[3],
          'dayEnd': r[4]
        }


  finally:
    connection.close()

  return period


def get_employee_reports(employeeId):
  connection = get_db_connection()
  reports = []

  try:
    with connection.cursor() as cursor:
      sql = ('SELECT id, attendancePeriod from report where employeeId = %s AND status="PENDING"')
      cursor.execute(sql, (employeeId))
      result = cursor.fetchall()
      for r in result:
        report = {
          'reportId': r[0],
          'period': r[1]
        }
        reports.append(report)

  finally:
    connection.close()
  return reports


def get_employees_period(data):
  connection = get_db_connection()
  employees = []

  try:
    with connection.cursor() as cursor:
      sql = ('SELECT e.id as employeeId, a.firstName as firstName, a.lastName as lastName, '
        'a.middleInitial as middleInitial, r.id as reportId, e.employeePosition as position '
        'FROM employee e INNER JOIN account a ON e.accountId = a.id '
        'INNER JOIN report r ON r.employeeId = e.id '
        'INNER JOIN employeePosition ep ON ep.id = e.employeePosition '
        'WHERE r.attendancePeriod = %s AND ep.id = %s'
        )
      cursor.execute(sql, (data['period'], data['position']))
      result = cursor.fetchall()
      for r in result:
        employee = {
          'employeeId': r[0],
          'firstName': r[1],
          'lastName': r[2],
          'middleInitial': r[3],
          'reportId': r[4]
        }
        employees.append(employee)

  finally:
    connection.close()
  return employees

def get_reports_employee(data):
  connection = get_db_connection()
  reports = []

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT id, status, attendancePeriod FROM report "
        "WHERE employeeId = %s AND attendancePeriod = %s AND status = 'PENDING' "
        )
      cursor.execute(sql, (data['employee'], data['period']))
      result = cursor.fetchall()
      for r in result:
        report = {
          'id': r[0],
          'status': r[1],
          'period': r[2]
        }
        reports.append(report)
  finally:
    connection.close()
  return reports


def get_weeks_report(id):
  connection = get_db_connection()
  weeks = []

  try:
    with connection.cursor() as cursor:
      sql = ('SELECT * from weeklyEntry where reportId = %s')
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        week = {
          'id': r[0],
          'dateStart': r[1],
          'dateEnd': r[2]
        }
        weeks.append(week)
  finally:
    connection.close()

  return weeks


def get_tasks_week(data):
  connection = get_db_connection()
  tasks = []

  try:
    with connection.cursor() as cursor:
      sql = ('SELECT t.id as taskId, t.taskDescription as description '
          'FROM taskInstance ti INNER JOIN task t ON ti.taskId = t.id '
          'WHERE ti.reportId = %s AND ti.weekId = %s'
        )
      cursor.execute(sql, (data['report'], data['week']))
      result = cursor.fetchall()
      for r in result:
        task = {
          'id': r[0],
          'description': r[1]
        }
        tasks.append(task)

  finally:
    connection.close()

  return tasks

def approve_report(id):
  connection = get_db_connection()

  try:
    with connection.cursor() as cursor:
      sql = ("UPDATE report SET status = 'APPROVED' where id = %s ")
      result = cursor.execute(sql, (id))

    connection.commit()
  finally:
    connection.close()

  return result


# get all positions where sd = division
#   for po in positions:
#     get all employees with this position
#     get all reports with this employee
#     for r in reports:
#       periods.append(r['period'])
#     periods = list(set(periods))
#     for pr in periods:
#       get employees with reports where period = pr['id'] position = e.employeePosition = po['id']
#       for em in employees:
#         get reports where report has em['id'] & attendancePeriod = pr['id']
#         for rp in reports:
#           get weeks where reportid = rp['id']
#           for wk in weeks:
#             get taskInstance where weekId = wk['id'] & reportid = rp['id']
#             for ti in taskInstance:
#               get tasks description where ti tasks = [ti['taskId']]



