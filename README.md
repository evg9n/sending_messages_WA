<h1 style="text-align: center">Рассылка сообщений в WhatsApp Web</h1>

Функция **sending_messages_wa** предназначена для рассылки в WhatsApp WEB

**Рекомендуется перед рассылкой запустить функцию и получиться xpath от поля ввода и кнопки "Отправить" в открытом окне selenium**

**Для Linux нужно установить xclip и xsel, чтобы работал метод copy от pyperclip:**

`sudo apt-get update`
`sudo apt install python3-pyperclip`

`sudo apt-get install xclip`

`sudo apt-get install xsel`

### Принимает следующие параметры:
+ list_number: список с полными номерами, например +79874561230
+ message: текст рассылаемого сообщения
+ path_webdriver: путь к ( скачать можно по ссылки https://chromedriver.chromium.org/downloads)
+ xpath_field_input: xpath на поле ввода
+ xpath_button: xpath на кнопку "Отправить"
