-- Запрос 1: Все студенты
SELECT
    id,
    first_name AS 'Имя',
    last_name AS 'Фамилия',
    birth_data AS 'Дата рождения',
    email AS 'Email'
FROM Students;

-- Запрос 2: Все продукты (фрукты и овощи)
SELECT
    id,
    Название AS 'Продукт',
    Тип AS 'Тип',
    Цвет AS 'Цвет',
    Калорийность AS 'Калории'
FROM Product;

-- Запрос 3: Только фрукты
SELECT
    Название AS 'Фрукт',
    Цвет AS 'Цвет',
    Калорийность AS 'Калории'
FROM Product
WHERE Тип = 'фрукт';

-- Запрос 4: Только овощи
SELECT
    Название AS 'Овощ',
    Цвет AS 'Цвет',
    Калорийность AS 'Калории'
FROM Product
WHERE Тип = 'овощ';

-- Запрос 5: Студенты у которых есть стипендия (Grants не пустой)
SELECT
    first_name + ' ' + last_name AS 'Студент',
    Grants AS 'Стипендия',
    email AS 'Email'
FROM Students
WHERE Grants IS NOT NULL;