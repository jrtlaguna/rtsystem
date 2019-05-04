from app import get_db_connection

def get_position_list():
    connection = get_db_connection()
    positions = []
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT positionTitle FROM employeePosition')
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                positions.append(r[0])

    finally:
        connection.close()

    return positions


def get_section_division_list():
    connection = get_db_connection()
    section_divisions = []
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT name FROM sectionDivision')
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                section_divisions.append(r[0])

    finally:
        connection.close()

    return section_divisions


def create_position(data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = ('INSERT INTO employeePosition(positionTitle, sectionDivision'
                ') VALUES(%s, (SELECT id FROM sectionDivision WHERE name=%s)'
                ')'
            )
            cursor.execute(sql, (data['title'], data['section_division']))
            connection.commit()

    finally:
        connection.close()


def create_section_division(data):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = ('INSERT INTO sectionDivision(name, verifier'
                ') VALUES(%s, (SELECT id FROM account WHERE username=%s)'
                ')'
            )
            cursor.execute(sql, (data['name'], data['verifier']))
            connection.commit()

    finally:
        connection.close()


def get_section_divisions_and_positions():
    data = []

    connection = get_db_connection()
    try:
        section_divisions = []
        with connection.cursor() as cursor:
            sql = 'SELECT id, name FROM sectionDivision'
            cursor.execute(sql)
            
            result = cursor.fetchall()
            for r in result:
                sd = {
                    'id': r[0],
                    'name': r[1]
                }
                section_divisions.append(sd)

        positions = {}
        with connection.cursor() as cursor:
            sql = 'SELECT positionTitle, sectionDivision FROM employeePosition'
            cursor.execute(sql)

            result = cursor.fetchall()
            for r in result:
                p = r[0]
                sd = r[1]
                
                pos = {
                    'title': p,
                    'id': '-'.join(p.split())
                }
                if sd in positions.keys():
                    
                    positions[sd].append(pos)

                else:
                    positions[sd] = [pos]
        
        for sd in section_divisions:
            d = {
                'name': sd['name'],
                'positions': positions[sd['id']] if sd['id'] in positions.keys() else [],
                'id_prepend': '-'.join(sd['name'].split())
            }

            data.append(d)
            
    finally:
        connection.close()

    return data


def get_verifier(sec_div):
    verifier = None

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT username '
                'FROM account '
                'WHERE id=('
                'SELECT verifier from sectionDivision WHERE name=%s'
                ')'
            )
            cursor.execute(sql, sec_div)

            result = cursor.fetchone()
            if result:
                verifier = result[0]

    finally:
        connection.close()

    return verifier


def delete_secdiv_positions(sec_div):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = ('DELETE FROM employeePosition WHERE sectionDivision = '
                '(SELECT id FROM sectionDivision WHERE name=%s)'
            )
            cursor.execute(sql, sec_div)
            connection.commit()

    finally:
        connection.close()


def delete_secdiv_record(sec_div):
    nullify_secdivs_in_admin_accounts(sec_div)
    nullify_secdivs_in_chief_accounts(sec_div)
    nullify_positions_in_employee_accounts(sec_div=sec_div)
    delete_secdiv_positions(sec_div)

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM sectionDivision WHERE name=%s'
            cursor.execute(sql, sec_div)
            connection.commit()

    finally:
        connection.close()


def delete_position_record(sec_div, pos):
    nullify_positions_in_employee_accounts(sec_div, pos)

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM employeePosition WHERE positionTitle = %s'
            cursor.execute(sql, pos)
            connection.commit()

    finally:
        connection.close()


def update_secdiv_record(current, new, verifier):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                'UPDATE sectionDivision SET name = %s, '
                'verifier = (SELECT id FROM account WHERE username = %s) '
                'WHERE name = %s'
            )
            cursor.execute(sql, (new, verifier, current))
            connection.commit()

    finally:
        connection.close()


def update_position_record(current, new, secdiv):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                'UPDATE employeePosition SET positionTitle = %s, '
                'sectionDivision = (SELECT id FROM sectionDivision WHERE name = %s) '
                'WHERE positionTitle = %s'
            )
            cursor.execute(sql, (new, secdiv, current))
            connection.commit()

    finally:
        connection.close()


def check_position_duplicate(pos, secdiv):
    duplicate = False

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                'SELECT id FROM employeePosition WHERE positionTitle = %s '
                'AND sectionDivision = (SELECT id FROM sectionDivision WHERE name = %s)'
            )
            cursor.execute(sql, (pos, secdiv))
            result = cursor.fetchone()

            if result:
                duplicate = True

    finally:
        connection.close()

    return duplicate


def nullify_positions_in_employee_accounts(sec_div = None, pos = None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if pos:
                sql = (
                    'UPDATE employee SET employeePosition = %s '
                    'WHERE employeePosition = ('
                        'SELECT id FROM employeePosition '
                        'WHERE positionTitle = %s AND sectionDivision = ('
                            'SELECT id FROM sectionDivision WHERE name = %s'
                        ')'
                    ')'
                )
                cursor.execute(sql, (None, pos, sec_div))
                
            else:
                sql = (
                    'UPDATE employee SET employeePosition = %s '
                    'WHERE employeePosition IN ('
                    'SELECT id FROM employeePosition WHERE sectionDivision = '
                    '(SELECT id FROM sectionDivision WHERE name=%s)'
                    ')'
                )
                cursor.execute(sql, (None, sec_div))
            connection.commit()

    finally:
        connection.close()


def nullify_secdivs_in_chief_accounts(sec_div):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                'UPDATE chief SET sectionDivision = %s '
                'WHERE sectionDivision = ('
                'SELECT id FROM sectionDivision WHERE name = %s'
                ')'
            )
            cursor.execute(sql, (None, sec_div))
            connection.commit()

    finally:
        connection.close()


def nullify_secdivs_in_admin_accounts(sec_div):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                'UPDATE admin SET sectionDivision = %s '
                'WHERE sectionDivision = ('
                'SELECT id FROM sectionDivision WHERE name = %s'
                ')'
            )
            cursor.execute(sql, (None, sec_div))
            connection.commit()

    finally:
        connection.close()