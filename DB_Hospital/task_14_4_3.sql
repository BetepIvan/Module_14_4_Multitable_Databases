-- Запрос 1: Врачи и их обследования (с временем)
SELECT
    d.Surname AS 'Фамилия врача',
    d.Name AS 'Имя врача',
    e.Name AS 'Название обследования',
    de.StartTime AS 'Начало',
    de.EndTime AS 'Окончание',
    w.Name AS 'Палата'
FROM DoctorsExaminations de
JOIN Doctors d ON de.DoctorId = d.Id
JOIN Examinations e ON de.ExaminationId = e.Id
JOIN Wards w ON de.WardId = w.Id
ORDER BY d.Surname, de.StartTime;

-- Запрос 2: Пожертвования по отделениям и спонсорам
SELECT
    s.Name AS 'Спонсор',
    d.Amount AS 'Сумма',
    d.Date AS 'Дата',
    dep.Name AS 'Отделение'
FROM Donations d
JOIN Sponsors s ON d.SponsorId = s.Id
JOIN Departments dep ON d.DepartmentId = dep.Id
WHERE d.Amount > 1000
ORDER BY d.Amount DESC;

-- Запрос 3: Количество обследований на каждого врача
SELECT
    d.Surname AS 'Врач',
    COUNT(de.Id) AS 'Количество обследований'
FROM Doctors d
LEFT JOIN DoctorsExaminations de ON d.Id = de.DoctorId
GROUP BY d.Id, d.Surname
ORDER BY 'Количество обследований' DESC;

-- Запрос 4: Палаты и количество обследований в них
SELECT
    w.Name AS 'Палата',
    dep.Name AS 'Отделение',
    COUNT(de.Id) AS 'Проведено обследований'
FROM Wards w
JOIN Departments dep ON w.DepartmentId = dep.Id
LEFT JOIN DoctorsExaminations de ON w.Id = de.WardId
GROUP BY w.Id, w.Name, dep.Name
ORDER BY 'Проведено обследований' DESC;

-- Запрос 5: Свободные палаты (где нет обследований)
SELECT
    w.Name AS 'Палата',
    dep.Name AS 'Отделение',
    w.Places AS 'Количество мест'
FROM Wards w
JOIN Departments dep ON w.DepartmentId = dep.Id
LEFT JOIN DoctorsExaminations de ON w.Id = de.WardId
WHERE de.Id IS NULL;