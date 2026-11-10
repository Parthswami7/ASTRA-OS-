@echo off
title ASTRA OS BOOT SEQUENCE
rundll32.exe user32.dll,LockWorkStation
D:
cd "D:\ASTRA_MAIN_FOLDER\PYTHON_ASTRA\ASTRA_OS1"
"C:\Users\ASUS\AppData\Local\Programs\Python\Python314\python.exe" core/main.py