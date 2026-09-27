<#
fusion_view.ps1 - picture of what Resolve shows right now (e.g. the Fusion page viewer),
without switching pages or touching the comp. Samuel, 2026-09-27: "Create a script that
let's you always view the view on fusion page".

Uses PrintWindow with PW_RENDERFULLCONTENT, so it works even when Resolve is behind other
windows (not when it is minimised). To look at a given frame, set it first over the bridge
(`comp.CurrentTime = n`), then run this.

  powershell -File fusion_view.ps1 -Out C:\...\view.png                 # whole window, half size
  powershell -File fusion_view.ps1 -Out view.png -Crop viewer           # the saved viewer area
  powershell -File fusion_view.ps1 -Out view.png -Crop 0,0.05,0.5,0.45  # x,y,w,h as window fractions
  powershell -File fusion_view.ps1 -SetViewer 0,0.05,0.5,0.45           # remember the viewer area
#>
param(
    [string]$Out = "$env:TEMP\fusion_view.png",
    [string]$Crop = "",
    [double]$Scale = 0.5,
    [string]$SetViewer = ""
)
$ErrorActionPreference = "Stop"
$cfg = Join-Path $PSScriptRoot "fusion_view.viewer.txt"
if ($SetViewer) { Set-Content -Path $cfg -Value $SetViewer -Encoding ascii; "viewer area saved: $SetViewer"; return }

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public static class Win {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
}
"@
[Win]::SetProcessDPIAware() | Out-Null

$p = Get-Process Resolve -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $p) { throw "Resolve window not found" }
$h = $p.MainWindowHandle
if ([Win]::IsIconic($h)) { throw "Resolve is minimised - restore it to capture" }
$r = New-Object Win+RECT
[Win]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L; $hh = $r.B - $r.T

$bmp = New-Object System.Drawing.Bitmap $w, $hh
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
$ok = [Win]::PrintWindow($h, $hdc, 2)          # 2 = PW_RENDERFULLCONTENT (GPU-drawn viewers)
$g.ReleaseHdc($hdc); $g.Dispose()
if (-not $ok) { throw "PrintWindow failed" }

if ($Crop -eq "viewer") {
    if (-not (Test-Path $cfg)) { throw "no viewer area saved yet - run with -SetViewer x,y,w,h" }
    $Crop = (Get-Content $cfg -Raw).Trim()
}
$src = New-Object System.Drawing.Rectangle 0, 0, $w, $hh
if ($Crop) {
    $f = $Crop.Split(",") | ForEach-Object { [double]$_ }
    $src = New-Object System.Drawing.Rectangle ([int]($f[0] * $w)), ([int]($f[1] * $hh)), ([int]($f[2] * $w)), ([int]($f[3] * $hh))
}
$ow = [int]($src.Width * $Scale); $oh = [int]($src.Height * $Scale)
$outBmp = New-Object System.Drawing.Bitmap $ow, $oh
$g2 = [System.Drawing.Graphics]::FromImage($outBmp)
$g2.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g2.DrawImage($bmp, (New-Object System.Drawing.Rectangle 0, 0, $ow, $oh), $src, [System.Drawing.GraphicsUnit]::Pixel)
$g2.Dispose(); $bmp.Dispose()
$outBmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png); $outBmp.Dispose()
"saved $Out (${ow}x${oh}, window ${w}x${hh})"
