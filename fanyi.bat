@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
ren 
c:
cd C:\Users\Administrator\Desktop\py
python test.py

PAUSE 
taskkill /f /im cmd.exe
exit