#define AppName "Duct"
#define ExeName "Duct"    
#define AppId 'E14EE998-7025-4FC4-8FAE-53E1E0C6D24B'  
#define AppVersion = '0.0.1'
#define AppPublisher "Nathan Rath"
#define AppURL "https://github.com/IronicPickle/duct"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{{#AppId}}                                                            
AppName={#AppName}
AppVersion={#AppVersion}
;AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}                                               
DefaultGroupName={#AppName}
SetupIconFile=".\dist\duct\images\icon.ico"                                                                                   
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename={#AppName} Setup                                                                                               
Compression=lzma
SolidCompression=yes
WizardStyle=modern
CloseApplications=no
OutputDir=".\output\{#AppVersion}"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: ".\dist\duct\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#ExeName}.exe"; WorkingDir: "{app}"
Name: "{group}\{#AppName} Background"; Filename: "{app}\{#ExeName}.exe"; WorkingDir: {app}; Parameters: "--launch-background"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

procedure TaskKill(FileName: String);
var
  ResultCode: Integer;
begin
    Exec(ExpandConstant('taskkill.exe'), '/F /IM ' + '"' + FileName + '"', '', SW_HIDE,
     ewWaitUntilTerminated, ResultCode);
end;

function GetUninstallString(): string;
var
  sUnInstPath: string;
  sUnInstallString: String;
begin
  Result := '';
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{{{#AppId}}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function CheckOldInstall(): Boolean;
var
  V: Integer;
  ResultCode: Integer;
  sUnInstallString: string;
begin
  Result := True;
  if RegValueExists(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\{{#AppId}}_is1', 'UninstallString') then
  begin
    sUnInstallString := GetUninstallString();
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Pos('DW Piper', sUnInstallString) <> 0 then 
    begin
      MsgBox(ExpandConstant('In order to install this update, we must remove the previous installation. Press OK to continue.'), mbInformation, MB_OK);
      Result := Exec(ExpandConstant(sUnInstallString), '', '', SW_SHOW, ewWaitUntilTerminated, ResultCode);   
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  TaskKill('{#ExeName}.exe');
  TaskKill('DW-Piper.exe');
  Result := CheckOldInstall();
end;

[Run]
Filename: "schtasks"; \
    Parameters: "/CREATE /F /SC ONLOGON /TN ""Duct"" /TR ""'{app}\{#ExeName}.exe' --launch-background"""; \
    Flags: runhidden
Filename: "{app}\{#ExeName}"; \
    Parameters: "--launch-background"; \
    Flags: runhidden nowait runasoriginaluser

[UninstallRun]
Filename: "schtasks"; \
    Parameters: "/DELETE /F /TN ""Duct"""; \
    Flags: runhidden
Filename: "taskkill"; \
    Parameters: "/F /IM ""{#ExeName}.exe"""; \
    Flags: runhidden