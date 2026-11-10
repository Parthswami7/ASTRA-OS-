Set WshShell = CreateObject("WScript.Shell")
' The "0" at the end tells Windows to run this completely hidden in the background
WshShell.Run chr(34) & "D:\JARVIS_MAIN_FOLDER\PYTHON_JARVIS\JARVIS_OS1\jarvis_autoboot.bat" & Chr(34), 0
Set WshShell = Nothing