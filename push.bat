@echo off
set /p comment="Enter Comment: "
git add ./
git commit -m "%comment%"
git push -u origin master
pause