REM Delete the directories 
rd /s /q "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist"
rd /s /q "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\build"


REM "Compile" the code
pyinstaller main.py 


REM Copy the dependencies
mkdir "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\babelfish"
xcopy "C:\Python35\Lib\site-packages\babelfish" "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\babelfish" /E

mkdir "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\guessit"
xcopy "C:\Python35\Lib\site-packages\guessit" "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\guessit" /E


REM Create the archive 
7z a -tzip "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\tvst_checker.zip" "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main"

REM Upload the file
copy /Y "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\tvst_checker.zip" "C:\Users\Shock\Google Drive\Python"