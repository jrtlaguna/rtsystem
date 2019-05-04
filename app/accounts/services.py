from app import get_db_connection
from werkzeug.security import generate_password_hash

def create_account(data):
    create_function_list = {
        'admin': __create_admin_account,
        'chief': __create_chief_account,
        'employee': __create_employee_account
        
    }

    create_function = create_function_list[data['account_type'].lower()]
    return create_function(data)


def get_verifiers():
    verifiers = []

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT username, firstName, lastName, middleInitial FROM account '
                'WHERE accountType = %s OR accountType = %s ORDER BY lastName'
            )
            cursor.execute(sql, ('Admin', 'Chief'))

            result = cursor.fetchall()
            for r in result:
                account = {
                    'username': r[0],
                    'first_name': r[1],
                    'last_name': r[2],
                    'middle_initial': r[3] 
                }

                verifiers.append(account)

    finally:
        connection.close()

    return verifiers
            

def __create_admin_account(data):
    status = None

    exists = __check_username(data['username'])
    if exists:
        status = 'User already exists.'
        return status

    account_id = __create_base_account(data)
    if not account_id:
        status = 'Account Creation Failed!'
        return status

    connection = get_db_connection()
    try:
        admin_id = None
        with connection.cursor() as cursor:
            sql = ('INSERT INTO admin('
                'accountId, sectionDivision'
                ') VALUES(%s, (SELECT id FROM sectionDivision WHERE name=%s)'
                ')'
            )
            cursor.execute(sql, (account_id, data['section_division']))
            admin_id = cursor.lastrowid

        if admin_id:
            status = 'Successfully created Admin account!'
            connection.commit()
        else:
            status = 'Failed to create Admin account.'

    finally:
        connection.close()

    return status


def __create_chief_account(data):
    status = None

    exists = __check_username(data['username'])
    if exists:
        status = 'User already exists.'
        return status

    account_id = __create_base_account(data)
    if not account_id:
        status = 'Failed to create acount.'
        return status

    connection = get_db_connection()
    try:
        chief_id = None
        with connection.cursor() as cursor:
            sql = ('INSERT INTO chief('
                'accountId, sectionDivision'
                ') VALUES(%s, (SELECT id FROM sectionDivision WHERE name=%s)'
                ')'
            )
            cursor.execute(sql, (account_id, data['section_division']))
            chief_id = cursor.lastrowid

        if chief_id:
            status = 'Successfully created Chief account!'
            connection.commit()
        else:
            status = 'Failed to create Chief account.'

    finally:
        connection.close()

    return status


def __create_employee_account(data):
    status = None

    exists = __check_username(data['username'])
    if exists:
        status = 'User already exists.'
        return status

    account_id = __create_base_account(data)
    if not account_id:
        status = 'Failed to create account.'
        return status

    connection = get_db_connection()
    try:
        employee_id = None
        with connection.cursor() as cursor:
            sql = ('INSERT INTO employee('
                'accountId, employeePosition, contactNumber, '
                'isWorkingSunday, isWorkingMonday, isWorkingTuesday, isWorkingWednesday, '
                'isWorkingThursday, isWorkingFriday, isWorkingSaturday'
                ')VALUES('
                '%s, (SELECT id FROM employeePosition WHERE positionTitle=%s), %s, '
                '%s, %s, %s, %s, '
                '%s, %s, %s'
                ')'
            )
            cursor.execute(sql, (
                    account_id, data['position'], data['contact_number'],
                    data['is_working_sun'], data['is_working_mon'], data['is_working_tue'], data['is_working_wed'],
                    data['is_working_thu'], data['is_working_fri'], data['is_working_sat']
                )
            )
            employee_id = cursor.lastrowid
        
        if employee_id:
            status = 'Successfully created Employee account!'
            connection.commit()
        else:
            status = 'Failed to create Employee account.'

    finally:
        connection.close()

    return status



def __check_username(username):
    exists = False

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT username FROM account WHERE username=%s'
            cursor.execute(sql, username)

            result = cursor.fetchone()

            if result:
                exists = True

    finally:
        connection.close()

    return exists


def __create_base_account(data):
    account_id = None

    connection = get_db_connection()
    try:
        password_hash = generate_password_hash(data['password'])

        account_id = None
        with connection.cursor() as cursor:
            sql = ('INSERT INTO account('
                'username, password, '
                'firstName, middleInitial, lastName, '
                'isActive, accountType'
                ') VALUES(%s, %s, %s, %s, %s, %s, %s)'
            )
            cursor.execute(sql, (
                data['username'], password_hash,
                data['first_name'], data['middle_initial'], data['last_name'],
                data['active'], data['account_type']
                )
            )

            account_id = cursor.lastrowid

            if account_id:
                connection.commit()

    finally:
        connection.close()

    return account_id