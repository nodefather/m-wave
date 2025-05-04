# PowerShell script to fully set up a Windows machine for Cursor development

Write-Host "=== Cursor Dev Environment Setup ===" -ForegroundColor Cyan

# 1. Ensure Chocolatey is available and in PATH
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    $env:Path += ";C:\ProgramData\chocolatey\bin"
}

# 2. Install core tools
$tools = @(
    "docker-desktop", "python", "poetry", "nodejs-lts", "git", "vscode", "wsl2"
)
foreach ($tool in $tools) {
    Write-Host "Installing $tool..."
    choco install $tool -y --ignore-checksums
}

# 3. Enable Hyper-V and Virtualization
Write-Host "Enabling Hyper-V and Virtualization..."
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart

# 4. Check virtualization support
$virt = Get-WmiObject -Class Win32_Processor | Select-Object -ExpandProperty VirtualizationFirmwareEnabled
if ($virt) {
    Write-Host "Virtualization is enabled."
} else {
    Write-Host "Virtualization is NOT enabled. Please enable it in your BIOS/UEFI settings."
}

# 5. Install WSL2 kernel update (if needed)
Write-Host "Checking WSL2 kernel..."
wsl --set-default-version 2

# 6. Final message and restart prompt
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host "It is recommended to restart your computer now."
$restart = Read-Host "Restart now? (y/n)"
if ($restart -eq "y") {
    Restart-Computer
} else {
    Write-Host "Please restart manually before starting development." -ForegroundColor Yellow
} 