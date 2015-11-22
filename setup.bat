REM Delete the directories 
rd /s /q "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist"
rd /s /q "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\build"

pyinstaller main.py 

mkdir "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\babelfish"
xcopy "C:\Python34\Lib\site-packages\babelfish" "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\babelfish" /E

mkdir "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\guessit"
xcopy "C:\Python34\Lib\site-packages\guessit" "C:\Users\Shock\PycharmProjects\TvShowTimeChecker\dist\main\guessit" /E