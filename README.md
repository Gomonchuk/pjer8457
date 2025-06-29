# Шаги по развертыванию приложение на сервере c systemd
## 1.Подключение через ssh к серверу
### 1.1 Сгенерировать публичный и приватный ключ с помощью ультилиты ssh-keygen
```bash
ssh-keygen
```
### 1.2 Подключение к серверу через сгенерированный публичный ключ
```bash
ssh-copy-id -i /home/ubuntu/.ssh/id_rsa.pub login@ip_address_of_server
```
потребует ввести пароль от учетной записи пользователя(login) на удаленном хосте
### 1.3 В дальнейшим достаточно подключаться через комманду
```bash
ssh login@ip_address_of_server
```
## 2. Установка всех необходимых пакетов
```
sudo apt update
sudo apt upgrade
sudo apt install ufw git python3 nginx python3-venv 
```
## 3. Загружаем приложение в стандартную директорию /var/www/
```
cd /var/www/ && sudo git clone https://github.com/Gomonchuk/pjer8457 my_flask_app 
sudo chown -R :www-data ./
cd my_flask_app
```
### 3.1 Создание виртуального окружение python с помощью модуля venv
```
sudo python3 -m venv venv
```
### 3.2 Активируем виртуальное окружение
```
. venv/bin/activate
```
### 3.3 Загружаем зависемости
```
pip install -r requirements.txt
```
### 4. Регистрируем сокет в systemd
```
sudo vim /etc/systemd/system/gunicorn.socket
```
### 4.1 Конфиг сокета
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
SocketUser=www-data
SocketGroup=www-data
SocketMode=0660

[Install]
WantedBy=sockets.target
```
## 5. Регистрируем daemon(службу) в systemd
```
sudo vim /etc/systemd/system/gunicorn.service
```
### 5.1 Конфиг daemon(cлужбы)
```
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/my_flask_app
ExecStart=/var/www/my_flask_app/venv/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock  -m 007 wsgi:app1

[Install]
WantedBy=multi-user.target
```
## 6. Настройка nginx
```
sudo rm /etc/nginx/sites-available/default
sudo vim /etc/nginx/sites-available/my_flask_app
```
### 6.1 Конфиг nginx для нашего приложения
```
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /favicon.ico {
        alias /var/www/my_flask_app/static/favicon.ico;

    }
}
```
### 6.2 Активиция конфига Nginx
```
sudo ln -s /etc/nginx/sites-available/my_flask_app /etc/nginx/sites-enabled
```
## 7. Настроим iptables через UFW
```
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh # не забываем а то можно потерять доступ к серверу
sudo ufw enable
```
## 8. Обновляем конфигурацию менеджера системных служб systemd
```
sudo systemctl daemon-reload
```
## 8.1 Включаем и запускаем сокет
```
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.socket
```
## 8.2 Включаем и запускаем daemon(службу
```
sudo systemctl enable gunicorn.service
sudo systemctl start gunicorn.service
```
## 8.3 Перезагружаем nginx
```
sudo systemctl reload nginx
```
