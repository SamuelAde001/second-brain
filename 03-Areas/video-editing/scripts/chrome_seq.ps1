<#
chrome_seq.ps1 - record a real scroll in Samuel's Chrome as full-resolution frames.
Pair it with a page script that steps the scroll and sets document.title to "S<n>" once each
step has settled ("moving" while it scrolls, "DONE" at the end). This loop grabs the window
(PrintWindow, device pixels) and saves each grab as <Dir>\s<n>.png, so every step keeps its last
settled grab. Stops on "DONE" or after -Timeout seconds.

  powershell -ExecutionPolicy Bypass -File chrome_seq.ps1 -Dir C:\...\web_seq -Timeout 120
#>
param([string]$Dir, [int]$Timeout = 120)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force $Dir | Out-Null
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public static class WinS {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
}
"@
[WinS]::SetProcessDPIAware() | Out-Null
function Title($h) { $sb = New-Object System.Text.StringBuilder 512; [WinS]::GetWindowText($h, $sb, 512) | Out-Null; $sb.ToString() }
$p = Get-Process chrome | Where-Object { $_.MainWindowHandle -ne 0 } | Where-Object { (Title $_.MainWindowHandle) -match '^(S\d+|moving|READY)' } | Select-Object -First 1
if (-not $p) { throw "no Chrome window titled S<n>/moving/READY" }
$h = $p.MainWindowHandle
$t0 = Get-Date; $n = 0
while (((Get-Date) - $t0).TotalSeconds -lt $Timeout) {
  $title = Title $h
  if ($title -match '^DONE') { break }
  if ($title -match '^S(\d+)') {
    $k = $Matches[1]
    $r = New-Object WinS+RECT; [WinS]::GetWindowRect($h, [ref]$r) | Out-Null
    $bmp = New-Object System.Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
    $g = [System.Drawing.Graphics]::FromImage($bmp); $hdc = $g.GetHdc()
    [WinS]::PrintWindow($h, $hdc, 2) | Out-Null
    $g.ReleaseHdc($hdc); $g.Dispose()
    if ((Title $h) -match "^S$k\b") { $bmp.Save((Join-Path $Dir "s$k.png"), [System.Drawing.Imaging.ImageFormat]::Png); $n++ }
    $bmp.Dispose()
  } else { Start-Sleep -Milliseconds 60 }
}
"grabs saved: $n in $Dir"
