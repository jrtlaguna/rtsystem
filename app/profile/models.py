from app import get_db_connection

class Profile(object):
    def __init__(self, username=None):
        self.id = None
        self.username = username
        self.password = None
        self.first_name = None
        self.middle_initial = None
        self.last_name = None
        self.account_type = None

        self.__load_profile()


    def __load_profile(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = ('SELECT '
                    'id, username, password, '
                    'firstName, middleInitial, lastName, '
                    'accountType '
                    'FROM account '
                    'WHERE username=%s'
                )
                cursor.execute(sql, self.username)

                results = cursor.fetchone()
                if results:
                    self.id, self.username, self.password, self.first_name, self.middle_initial, self.last_name, self.account_type = results

        finally:
            connection.close()


class Employee(Profile):
    def __init__(self, username):
        Profile.__init__(self, username)
        self.position = None
        self.contact_number = None
        self.is_working_sunday = False
        self.is_working_monday = False
        self.is_working_tuesday = False
        self.is_working_wednesday = False
        self.is_working_thursday = False
        self.is_working_friday = False
        self.is_working_saturday = False
        self.section_division = None
        self.employeeId = None

        self.__load_details()


    def __load_details(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = ('SELECT '
                    'p.positionTitle, e.contactNumber, '
                    'e.isWorkingSunday, e.isWorkingMonday, e.isWorkingTuesday, e.isWorkingWednesday, '
                    'e.isWorkingThursday, e.isWorkingFriday, e.isWorkingSaturday, sd.name, e.employeePosition, e.id '
                    'FROM employee e '
                    'INNER JOIN employeePosition p '
                    'ON e.employeePosition = p.id '
                    'INNER JOIN sectionDivision sd '
                    'ON p.sectionDivision = sd.id '
                    'WHERE e.accountId=%s'
                )
                cursor.execute(sql, self.id)

                result = cursor.fetchone()
                if result:
                    self.position = result[0]
                    self.contact_number = result[1]
                    self.is_working_sunday = result[2]
                    self.is_working_monday = result[3]
                    self.is_working_tuesday = result[4]
                    self.is_working_wednesday = result[5]
                    self.is_working_thursday = result[6]
                    self.is_working_friday = result[7]
                    self.is_working_saturday = result[8]
                    self.section_division = result[9]
                    self.position_id = result[10]
                    self.employeeId = result[11]

        finally:
            connection.close()


class Chief(Profile):
    def __init__(self, username):
        Profile.__init__(self, username)
        self.section_division = None
        self.divisionId = None

        self.__load_details()


    def __load_details(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = ('SELECT sd.name, c.sectionDivision '
                    'FROM chief c '
                    'INNER JOIN sectionDivision sd '
                    'ON c.sectionDivision = sd.id '
                    'WHERE c.accountId=%s'
                )
                cursor.execute(sql, self.id)

                result = cursor.fetchone()
                if result:
                    self.section_division = result[0]
                    self.divisionId = result[1]

        finally:
            connection.close()


class Admin(Profile):
    def __init__(self, username):
        Profile.__init__(self, username)
        self.section_division = None

        self.__load_details()


    def __load_details(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = ('SELECT sd.name '
                    'FROM admin a '
                    'INNER JOIN sectionDivision sd '
                    'ON a.sectionDivision = sd.id '
                    'WHERE a.accountId=%s'
                )
                cursor.execute(sql, self.id)

                result = cursor.fetchone()
                if result:
                    self.section_division = result[0]

        finally:
            connection.close()