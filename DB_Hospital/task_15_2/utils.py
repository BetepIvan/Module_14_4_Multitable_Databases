# utils.py
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


def format_value(value: Any) -> str:
    """Форматирование значения для вывода"""
    if value is None:
        return "NULL"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, dict) or isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    else:
        return str(value)


def print_table(results: List[Dict], limit: int = 10):
    """Вывод результатов в виде таблицы"""
    if not results:
        print("  📭 Нет данных")
        return

    # Получаем заголовки
    headers = list(results[0].keys())

    # Выводим заголовки
    print("  " + " | ".join(headers))
    print("  " + "-" * 50)

    # Выводим данные
    for i, row in enumerate(results[:limit]):
        row_str = "  "
        for header in headers:
            value = format_value(row.get(header, ''))
            row_str += f"{value[:15]:<15} | "
        print(row_str[:-2])

    if len(results) > limit:
        print(f"  ... и еще {len(results) - limit} записей")


def print_query_summary(query_name: str, results: Optional[List[Dict]], show_preview: bool = True):
    """Вывод результатов запроса в красивом формате"""
    print(f"\n📌 {query_name}")
    print("-" * 70)

    if results is None:
        print("  ❌ Ошибка выполнения запроса")
    elif len(results) == 0:
        print("  📭 Нет данных")
    else:
        print(f"  📊 Всего записей: {len(results)}")

        if show_preview and len(results) > 0:
            print("  🔍 Первые 3 записи:")
            for i, record in enumerate(results[:3]):
                record_str = ", ".join([f"{k}: {format_value(v)}" for k, v in record.items()])
                print(f"    {i + 1}. {record_str[:100]}{'...' if len(record_str) > 100 else ''}")


def save_to_json(results: Dict, filename: str = "hospital_queries_results.json", config: Any = None) -> bool:
    """Сохранение результатов в JSON файл"""
    try:
        total_records = sum(len(records) for records in results.values())

        output = {
            "timestamp": datetime.now().isoformat(),
            "database": "Hospital",
            "total_queries": len(results),
            "total_records": total_records,
            "results": results
        }

        # Добавляем информацию о конфигурации, если предоставлена
        if config:
            output["server"] = config.SERVER
            output["user"] = config.USER

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Результаты сохранены в файл: {filename}")
        print(f"   Всего запросов: {len(results)}, записей: {total_records}")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения в JSON: {e}")
        return False


def clear_screen():
    """Очистка экрана"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str, width: int = 80):
    """Печать заголовка"""
    print("=" * width)
    print(f"{text:^{width}}")
    print("=" * width)