@echo off

title AstralSim installer v1.0.2

rem Installieren der benötigte Python-Bibliotheken

type doh.txt

echo Checking for neweset pip Version
py -m pip install --upgrade pip
echo Installing tkinter...
py -m pip install tkinter
echo Installing customtkinter...
py -m pip install customtkinter
echo Installing numpy...
py -m pip install numpy
echo Installing json...
py -m pip install json
echo Installing os...
py -m pip install os

cls
type doh.txt

echo Installing math...
py -m pip install math
echo Installing datetime...
py -m pip install datetime
echo Installing matplotlib.pyplot...
py -m pip install matplotlib.pyplot
echo Installing matplotlib...
py -m pip install matplotlib
echo Installing CTkListbox...
py -m pip install CTkListbox
echo Installing customtkinter...
py -m pip install customtkinter
echo Installing subprocess...
py -m pip install subprocess


cls
type dohii.txt

echo
echo -
echo Installation abgeschlossen!
echo Installer schliesst automatisch in 10s
echo -

timeout /t 10
exit
