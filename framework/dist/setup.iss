; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{11ED8FB9-5932-4ECF-8968-5CFCC313735B}
AppName=Cuphead_run
AppVersion=1.5
;AppVerName=Cuphead_run 1.5
AppPublisher=HSJ
AppPublisherURL=http://www.example.com/
AppSupportURL=http://www.example.com/
AppUpdatesURL=http://www.example.com/
DefaultDirName={pf}\Cuphead_run
DisableProgramGroupPage=yes
OutputDir=C:\Users\Han seong-jae\Desktop
OutputBaseFilename=Cuphead_setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Han seong-jae\Desktop\2d\framework\dist\mygame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Han seong-jae\Desktop\2d\framework\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Cuphead_run"; Filename: "{app}\mygame.exe"
Name: "{commondesktop}\Cuphead_run"; Filename: "{app}\mygame.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\mygame.exe"; Description: "{cm:LaunchProgram,Cuphead_run}"; Flags: nowait postinstall skipifsilent

