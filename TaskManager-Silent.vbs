' Silent launcher for Task Manager Desktop App
' Launches the application without showing a console window

Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
WshShell.CurrentDirectory = strScriptPath

' Launch the batch file hidden (0 = hidden, True = wait for it to complete)
WshShell.Run "cmd /c TaskManager.bat", 0, False

' Clean up
Set WshShell = Nothing
Set objFSO = Nothing

