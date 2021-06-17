@echo off

rem echo > smartlock.log

FOR /L %%i IN (1,1,60) DO (
	smartlock.py
	rem  >> smartlock.log 2>&1
	timeout 1 > NUL
)
