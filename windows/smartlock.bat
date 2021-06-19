@echo off

cd ..

FOR /L %%i IN (1,1,20) DO (
	timeout 3 > NUL
	if NOT EXIST C:\smartlock.flags\STOP (
		python smartlock.py windows\smartlock.yaml -R
	)
)
