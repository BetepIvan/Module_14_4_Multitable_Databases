-- Запрос 1: Студенты с названиями групп
SELECT
    s.LastName AS 'Имя',
    s.FirstName AS 'Фамилия',
    g.GroupName AS 'Группа'
FROM Students s
JOIN Groups g ON s.GroupId = g.Id
ORDER BY g.GroupName, s.FirstName;

-- Запрос 2: Преподаватели и предметы, которые они ведут
SELECT
    t.FirstName AS 'Преподаватель',
    sub.SubjectName AS 'Предмет'
FROM Teachers t
JOIN TeachersSubjects ts ON t.Id = ts.TeacherId
JOIN Subjects sub ON ts.SubjectId = sub.Id
ORDER BY t.FirstName, sub.SubjectName;

-- Запрос 3: Средняя оценка по предметам
SELECT
    sub.SubjectName AS 'Предмет',
    ROUND(AVG(CAST(a.Assesment AS FLOAT)), 2) AS 'Средняя оценка'
FROM Subjects sub
LEFT JOIN Achievements a ON sub.Id = a.SubjectId
GROUP BY sub.Id, sub.SubjectName
ORDER BY 'Средняя оценка' DESC;

-- Запрос 4: Количество студентов в каждой группе
SELECT
    g.GroupName AS 'Группа',
    COUNT(s.Id) AS 'Количество студентов'
FROM Groups g
LEFT JOIN Students s ON g.Id = s.GroupId
GROUP BY g.Id, g.GroupName
ORDER BY 'Количество студентов' DESC;

-- Запрос 5: Студенты с максимальной оценкой по 'SQL Server'
SELECT
    s.FirstName AS 'Фамилия',
    s.LastName AS 'Имя',
    a.Assesment AS 'Оценка'
FROM Students s
JOIN Achievements a ON s.Id = a.StudentId
JOIN Subjects sub ON a.SubjectId = sub.Id
WHERE sub.SubjectName = 'SQL Server'
  AND a.Assesment = (
      SELECT MAX(Assesment)
      FROM Achievements a2
      WHERE a2.SubjectId = sub.Id
  );