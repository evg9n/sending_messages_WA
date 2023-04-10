<h1 style="text-align: center">Рассылка сообщений в WhatsApp Web</h1>

<h3 style="text-align: center">Описание</h3>

Функция **sending_messages_wa** предназначена для рассылки в WhatsApp WEB

рекомендуется перед рассылкой запустить функцию и получиться xpath от поля ввода и кнопки отправить в открытом окне selenium

**Для Linux нужно применить чтобы работал метод copy от pyperclip:**

`sudo apt-get install xclip`

`sudo apt-get install xsel`

### Принимает следующие параметры:
+ list_number: список с полными номерами, например +79874561230
+ message: текст рассылаемого сообщения
+ path_webdriver: путь к [ChromeDriver](#https://chromedriver.chromium.org/downloads)
+ path_profile: путь где будет храниться сессия 
+ xpath_field_input: xpath на поле ввода
+ xpath_button: xpath на кнопку "Отправить"