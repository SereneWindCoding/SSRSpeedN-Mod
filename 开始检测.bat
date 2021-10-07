@echo off&
echo.
echo ##### 机场奈飞解锁批量检测工具 Mod By 肥羊 #####
echo.
if exist "%~dp0\main.py" (echo 已在SSRSpeed目录下，欢迎使用) else (echo 请放在检测工具目录下运行！ )
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%~dp0
bcdedit >nul
if '%errorlevel%' NEQ '0' (echo 当前无管理员权限) else (echo 当前已获取管理员权限)
:start
echo ====================================
echo 1：开始测速（自定义设置）
echo 2：首次运行前安装pip和相关支持（需要管理员权限）
echo 3：为本次运行获取管理员权限
echo ====================================
echo 请选择（1~3）：
choice /c 123
if %errorlevel%==3 (goto :uac)
if %errorlevel%==2 (goto :pip)
if %errorlevel%==1 (goto :test2)


:pip
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%~dp0
bcdedit >nul
if '%errorlevel%' NEQ '0' (echo #当前无管理员权限，无法安装。 && echo. && echo #您可以通过命令3获取权限，或右键以管理员权限启动。 && pause && goto :start) else (goto :pip2)
:pip2
python -m pip install --upgrade pip
pip3 install -r %~dp0%\requirements.txt
::pip3 install requests
::pip3 install pyyaml
::pip3 install Pillow
::pip3 install pysocks
::pip3 install aiohttp
::pip3 install aiohttp_socks
::pip3 install requests[socks]
::pip3 install flask
::pip3 install flask-cors
pause
goto :start

:test2
echo.
echo      以下自定义选项留空回车即可跳过
echo.
:test3
set /p a=请输入您的订阅链接(右键直接粘贴，不可留空):
if "%a%"=="" (
goto :test3
) else (
goto :jx1
)
:jx1
echo      以下2项可以通过空格分隔关键词
set /p e=1.使用关键字通过注释筛选节点:
set /p i=2.通过使用关键字的注释排除节点:
set /p k=3.请输入测速组名:
echo.
if "%e%"=="" (
set e= && goto :jx1
) else (
set e=--include-remark %e% && goto :jx1
)
:jx1
if "%i%"=="" (
set i= && goto :jx2
) else (
set i=--exclude-remark %i% && goto :jx2
)
:jx2
if "%k%"=="" (
set k= && goto :jx3
) else (
set k=-g %k% && goto :jx3
)
:jx3
set o=--skip-requirements-check && goto :jx4
:jx4
echo python main.py -u "%a%" %e% %i% %k% %y% %m% %n%  %o%
echo.
python main.py -u "%a%" %e% %i% %k% %y% %m% %n%  %o%
pause
set e=
set i=
set k=
set o=
goto :start

:uac
echo.
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%~dp0
bcdedit >nul
if '%errorlevel%' NEQ '0' (goto UACPrompt) else (goto UACAdmin)
:UACPrompt
echo 提示：通用依赖安装需要管理员权限
echo.
echo      尝试获取管理员权限，程序将重启
ping -n 3 127.0.0.1>nul && %1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit
exit /B
:UACAdmin
cd /d "%~dp0"
echo.
echo 已获取管理员权限
echo.
pause
goto :start