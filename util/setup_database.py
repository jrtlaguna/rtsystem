import pymysql
from getpass import getpass
from werkzeug.security import generate_password_hash

def setup_db():
    connection = connect()
    create_database(connection)
    create_tables(connection)
    insert_atttendancePeriod_defaultValues(connection)
    create_dummy_data(connection)
    connection.close()


def connect():
    localhost = 'localhost'
    username = 'root'
    password = getpass(prompt='root password: ')

    return pymysql.connect(localhost, username, password)


def create_database(connection):
    try:
        with connection.cursor() as cursor:
            sql = 'DROP DATABASE IF EXISTS rt_system_db'
            cursor.execute(sql)

        with connection.cursor() as cursor:
            sql = 'CREATE DATABASE rt_system_db'
            cursor.execute(sql)

        with connection.cursor() as cursor:
            sql = 'USE rt_system_db'
            cursor.execute(sql)

    finally:
        connection.commit()


def create_tables(connection):
    create_account_table(connection)
    create_sectionDivision_table(connection)
    create_position_table(connection)
    create_employee_table(connection)
    create_chief_table(connection)
    create_admin_table(connection)
    create_task_table(connection)
    create_attendancePeriod_table(connection)
    create_report_table(connection)
    create_attendance_table(connection)
    create_weeklyEntry_table(connection)
    create_taskInstance_table(connection)
    create_changeLog_table(connection)


