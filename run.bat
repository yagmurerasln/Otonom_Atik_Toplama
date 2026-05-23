@echo off
title Otonom Atik Toplama Simulasyonu

echo ==========================================
echo  Otonom Atik Toplama Simulasyonu
echo ==========================================
echo.

echo Python kontrol ediliyor...
py --version >nul 2>&1

if errorlevel 1 (
    echo Python bulunamadi.
    echo Lutfen Python kurulu oldugundan ve PATH'e eklendiginden emin olun.
    echo.
    pause
    exit /b
)

echo Python bulundu.
echo.

echo Pip kontrol ediliyor...
py -m ensurepip --upgrade

echo.
echo Pip guncelleniyor...
py -m pip install --upgrade pip

echo.
echo Gerekli kutuphaneler yukleniyor...
py -m pip install pygame numpy matplotlib

echo.
echo requirements.txt dosyasindaki kutuphaneler yukleniyor...
py -m pip install -r requirements.txt

echo.
echo Yuklu paketler kontrol ediliyor...
py -m pip show pygame
py -m pip show numpy
py -m pip show matplotlib

echo.
echo Simulasyon baslatiliyor...
py visualization.py

echo.
echo Program kapatildi.
pause