param([string]$Out, [double]$Scale = 0.45)
# capture Resolve's edit-page viewer
& powershell -File "C:\Users\repzy\Desktop\My Second brain\03-Areas\video-editing\scripts\fusion_view.ps1" -Out $Out -Crop "0.387,0.05,0.416,0.428" -Scale $Scale | Out-Null