def create_account_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE account('
                'id int NOT NULL AUTO_INCREMENT, '
                'username VARCHAR(32) NOT NULL, '
                'password VARCHAR(255) NOT NULL, '
                'firstName VARCHAR(64) NOT NULL, '
                'middleInitial VARCHAR(8) NOT NULL, '
                'lastName VARCHAR(64) NOT NULL, '
                'isActive BOOLEAN NOT NULL, '
                'accountType VARCHAR(16) NOT NULL, '
                'PRIMARY KEY (id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_sectionDivision_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE sectionDivision('
                'id int NOT NULL AUTO_INCREMENT, '
                'name VARCHAR(64) NOT NULL, '
                'verifier int, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (verifier) REFERENCES account(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_position_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE employeePosition('
                'id int NOT NULL AUTO_INCREMENT, '
                'positionTitle VARCHAR(64) NOT NULL, '
                'sectionDivision int NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (sectionDivision) REFERENCES sectionDivision(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_employee_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE employee('
                'id int NOT NULL AUTO_INCREMENT, '
                'accountId int NOT NULL, '
                'employeePosition int, '
                'contactNumber VARCHAR(16) NOT NULL, '
                'isWorkingSunday BOOLEAN, '
                'isWorkingMonday BOOLEAN, '
                'isWorkingTuesday BOOLEAN, '
                'isWorkingWednesday BOOLEAN, '
                'isWorkingThursday BOOLEAN, '
                'isWorkingFriday BOOLEAN, '
                'isWorkingSaturday BOOLEAN, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (accountId) REFERENCES account(id), '
                'FOREIGN KEY (employeePosition) REFERENCES employeePosition(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_chief_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE chief('
                'id int NOT NULL AUTO_INCREMENT, '
                'accountId int NOT NULL, '
                'sectionDivision int, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (accountId) REFERENCES account(id), '
                'FOREIGN KEY (sectionDivision) REFERENCES sectionDivision(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_admin_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE admin('
                'id int NOT NULL AUTO_INCREMENT, '
                'accountId int NOT NULL, '
                'sectionDivision int, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (accountId) REFERENCES account(id), '
                'FOREIGN KEY (sectionDivision) REFERENCES sectionDivision(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_task_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE task('
                'id int NOT NULL AUTO_INCREMENT, '
                'taskDescription VARCHAR(255) NOT NULL, '
                'isRecurring BOOLEAN, '
                'hasQuantity BOOLEAN, '
                'employeePosition int NOT NULL, '
                'accountId int NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (employeePosition) REFERENCES employeePosition(id), '
                'FOREIGN KEY (accountId) REFERENCES account(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_attendancePeriod_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE attendancePeriod('
                'id int NOT NULL AUTO_INCREMENT, '
                'dateStart_month INT NOT NULL, '
                'dateStart_day INT NOT NULL, '
                'dateFinish_month INT NOT NULL, '
                'dateFinish_day INT NOT NULL, '
                'PRIMARY KEY (id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_report_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = (
                'CREATE TABLE report('
                'id INT NOT NULL AUTO_INCREMENT, '
                'status VARCHAR(32) NOT NULL, '
                'year INT NOT NULL, '
                'employeeId INT NOT NULL, '
                'attendancePeriod INT NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (employeeId) REFERENCES employee(id), '
                'FOREIGN KEY (attendancePeriod) REFERENCES attendancePeriod(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_attendance_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE attendance('
                'id int NOT NULL AUTO_INCREMENT, '
                'date DATE NOT NULL, '
                'reason VARCHAR(128) NOT NULL, '
                'reportId int NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (reportId) REFERENCES report(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_weeklyEntry_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE weeklyEntry('
                'id int NOT NULL AUTO_INCREMENT, '
                'dateStart_week DATE NOT NULL, '
                'dateFinish_week DATE NOT NULL, '
                'reportId int NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (reportId) REFERENCES report(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_taskInstance_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE taskInstance('
                'id int NOT NULL AUTO_INCREMENT, '
                'taskId int NOT NULL, '
                'weekId int NOT NULL, '
                'quantity int NOT NULL DEFAULT 1,'
                'reportId int NOT NULL,'
                'isAccomplished BOOLEAN, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (taskId) REFERENCES task(id), '
                'FOREIGN KEY (weekId) REFERENCES weeklyEntry(id),'
                'FOREIGN KEY (reportId) REFERENCES report(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def create_changeLog_table(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('CREATE TABLE changeLog('
                'id int NOT NULL AUTO_INCREMENT, '
                'timestamp TIMESTAMP NOT NULL, '
                'description VARCHAR(255) NOT NULL, '
                'accountId int NOT NULL, '
                'PRIMARY KEY (id), '
                'FOREIGN KEY (accountId) REFERENCES account(id)'
                ')'
            )
            cursor.execute(sql)

    finally:
        connection.commit()


def insert_atttendancePeriod_defaultValues(connection):
    try:
        with connection.cursor() as cursor:
            sql = (
                'INSERT INTO attendancePeriod('
                'dateStart_month, dateStart_day, '
                'dateFinish_month, dateFinish_day '
                ') VALUES(%s, %s, %s, %s)'
            )
            cursor.execute(sql, (1,26,2,25))
            cursor.execute(sql, (2,26,3,25))
            cursor.execute(sql, (3,26,4,25))
            cursor.execute(sql, (4,26,5,25))
            cursor.execute(sql, (5,26,6,25))
            cursor.execute(sql, (6,26,7,25))
            cursor.execute(sql, (7,26,8,25))
            cursor.execute(sql, (8,26,9,25))
            cursor.execute(sql, (9,26,10,25))
            cursor.execute(sql, (10,26,11,25))
            cursor.execute(sql, (11,26,12,25))
            cursor.execute(sql, (12,26,1,25))

    finally:
        connection.commit()


def create_dummy_data(connection):
    try:
        with connection.cursor() as cursor:
            sql = ('INSERT INTO account('
                'username, '
                'password, '
                'firstName, '
                'middleInitial, '
                'lastName, '
                'isActive, '
                'accountType'
                ') '
                'VALUES(%s, %s, %s, %s, %s, %s, %s)'
            )
            cursor.execute(sql, ('admin', generate_password_hash('admin'),
                'Admin', 'A', 'Admin',
                True, 'Admin'))
            cursor.execute(sql, ('employeeone', generate_password_hash('employeeone'),
                'Em', 'P', 'Loyee',
                True, 'Employee'))

            connection.commit()

        with connection.cursor() as cursor:
            sql = ('INSERT INTO sectionDivision(name, verifier) VALUES(%s, %s)')
            cursor.execute(sql, ('Administrative Division', 1))
            cursor.execute(sql, ('HR Division', 2))

            connection.commit()

        with connection.cursor() as cursor:
            sql = ('INSERT INTO employeePosition(positionTitle, sectionDivision) VALUES(%s, %s)')
            cursor.execute(sql, ('Secretary', 2))

            connection.commit()

        with connection.cursor() as cursor:
            sql = ('INSERT INTO employee('
                'accountId,'
                'employeePosition, '
                'contactNumber, '
                'isWorkingSunday, '
                'isWorkingMonday, '
                'isWorkingTuesday, '
                'isWorkingWednesday, '
                'isWorkingThursday, '
                'isWorkingFriday, '
                'isWorkingSaturday'
                ') VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )
            cursor.execute(sql, (2, 1, '+639171234567', False, True, True, True, True, True, False))

            connection.commit()

        with connection.cursor() as cursor:
            sql = ('INSERT INTO admin(accountId, sectionDivision) VALUES(%s, %s)')
            cursor.execute(sql, (1, 1))

    finally:
        connection.commit()


setup_db()