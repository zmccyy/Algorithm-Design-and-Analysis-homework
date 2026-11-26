param(
  [ValidateSet('Both', 'Claude', 'Codex')]
  [string]$Target = 'Both'
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$src = Join-Path $root 'skills'
$license = Join-Path $root 'LICENSE'

$destinations = @()
if ($Target -in @('Both', 'Claude')) { $destinations += Join-Path $HOME '.claude\skills' }
if ($Target -in @('Both', 'Codex')) { $destinations += Join-Path $HOME '.codex\skills' }

foreach ($dest in $destinations) {
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Get-ChildItem -Path $src -Directory | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
  }
  Copy-Item -Path $license -Destination (Join-Path $dest 'LICENSE-grad-project-mentor.txt') -Force
  Write-Host "Installed grad-project-mentor skills -> $dest"
}

Write-Host 'Restart Claude Code / Codex to load the skills.'
