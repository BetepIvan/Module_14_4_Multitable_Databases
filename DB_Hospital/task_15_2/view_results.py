# view_results.py
import json
from utils import clear_screen, print_header, format_value


def view_json_results(filename="hospital_queries_results.json"):
    """Просмотр результатов из JSON файла"""

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        while True:
            clear_screen()
            print_header("🏥 РЕЗУЛЬТАТЫ ЗАПРОСОВ К БАЗЕ HOSPITAL")

            print(f"\n📅 Время создания: {data['timestamp']}")
            if 'server' in data:
                print(f"🖥️  Сервер: {data['server']}")
            if 'user' in data:
                print(f"👤 Пользователь: {data['user']}")
            print(f"📊 Всего запросов: {data['total_queries']}")
            print(f"📈 Всего записей: {data['total_records']}")

            results = data['results']

            print("\n" + "-" * 80)
            print("📋 ДОСТУПНЫЕ ЗАПРОСЫ:")
            print("-" * 80)

            # Нумерованный список запросов
            query_list = list(results.keys())
            for i, query_name in enumerate(query_list, 1):
                records_count = len(results[query_name])
                # Сокращаем длинное имя для отображения
                short_name = query_name[:57] + "..." if len(query_name) > 60 else query_name
                print(f"{i:2}. {short_name:<60} - {records_count:4} записей")

            print("\n" + "-" * 80)
            print("МЕНЮ:")
            print("  [номер] - Показать результаты запроса")
            print("  [s]     - Показать статистику")
            print("  [q]     - Выход")

            choice = input("\nВаш выбор: ").strip().lower()

            if choice == 'q':
                break
            elif choice == 's':
                show_statistics(results, query_list)
            elif choice.isdigit():
                show_query_results(choice, query_list, results)
            else:
                print("❌ Неверный выбор")
                input("Нажмите Enter...")

    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден")
        print("\nСначала запустите основную программу:")
        print("python hospital_queries.py")
        input("\nНажмите Enter для выхода...")
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        input("\nНажмите Enter для выхода...")


def show_statistics(results, query_list):
    """Показать статистику по запросам"""
    clear_screen()
    print_header("📊 СТАТИСТИКА ПО ЗАПРОСАМ")

    # Группировка по типам запросов
    stats = {
        'EXISTS': {'count': 0, 'records': 0},
        'ANY/SOME': {'count': 0, 'records': 0},
        'ALL': {'count': 0, 'records': 0},
        'UNION': {'count': 0, 'records': 0},
        'JOIN': {'count': 0, 'records': 0}
    }

    for query_name in query_list:
        records_count = len(results[query_name])
        if 'EXISTS' in query_name:
            stats['EXISTS']['count'] += 1
            stats['EXISTS']['records'] += records_count
        elif 'ANY' in query_name or 'SOME' in query_name:
            stats['ANY/SOME']['count'] += 1
            stats['ANY/SOME']['records'] += records_count
        elif 'ALL' in query_name and 'UNION' not in query_name:
            stats['ALL']['count'] += 1
            stats['ALL']['records'] += records_count
        elif 'UNION' in query_name:
            stats['UNION']['count'] += 1
            stats['UNION']['records'] += records_count
        elif 'JOIN' in query_name:
            stats['JOIN']['count'] += 1
            stats['JOIN']['records'] += records_count

    print("\n📊 Статистика по типам запросов:")
    print("-" * 50)
    for stat_type, stat_data in stats.items():
        if stat_data['count'] > 0:
            print(f"{stat_type:10} : {stat_data['count']:2} запросов, {stat_data['records']:4} записей")

    # Самая большая таблица
    max_query = max(query_list, key=lambda q: len(results[q]))
    print(f"\n🏆 Самая большая таблица:")
    print(f"   {max_query}")
    print(f"   Записей: {len(results[max_query])}")

    input("\nНажмите Enter для продолжения...")


def show_query_results(choice, query_list, results):
    """Показать результаты конкретного запроса"""
    idx = int(choice) - 1
    if 0 <= idx < len(query_list):
        query_name = query_list[idx]
        records = results[query_name]

        clear_screen()
        print_header(f"📌 {query_name}")
        print(f"\nВсего записей: {len(records)}")
        print("-" * 80)

        if records:
            # Определяем ширину для нумерации
            width = len(str(len(records)))

            for i, record in enumerate(records, 1):
                print(f"{i:>{width}}. ", end="")

                # Форматированный вывод записи
                record_items = []
                for key, value in record.items():
                    record_items.append(f"{key}: {format_value(value)}")

                # Перенос строк для длинных записей
                line = ", ".join(record_items)
                if len(line) > 100:
                    print(line[:100] + "...")
                else:
                    print(line)

                # Пауза после каждых 20 записей
                if i % 20 == 0 and i < len(records):
                    if input("\nНажмите Enter для продолжения (q - выход)... ").lower() == 'q':
                        break
        else:
            print("Нет данных для отображения")

        input("\nНажмите Enter для продолжения...")
    else:
        print("❌ Неверный номер")
        input("Нажмите Enter...")


if __name__ == "__main__":
    view_json_results()