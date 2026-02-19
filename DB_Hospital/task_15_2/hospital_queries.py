# hospital_queries.py
from config import Config
from database import DatabaseConnection, DatabaseOperations
from queries import HospitalQueries
from utils import print_query_summary, save_to_json, print_header


def check_tables_exist(db_ops):
    """Проверка существования необходимых таблиц"""
    tables = ['Doctors', 'Wards', 'Departments', 'Examinations',
              'Sponsors', 'Donations', 'DoctorsExaminations']

    existing_tables = []
    missing_tables = []

    for table in tables:
        try:
            db_ops.db.cursor.execute(f"SELECT TOP 1 * FROM {table}")
            existing_tables.append(table)
        except:
            missing_tables.append(table)

    return existing_tables, missing_tables


def main():
    """Основная функция программы"""

    print_header("🏥 ПРОГРАММА ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ HOSPITAL")
    Config.print_config()
    print("=" * 70)

    # Создание подключения
    db_conn = DatabaseConnection()
    if not db_conn.connect():
        print("\n❌ Не удалось подключиться к базе данных. Проверьте параметры подключения в .env файле.")
        return

    # Создание объектов для работы с БД
    db_ops = DatabaseOperations(db_conn)

    # Проверка наличия таблиц
    existing_tables, missing_tables = check_tables_exist(db_ops)

    print(f"\n📊 Таблицы в базе данных Hospital:")
    print(f"   ✅ Найдены: {', '.join(existing_tables)}")
    if missing_tables:
        print(f"   ❌ Отсутствуют: {', '.join(missing_tables)}")
        print("\n⚠️  Некоторые таблицы отсутствуют. Запросы могут работать не полностью.")

    queries = HospitalQueries.get_all_queries()

    print(f"\n📋 Всего запросов для выполнения: {len(queries)}")
    print("=" * 70)

    # Выполнение всех запросов
    successful_queries = 0
    for i, (query_name, query_text) in enumerate(queries.items(), 1):
        print(f"\n🔷 [{i}/{len(queries)}] {query_name}")
        result = db_ops.execute_query(query_text, query_name)
        if result is not None:
            successful_queries += 1
        print_query_summary(query_name, result, show_preview=True)

    # Сохранение результатов в JSON
    print("\n" + "=" * 70)
    if db_ops.results:
        # Сохраняем в текущую папку
        save_to_json(db_ops.results, "hospital_queries_results.json", Config)
    else:
        print("❌ Нет результатов для сохранения")
    print("=" * 70)

    # Статистика
    summary = db_ops.get_results_summary()
    print(f"\n📈 Итоговая статистика:")
    print(f"   ✅ Успешно выполнено запросов: {successful_queries}/{len(queries)}")
    print(f"   📊 Всего получено записей: {summary['total_records']}")

    # Закрытие соединения
    db_conn.disconnect()

    print("\n✨ Программа успешно завершена.")
    print(f"   📁 Результаты сохранены в: {Path.cwd() / 'hospital_queries_results.json'}")
    print("   🔍 Для просмотра результатов запустите: python view_results.py")


if __name__ == "__main__":
    from pathlib import Path

    main()