@echo off

rem echo > smartlock.log

cd ..
FOR /L %%i IN (1,1,20) DO (
	python smartlock windows\smartlock.yaml -R
	rem  >> smartlock.log 2>&1
	timeout 3 > NUL
)
