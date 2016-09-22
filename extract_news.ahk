#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#z::
IfWinExist Live News Main@thinkorswim
{
	LastClickX = 35
	LastClickY = 87
	WinActivate Live News Main@thinkorswim
	WinMaximize Live News Main@thinkorswim
	Click 35, 87
	sleep 2000
	Loop 120 {
		Send ^c
		Run Notepad
		WinActivate Untitled - Notepad
		sleep 2000
		WinMaximize Untitled - Notepad
		Send ^v
		WinActivate Live News Main@thinkorswim
		Send {Right}
		Send ^c
		WinActivate Untitled - Notepad
		Send {space}
		Send ^v
		WinActivate Live News Main@thinkorswim
		Click 365, 457
		Send ^a
		Send ^c
		sleep 2000
		WinActivate Untitled - Notepad
		Send ^v
		sleep 2000
		Click 1916, 71
		sleep 2000
		Click 14, 63
		Send {shift down}{end}{shift up}
		sleep 2000
		Send ^c
		Send ^s
		sleep 2000
		StringReplace, clipboard, clipboard, `/, - , All
		StringReplace, clipboard, clipboard, *, , All
		StringReplace, clipboard, clipboard, :, - , All
		Send ^v
		Click 675, 48
		Send Documents\GitHub\Stock-Research\AERI\News
		Send {Enter}
		sleep 2000
		Send !s
		WinActivate Live News Main@thinkorswim
		LastClickY += 20
		Click LastClickX, LastClickY
		Sleep 2000
	}
}
return

#c::
StringReplace, clipboard, clipboard, `/, - , All
StringReplace, clipboard, clipboard, *, , All
StringReplace, clipboard, clipboard, :, - , All

Escape::
ExitApp
Return