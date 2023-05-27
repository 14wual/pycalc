[Setup]
AppName=PyCalc
AppVersion=1.0
DefaultDirName={pf}\PyCalc
DefaultGroupName=PyCalc
OutputDir=output

[Files]
Source: "README.md"; DestDir: "{app}"
Source: "LICENSE"; DestDir: "{app}"
Source: "__init__.py"; DestDir: "{app}"
Source: "pycalc\windows.py"; DestDir: "{app}\pycalc"
Source: "pycalc\linux.py"; DestDir: "{app}\pycalc"
Source: "pycalc\src\config.ini"; DestDir: "{app}pycalc\src"
Source: "pycalc\src\images\*"; DestDir: "{app}pycalc\src\images"
Source: "pycalc\src\log\*"; DestDir: "{app}pycalc\src\log"

[Run]
Filename: "{app}\pycalc.exe"; Description: "Your Python GUI Calculator"

[Code]
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Result := '';

  { Install pip packages }
  Exec('"{app}\Scripts\pip.exe"', 'install customtkinter==5.1.3 pyperclip==1.8.2 Pillow==9.5.0 plyer==2.1.0', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  if ResultCode <> 0 then
  begin
    Result := 'Error installing pip packages.';
    Exit;
  end;

  { Add python path to system PATH }
  Exec('cmd.exe', '/C setx PATH "%PATH%;{app}\Scripts" > NUL', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  if ResultCode <> 0 then
  begin
    Result := 'Failed to add python path to system PATH.';
    Exit;
  end;
end;