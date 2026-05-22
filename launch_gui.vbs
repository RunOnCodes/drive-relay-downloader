Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Find the first .py file in the folder
Dim pyFile
For Each file In fso.GetFolder(scriptFolder).Files
    If LCase(fso.GetExtensionName(file.Name)) = "py" Then
        pyFile = file.Path
        Exit For
    End If
Next

If pyFile <> "" Then
    objShell.Run "pythonw """ & pyFile & """", 0, False
Else
    MsgBox "No Python (.py) file found in " & scriptFolder, 16, "Error"
End If