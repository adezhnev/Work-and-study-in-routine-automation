import csv
import paramiko
      
def send_show_save(ip, username, password, max_bytes=100): #  Размер нужно потестить
    vendor = ''
    data = ''
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ''' При первом подключении в trusted hosts без ручного подтверждения. 
     Обходим отсутствие ключей'''
    try:
        cli.connect(hostname=ip, username=username, password=password,
                look_for_keys=False, # Не ищем приватные ключи
                allow_agent=False) # Неиспользуем локальный ssh-agent
        stdin, stdout, stderr = cli.exec_command('?')  # Запрос ? у Jun  - 'Possible completions:' у Hua 'Current view commands:'
        data = stdout.read().decode('utf-8', errors='ignore') + stderr.read().decode('utf-8', errors='ignore') 
        """Декодируем и собираем stdout & stderr протестировать на необходимость stderr
        добавил ингорирование ошибок errors='ignore'"""
        if "Possible completions:" in data:
            vendor = 'Juniper'
        elif "Current view commands" in data:
            vendor = 'Huawei'
        else: 
            vendor = 'Unknow'
    except paramiko.AuthenticationException:
        vendor = f'Ошибка аутентификации на устройстве {ip}'
    except paramiko.SSHException as e:
        vendor = f'Ошибка подключения к устройству {ip}: {e}'
    finally:
        cli.close()
    return vendor

csv_file_path = input("Введите полный путь к файлу CSV: ")
# Запрашиваем путь к файлу CSV
try:
    # Читаем CSV файл
    with open(csv_file_path, mode='r') as f:
        reader = csv.DictReader(f,  delimiter=';')
        # Преобразуем строки CSV в список словарей
        data_list = list(reader)
        # Получаем список словарей вида {hostname: xyz, ip: a.b.c.d, vendor: <empty>}
except FileNotFoundError:
    print('Ошибка: указанный файл не найден.')
except Exception as e:
    print(f'Ошибка обработки файла: {e}') 

username = input('Введите username: ')
password = input('Введите пароль: ')

for row in data_list:
    ip = row.get('ip')
    row['vendor'] = send_show_save(ip, username, password, max_bytes=100) # Собственно цикл, проходим по ip, функцией определяем вендора и пишем это в словарь.

try:
    fieldnames = ['hostname', 'ip', 'vendor']
    with open(csv_file_path, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(data_list)
        print(f'Файл успешно сохранен {csv_file_path}') 
except FileNotFoundError:
    print('Ошибка: указанный файл не найден.')
except Exception as e:
    print(f'Ошибка обработки файла: {e}')         
      
