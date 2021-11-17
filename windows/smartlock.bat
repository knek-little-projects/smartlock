@echo off

cd ..

FOR /L %%i IN (1,1,20) DO (
	if NOT EXIST C:\smartlock.flags\STOP (
		type config.d\* windows\config.d\* | python smartlock.py -R
	)
	timeout 3 > NUL
)
