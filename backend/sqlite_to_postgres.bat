@echo off
chcp 65001 >nul
REM ==============================================================
REM  Kompyuterdagi db.sqlite3 ma'lumotlarini Railway PostgreSQL'ga ko'chirish.
REM  DIQQAT: Postgres bazasidagi BOR ma'lumotlar o'chib, SQLite'dagilar yoziladi.
REM  Faqat birinchi marta ko'chirishda ishlating.
REM ==============================================================

if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate
pip install -q -r requirements.txt

echo.
echo 1/4  SQLite'dan ma'lumotlar olinmoqda (data.json)...
set DATABASE_URL=
python manage.py migrate --noinput
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --exclude admin.logentry --exclude sessions -o data.json
if errorlevel 1 goto :error

echo.
echo Railway - Postgres - Connect - "Public Network" bo'limidagi DATABASE_PUBLIC_URL ni joylang:
set /p DATABASE_URL=DATABASE_URL: 
if "%DATABASE_URL%"=="" goto :error

echo.
set /p CONFIRM=Postgres'dagi eski ma'lumotlar o'chiriladi. Davom etasizmi? (ha/yo'q): 
if /I not "%CONFIRM%"=="ha" goto :cancel

echo 2/4  Jadvallar yaratilmoqda...
python manage.py migrate --noinput
if errorlevel 1 goto :error
echo 3/4  Ma'lumotlar yozilmoqda...
python manage.py flush --noinput
python manage.py loaddata data.json
if errorlevel 1 goto :error
echo 4/4  Testlar va admin tekshirilmoqda...
python manage.py seed_demo

echo.
echo Tayyor! Ma'lumotlar PostgreSQL'ga ko'chirildi.
set DATABASE_URL=
pause
exit /b 0

:cancel
echo Bekor qilindi. Hech narsa o'zgarmadi.
set DATABASE_URL=
pause
exit /b 0

:error
echo Xatolik yuz berdi. Yuqoridagi xabarni o'qing.
set DATABASE_URL=
pause
exit /b 1
