# PowerShell Script to Create Desktop Shortcut
# Run this with: powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WshShell = New-Object -comObject WScript.Shell
$ShortcutPath = "$Home\Desktop\Task Manager.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "$ScriptDir\TaskManager.bat"
$Shortcut.WorkingDirectory = "$ScriptDir"
$Shortcut.Description = "Task Manager Desktop Application"

# Set icon if it exists
$IconPath = "$ScriptDir\taskmanager.ico"
if (Test-Path $IconPath) {
    $Shortcut.IconLocation = $IconPath
    Write-Host "✅ Using custom icon: taskmanager.ico" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Custom icon not found. Run: python create_icon.py" -ForegroundColor Yellow
    # Use default Python icon as fallback
    try {
        $PythonPath = (Get-Command python).Source
        $Shortcut.IconLocation = $PythonPath
        Write-Host "   Using Python icon as fallback" -ForegroundColor Yellow
    } catch {
        Write-Host "   Using default icon" -ForegroundColor Yellow
    }
}

$Shortcut.Save()

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Desktop Shortcut Created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Shortcut location: $Home\Desktop\Task Manager.lnk" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now double-click 'Task Manager' on your desktop" -ForegroundColor White
Write-Host "to launch the application!" -ForegroundColor White
Write-Host ""

