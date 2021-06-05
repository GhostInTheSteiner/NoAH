; Project-Bin
xProjectBinCenter := 690
yProjectBinCenter := 536

; Scroll after offset
yProjectBinCenterOffset := 350

; Master-Button
xMasterButton := 1174
yMasterButton := 149

; Timeline Top-Area
xTimelineTopArea = 983 
yTimelineTopArea = 102
wTimelineTopArea = 600
hTimelineTopArea = 20

; Height of track
hTrack = 70

; Mouse Position at track
yCurrentTrack := xTimelineTopArea + hTimelineTopArea + hTrack / 2
xCurrentTrack := 0

binFocused := False
timelineFocused := True



; Functions

CursorToTimeline() {
;   global xTimelineTopArea
;   global yTimelineTopArea
;   global wTimelineTopArea
;   global hTimelineTopArea
;   global yCurrentTrack

;   PixelSearch, x, y, xTimelineTopArea, yTimelineTopArea, xTimelineTopArea + wTimelineTopArea, yTimelineTopArea + hTimelineTopArea, 0xEFF0F1, 2, Fast
;   MouseMove x + 3, yCurrentTrack, 0
}

BinScrollDown() {
	global yProjectBinCenter
	global yProjectBinCenterOffset

	MouseGetPos x, y

	if (y + 100 < (yProjectBinCenter + yProjectBinCenterOffset))
	{
		MouseMove 0, 100, 0, R
	}
	else
	{
		Send {WheelDown}
	}
}

BinScrollUp() {
	global yProjectBinCenter
	global yProjectBinCenterOffset

	MouseGetPos x, y

	if (y - 100 > (yProjectBinCenter - yProjectBinCenterOffset))
	{
		MouseMove 0, -100, 0, R
	}
	else
	{
		Send {WheelUp}
	}
}




; Script

SetTitleMatchMode 2

#IfWinActive fps - Kdenlive

$3::
if (binFocused)
{
	BinScrollDown()
	BinScrollDown()
	BinScrollDown()
	BinScrollDown()
}
else if (timelineFocused)
{
	SendInput 3
	Sleep 100
	CursorToTimeline()
}
else
	SendInput 3
return

$2::
if (binFocused)
{
	BinScrollUp()
	BinScrollUp()
	BinScrollUp()
	BinScrollUp()
}
else if (timelineFocused)
{
	SendInput 2
	Sleep 100
	CursorToTimeline()
}
else
	SendInput 2
return

$4::
SendInput, 4
CursorToTimeline()
return

$1::
SendInput, 1
CursorToTimeline()
return

t::
if (binFocused)
{
	MouseGetPos, x, y
	MouseClickDrag, L, x, y, xCurrentTrack, yCurrentTrack
	Click
	timelineFocused := True
	binFocused := False
}
else
	Send t
return

e::
if (binFocused)
{
	BinScrollDown()
}
else
	Send e
return

w::
if (binFocused)
{
	BinScrollUp()
}
else
	Send w
return

r::
if (binFocused)
{
	MouseGetPos, x, y
	MouseClick, L, x, y
}
else
	Send r
return

q::
SendInput {Home}

FileRead, content, TRANSFORM.txt
Clipboard := content
Send ^!v
return

F1::
FileRead, content, WIPE_IN.txt
Clipboard := content
Send ^v
return

F4::
FileRead, content, WIPE_OUT.txt
Clipboard := content
Send ^v
return

~Esc::
if (binFocused)
{
  binFocused := False
  timelineFocused := True
  CursorToTimeline()
  Click
}
else
{
  binFocused := False
  timelineFocused := False
}
return

F2::
SendInput {Right}
SendInput {Home}
SendInput 4

;Loop 4
;{
;	SendInput {Right}
;}

SendInput r
SendInput 2
SendInput {Home}

FileRead, content, FADE_IN.txt
Clipboard := content
Send ^!v
return

F3::
; Loop 4
; {
; 	SendInput {Right}
; }

; SendInput e

SendInput {Left}
SendInput {Home}
SendInput 1
SendInput {Left}

SendInput r

FileRead, content, FADE_OUT.txt
Clipboard := content
Send ^!v
return

^::
SendInput {Home}
return