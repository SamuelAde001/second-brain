<#
chrome_grab.ps1 - full-resolution picture of Samuel's Chrome window (for real UI shots).
Samuel, 2026-09-27: "Use my Browser to get actual screenshots". The Claude-in-Chrome screenshot
comes back at CSS size (about 1057 px wide on his 2.25x screen); this grabs the window at device
pixels with PrintWindow, so a 16:9 viewport comes out around 2380 px wide.

  powershell -ExecutionPolicy Bypass -File chrome_grab.ps1 -Out C:\...\li.png -Title "LinkedIn"
Crop the page area afterwards from innerWidth/innerHeight x devicePixelRatio (bottom-left anchored).
#>
param(
    [string]$Out = "$env:TEMP\chrome_grab.png",
    [string]$Title = ""
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class WinC {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
}
"@
[WinC]::SetProcessDPIAware() | Out-Null
$p = Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like "*$Title*" } | Select-Object -First 1
if (-not $p) { throw "no Chrome window with '$Title' in its title" }
$r = New-Object WinC+RECT
[WinC]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
$w = $r.R - $r.L; $h = $r.B - $r.T
$bmp = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
[WinC]::PrintWindow($p.MainWindowHandle, $hdc, 2) | Out-Null
$g.ReleaseHdc($hdc); $g.Dispose()
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
"saved $Out ($w x $h) title: $($p.MainWindowTitle)"
