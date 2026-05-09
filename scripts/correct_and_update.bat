
@echo off
echo Running fix_quellen.py...
python fix_quellen.py ../data/clusters
if errorlevel 1 (
    echo fix_quellen.py failed. Aborting.
    pause
    exit /b 1
)
 
echo.
echo Running build.py...
python build.py
if errorlevel 1 (
    echo build.py failed.
    pause
    exit /b 1
)
 
echo.
echo All done!
pause
