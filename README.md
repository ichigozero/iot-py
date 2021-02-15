# About
IoT web app built with Flask for Raspberry Pi.

# Requirements
This web application has been tested in environment with
the following configuration:
- Python 3.7.3
- Redis v5.0.3
- Nginx v1.14.2

When deploying to Raspberry Pi make sure `pigpio` library is
installed and loaded. The procedure is as follows:

1. Install `pigpio` library

   ```bash
   $ sudo apt install pigpio
   ```

2. Start `pigpio` Daemon

   ```bash
   $ sudo systemctl start pigpiod
   ```

3. (Optional) Set `pigpio` Daemon to auto-start on boot

   ```bash
   $ sudo systemctl enable pigpiod
   ```

# Wiring
See below diagram for wiring reference.

![wiring](/diagram/wiring.jpg)

# Demo

![demo](/diagram/demo.jpg)

# Installation
1. Clone this repo
2. Clone the submodule repositories

   ```bash
   $ git submodule update --init --recursive
   ```

3. Create Python virtual environment

   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```

4. Install all required packages

   ```bash
   $ pip3 install submodules/pydensha/
   $ pip3 install submodules/pytenki/
   $ pip3 install submodules/tenki-no-ko/
   $ pip3 install submodules/traininfojp/
   $ pip3 install .
   ```

5. Perform DB migration

   ```bash
   $ flask db upgrade
   ```

6. Seed DB

   This step will scrape necessary data from `tenki.jp`
   and `transit.yahoo.co.jp` websites.

   ```bash
   $ flask cli init_db
   ```

7. Create systemd service

   ```bash
   $ sudo touch /etc/systemctl/system/iot-py.service
   ```

   Add the following into iot-py.service file.

   ```
   [Unit]
   Description=iot-py
   After=network.target

   [Service]
   User=pi
   Environment="GPIOZERO_PIN_FACTORY=gpio"
   Environment="SECRET_KEY=7a23557c32db38e7d51ed74f14fa7580"
   WorkingDirectory=/home/pi/iot-py
   ExecStart=/home/pi/iot-py/venv/bin/gunicorn -b 127.0.0.1:5000 --worker-class gevent "app:create_app()"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   **NOTE**
   - Make sure to change the secret key value
   - When deploying to non raspberry pi environment, change
     `Environment="GPIOZERO_PIN_FACTORY=gpio"` to
     `Environment="GPIOZERO_PIN_FACTORY=mock"`

8. Configure Nginx

   Edit `etc/nginx/sites-enabled/default`

   ```
   server {
       listen 80
       location /iot-py {
           proxy_pass http://localhost:5000;
           proxy_redirect off;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

           # Required to make EventSource working through Nginx
           proxy_set_header Connection '';
           proxy_http_version 1.1;
           chunked_transfer_encoding off;
           proxy_buffering off;
           proxy_cache off;
       }
   }
   ```

9. Reload systemd and start `iot-py` service

   ```bash
   $ sudo systemctl daemon-reload
   $ sudo systemctl start iot-py
   ```

10. (Optional) Set `iot-py` service to auto-start on boot

    ```bash
    $ sudo systemctl enable iot-py
    ```

11. (Optional) Verify that `iot-py` service is running

    ```bash
    $ sudo systemctl status iot-py
    ```

12. Reload nginx

    ```bash
    $ sudo systemctl reload nginx
    ```

# Configuration
1. Login into admin page by visiting the following URL

   ```
   <IP or Host Name>/iot-py/admin
   ```

2. Enter the following username and password.

   ```
   Username: admin
   Password: Computer1
   ```

# Text-To-Speech (TTS)
TTS can be utilized by pressing a push button wired to Raspberry Pi.
Note that TTS engine must be installed first.

1. Install TTS engine with the following command

   ```bash
   $ sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
   ```

2. (Optional) Change TTS voice file

   ```bash
   $ wget https://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.7/MMDAgent_Example-1.7.zip --no-check-certificate
   $ unzip MMDAgent_Example-1.7.zip
   $ sudo cp -R ./MMDAgent_Example-1.7/Voice/mei /usr/share/hts-voice/
   ```
