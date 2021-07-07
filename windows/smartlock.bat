@echo off

cd ..

FOR /L %%i IN (1,1,20) DO (
	timeout 3 > NUL
	if NOT EXIST C:\smartlock.flags\STOP (
		type config.d\* windows\config.d\* | python smartlock.py -R
	)
)
