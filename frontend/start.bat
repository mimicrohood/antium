@echo off
REM Start the local mirror of the mycoid (rayoid) Framer site.
REM Requires Python 3. Serves at http://127.0.0.1:8848/
cd /d "%~dp0"
echo Starting local server at http://127.0.0.1:8848/
echo Press Ctrl+C to stop.
python serve.py 8848
