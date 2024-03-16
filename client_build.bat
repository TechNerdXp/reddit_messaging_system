@echo off
REM Empty the folder client_build
for /R "client_build" %%G in (*) do del /S /Q "%%G"

REM Change directory to client
cd client

REM Run npm build
npm run build && xcopy /E /I /Y build ..\\client_build

REM Change directory back to project home
cd ..
