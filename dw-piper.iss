#define AppName "DW Piper"
#define ExeName = "DW-Piper"
#define AppPublisher "Nathan Rath"
#define AppURL "https://github.com/IronicPickle/dw-piper"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E14EE998-7025-4FC4-8FAE-53E1E0C6D24B}                                                              
AppName={#AppName}
AppVersion={#AppVersion}
;AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}                                               
DefaultGroupName={#AppName}
SetupIconFile=".\dist\dw\images\icon.ico"                                                                                   
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
Source: ".\dist\dw\{#ExeName}.exe"; DestDir: "{app}"; Flags: ignoreversion; \
    BeforeInstall: TaskKill('{#ExeName}.exe')
Source: ".\dist\dw\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; \

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

[Run]
Filename: "schtasks"; \
    Parameters: "/CREATE /F /SC ONLOGON /TN ""DW Piper"" /TR ""'{app}\{#ExeName}.exe' --launch-background"""; \
    Flags: runhidden
Filename: "{app}\{#ExeName}"; \
    Parameters: "--launch-background"; \
    Flags: runhidden nowait runasoriginaluser

[UninstallRun]
Filename: "schtasks"; \
    Parameters: "/DELETE /F /TN ""DW Piper"""; \
    Flags: runhidden
Filename: "taskkill"; \
    Parameters: "/F /IM ""{#ExeName}.exe"""; \
    Flags: runhidden