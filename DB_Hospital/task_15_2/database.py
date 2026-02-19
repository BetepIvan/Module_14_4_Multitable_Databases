# database.py
import pyodbc
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import Config


class DatabaseConnection:
    """Класс для управления подключением к базе данных"""

    def __init__(self):
        self.connection_string = Config.get_connection_string()
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """Установка соединения с базой данных"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            self.cursor = self.connection.cursor()
            print(f"✅ Успешно подключено к базе данных {Config.DATABASE}")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False

    def disconnect(self):
        """Закрытие соединения с базой данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("🔌 Соединение закрыто")


class DatabaseOperations:
    """Класс для выполнения операций с базой данных"""

    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
        self.results = {}

    def execute_query(self, query: str, query_name: str) -> Optional[List[Dict[str, Any]]]:
        """Выполнение запроса и сохранение результата"""
        try:
            self.db.cursor.execute(query)

            if self.db.cursor.description:
                columns = [column[0] for column in self.db.cursor.description]
                rows = self.db.cursor.fetchall()

                result = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        # Преобразование специальных типов для JSON
                        if value is None:
                            row_dict[col] = None
                        elif hasattr(value, 'as_tuple'):  # Decimal
                            row_dict[col] = float(value)
                        elif isinstance(value, datetime):
                            row_dict[col] = value.isoformat()
                        else:
                            row_dict[col] = value
                    result.append(row_dict)

                self.results[query_name] = result
                print(f"  📊 Получено записей: {len(result)}")
                return result
            else:
                print(f"  ⚠️ Запрос не вернул данных")
                return []

        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return None

    def get_results_summary(self) -> Dict:
        """Получение сводки по результатам"""
        return {
            "total_queries": len(self.results),
            "total_records": sum(len(records) for records in self.results.values()),
            "queries": {name: len(records) for name, records in self.results.items()}
        }