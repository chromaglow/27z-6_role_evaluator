param(
  [Parameter(Mandatory = $true)][string]$Facility,
  [Parameter(Mandatory = $true)][string]$Title,
  [int]$Nearest = 0,
  [double]$RadiusKm = 0
)

$ErrorActionPreference = "Stop"

$cmd = @("python", "tools\risk_assessment.py", "--facility", $Facility, "--title", $Title)

if ($Nearest -gt 0) { $cmd += @("--nearest", $Nearest) }
if ($RadiusKm -gt 0) { $cmd += @("--radius_km", $RadiusKm) }

Write-Host ("Running: " + ($cmd -join " ")) -ForegroundColor Cyan
& $cmd[0] $cmd[1] $cmd[2] $cmd[3] $cmd[4] $cmd[5] $cmd[6] $cmd[7] $cmd[8] $cmd[9] $cmd[10] $cmd[11] $cmd[12] $cmd[13]
