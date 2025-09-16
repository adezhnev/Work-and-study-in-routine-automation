import csv
import json

# Запрашиваем путь к файлу CSV
csv_file_path = input("Введите полный путь к файлу CSV: ")

# Получаем название файла без расширения и формируем путь для JSON
json_file_path = f"{'.'.join(csv_file_path.split('.')[:-1])}.json"

try:
    # Читаем CSV файл
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file,  delimiter=';')
        
        # Преобразуем строки CSV в список словарей
        data_list = list(reader)
    
    # Сохраняем полученные данные в JSON файл
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)
    
    print(f'Файл успешно сохранён в {json_file_path}')
except FileNotFoundError:
    print('Ошибка: указанный файл не найден.')
except Exception as e:
    print(f'Ошибка обработки файла: {e}')
    