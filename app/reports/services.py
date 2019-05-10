from app import get_db_connection


def get_employee_details(id):
  connection = get_db_connection()

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT e.id as employeeId, a.id as accountId, ep.positionTitle, sd.name, "
            "a.firstName, a.lastName, a.middleInitial from employee e INNER JOIN account a "
            "ON a.id = e.accountId INNER JOIN employeePosition ep ON e.employeePosition = ep.id "
            "INNER JOIN sectionDivision sd ON ep.sectionDivision "
            "WHERE e.id = %s"
        )

      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        employee = {
          'id': r[0],
          'accountId': r[1],
          'position': r[2],
          'division': r[3],
          'firstName': r[4],
          'lastName': r[5],
          'middleInitial': r[6]
        }

  finally:
    connection.close()

  return employee



def get_employee_reports(id):
  connection = get_db_connection()
  reports = []

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT id, attendancePeriod, status FROM report WHERE employeeId = %s")
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        report = {
          'id': r[0],
          'period': r[1],
          'status': r[2]
        }
        reports.append(report)

  finally:
    connection.close()

  return reports


def get_chief_employees(id):
  connection = get_db_connection()
  employees = []

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT e.id as employeeId, accountId, a.firstName as firstName, a.lastName as lastName, "
        "a.middleInitial as middleInitial, ep.positionTitle as position, sd.name as division "
        "FROM employee e INNER JOIN account a ON e.accountId = a.id INNER JOIN employeePosition ep on ep.id = e.employeePosition "
        "INNER JOIN sectionDivision sd ON sd.id = ep.sectionDivision WHERE ep.sectionDivision = %s"
        )
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        employee = {
          'employeeId': r[0],
          'id': r[1],
          'firstName': r[2],
          'lastName': r[3],
          'middleInitial': r[4],
          'position': r[5],
          'division': r[6]
        }
        employees.append(employee)

  finally:
    connection.close()

  return employees

def get_report_details(id):
  connection = get_db_connection()

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT a.firstName, a.middleInitial, a.lastName, r.attendancePeriod, sd.id "
          "FROM account a INNER JOIN employee e ON e.accountId = a.id INNER JOIN report r ON r.employeeId = e.id INNER JOIN employeePosition ep ON "
          "e.employeePosition = ep.id INNER JOIN sectionDivision sd ON ep.sectionDivision = sd.id "
          "WHERE r.id = %s"
        )
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        report = {
          'firstName': r[0],
          'middleInitial': r[1],
          'lastName': r[2],
          'period': r[3],
          'divisionId': r[4]
        }

  finally:
    connection.close()

  return report

def get_chief_details(id):
  connection = get_db_connection()

  try:
    with connection.cursor() as cursor:
      sql = ("SELECT a.firstName as firstName, a.lastName as lastName, a.middleInitial as middileInitial "
          "FROM chief c INNER JOIN account a ON a.id = c.accountId WHERE c.sectionDivision = %s"
        )
      cursor.execute(sql, (id))
      result = cursor.fetchall()
      for r in result:
        chief = {
          'firstName': r[0],
          'lastName': r[1],
          'middleInitial': r[2]
        }

  finally:
    connection.close()

  return chief


