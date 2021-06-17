@echo off

cd ..
FOR /L %%i IN (1,1,20) DO (
	timeout 3 > NUL
	python smartlock.py windows\smartlock.yaml -R
)
