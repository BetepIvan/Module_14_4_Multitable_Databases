-- =====================================================
-- 1. Два запроса с EXISTS
-- =====================================================

-- 1.1. Врачи, у которых есть хотя бы одно обследование
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

-- 1.2. Отделения, в которых есть палаты с количеством мест > 3
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

-- =====================================================
-- 2. ANY и SOME (разные запросы)
-- =====================================================

-- 2.1. ANY: Врачи, у которых зарплата больше зарплаты любого врача с премией > 5000
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

-- 2.2. SOME: Палаты, количество мест в которых больше, чем в некоторых палатах отделения 1
SELECT
    Name,
    Places
FROM Wards
WHERE Places > SOME (
    SELECT Places
    FROM Wards
    WHERE DepartmentId = 1
);

-- =====================================================
-- 3. Один запрос с ALL
-- =====================================================

-- Врачи, у которых зарплата больше зарплаты ВСЕХ врачей с фамилией, начинающейся на 'С'
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

-- =====================================================
-- 4. Сочетание ANY/SOME и ALL
-- =====================================================

-- Врачи, у которых зарплата больше, чем у любого врача из отделения 1,
-- но меньше, чем у всех врачей из отделения 2
SELECT
    d.Surname,
    d.Name,
    d.Salary
FROM Doctors d
WHERE d.Salary > ANY (
    SELECT Salary
    FROM Doctors
    WHERE Id IN (SELECT DoctorId FROM DoctorsExaminations WHERE WardId IN (SELECT Id FROM Wards WHERE DepartmentId = 1))
)
AND d.Salary < ALL (
    SELECT Salary
    FROM Doctors
    WHERE Id IN (SELECT DoctorId FROM DoctorsExaminations WHERE WardId IN (SELECT Id FROM Wards WHERE DepartmentId = 2))
);

-- =====================================================
-- 5. UNION
-- =====================================================

-- Все уникальные названия отделений и названия палат
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

-- =====================================================
-- 6. UNION ALL
-- =====================================================

-- Все врачи и все спонсоры (с дубликатами, если есть одинаковые имена)
SELECT
    Surname + ' ' + Name AS FullName,
    'Doctor' AS Type
FROM Doctors
UNION ALL
SELECT
    Name AS FullName,
    'Sponsor' AS Type
FROM Sponsors;

-- =====================================================
-- 7. Пять запросов на все типы JOIN
-- =====================================================

-- 7.1. INNER JOIN: Врачи и их обследования (только те, у кого есть обследования)
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

-- 7.2. LEFT JOIN: Все врачи и их обследования (включая врачей без обследований)
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

-- 7.3. RIGHT JOIN: Все обследования и врачи, которые их проводят (включая обследования без врачей)
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

-- 7.4. LEFT + RIGHT (имитация FULL через UNION)
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

-- 7.5. FULL JOIN: Все врачи и все обследования (полное объединение)
SELECT
    d.Surname AS Doctor,
    e.Name AS Examination
FROM Doctors d
FULL JOIN DoctorsExaminations de ON d.Id = de.DoctorId
FULL JOIN Examinations e ON de.ExaminationId = e.Id
ORDER BY Doctor, Examination;