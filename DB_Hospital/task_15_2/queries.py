# queries.py

class HospitalQueries:
    """Класс с запросами из task_14_5_1.sql"""

    @staticmethod
    def get_all_queries():
        """Возвращает словарь со всеми запросами"""
        return {
            # EXISTS запросы
            "1.1 EXISTS: Врачи с обследованиями": """
                SELECT
                    d.Id,
                    d.Surname,
                    d.Name
                FROM Doctors d
                WHERE EXISTS (
                    SELECT 1
                    FROM DoctorsExaminations de
                    WHERE de.DoctorId = d.Id
                );
            """,

            "1.2 EXISTS: Отделения с палатами > 3 мест": """
                SELECT
                    d.Id,
                    d.Name AS DepartmentName,
                    d.Building
                FROM Departments d
                WHERE EXISTS (
                    SELECT 1
                    FROM Wards w
                    WHERE w.DepartmentId = d.Id AND w.Places > 3
                );
            """,

            # ANY запрос
            "2.1 ANY: Зарплата больше любого с премией > 5000": """
                SELECT
                    Surname,
                    Name,
                    Salary
                FROM Doctors
                WHERE Salary > ANY (
                    SELECT Salary
                    FROM Doctors
                    WHERE Premium > 5000
                );
            """,

            # SOME запрос
            "2.2 SOME: Палаты с местами больше некоторых из отделения 1": """
                SELECT
                    Name,
                    Places
                FROM Wards
                WHERE Places > SOME (
                    SELECT Places
                    FROM Wards
                    WHERE DepartmentId = 1
                );
            """,

            # ALL запрос
            "3 ALL: Зарплата больше всех врачей на 'С'": """
                SELECT
                    Surname,
                    Name,
                    Salary
                FROM Doctors
                WHERE Salary > ALL (
                    SELECT Salary
                    FROM Doctors
                    WHERE Surname LIKE 'С%'
                );
            """,

            # Комбинация ANY/SOME и ALL
            "4 Комбинация ANY и ALL": """
                SELECT
                    d.Surname,
                    d.Name,
                    d.Salary
                FROM Doctors d
                WHERE d.Salary > ANY (
                    SELECT Salary
                    FROM Doctors
                    WHERE Id IN (
                        SELECT DoctorId 
                        FROM DoctorsExaminations 
                        WHERE WardId IN (
                            SELECT Id 
                            FROM Wards 
                            WHERE DepartmentId = 1
                        )
                    )
                )
                AND d.Salary < ALL (
                    SELECT Salary
                    FROM Doctors
                    WHERE Id IN (
                        SELECT DoctorId 
                        FROM DoctorsExaminations 
                        WHERE WardId IN (
                            SELECT Id 
                            FROM Wards 
                            WHERE DepartmentId = 2
                        )
                    )
                );
            """,

            # UNION запрос
            "5 UNION: Отделения и палаты": """
                SELECT
                    Name AS Name,
                    'Department' AS Type
                FROM Departments
                UNION
                SELECT
                    Name AS Name,
                    'Ward' AS Type
                FROM Wards
                ORDER BY Type, Name;
            """,

            # UNION ALL запрос
            "6 UNION ALL: Врачи и спонсоры": """
                SELECT
                    Surname + ' ' + Name AS FullName,
                    'Doctor' AS Type
                FROM Doctors
                UNION ALL
                SELECT
                    Name AS FullName,
                    'Sponsor' AS Type
                FROM Sponsors;
            """,

            # INNER JOIN
            "7.1 INNER JOIN: Врачи и их обследования": """
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination,
                    de.StartTime,
                    de.EndTime,
                    w.Name AS Ward
                FROM DoctorsExaminations de
                INNER JOIN Doctors d ON de.DoctorId = d.Id
                INNER JOIN Examinations e ON de.ExaminationId = e.Id
                INNER JOIN Wards w ON de.WardId = w.Id
                ORDER BY d.Surname, de.StartTime;
            """,

            # LEFT JOIN
            "7.2 LEFT JOIN: Все врачи и их обследования": """
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination,
                    de.StartTime,
                    de.EndTime,
                    w.Name AS Ward
                FROM Doctors d
                LEFT JOIN DoctorsExaminations de ON d.Id = de.DoctorId
                LEFT JOIN Examinations e ON de.ExaminationId = e.Id
                LEFT JOIN Wards w ON de.WardId = w.Id
                ORDER BY d.Surname;
            """,

            # RIGHT JOIN
            "7.3 RIGHT JOIN: Все обследования и врачи": """
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination,
                    de.StartTime,
                    de.EndTime,
                    w.Name AS Ward
                FROM Doctors d
                RIGHT JOIN DoctorsExaminations de ON d.Id = de.DoctorId
                RIGHT JOIN Examinations e ON de.ExaminationId = e.Id
                LEFT JOIN Wards w ON de.WardId = w.Id
                ORDER BY e.Name;
            """,

            # LEFT + RIGHT (имитация FULL)
            "7.4 LEFT+RIGHT (FULL через UNION)": """
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination
                FROM Doctors d
                LEFT JOIN DoctorsExaminations de ON d.Id = de.DoctorId
                LEFT JOIN Examinations e ON de.ExaminationId = e.Id
                UNION
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination
                FROM Doctors d
                RIGHT JOIN DoctorsExaminations de ON d.Id = de.DoctorId
                RIGHT JOIN Examinations e ON de.ExaminationId = e.Id;
            """,

            # FULL JOIN
            "7.5 FULL JOIN: Все врачи и все обследования": """
                SELECT
                    d.Surname AS Doctor,
                    e.Name AS Examination
                FROM Doctors d
                FULL JOIN DoctorsExaminations de ON d.Id = de.DoctorId
                FULL JOIN Examinations e ON de.ExaminationId = e.Id
                ORDER BY Doctor, Examination;
            """
        }