#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import sys
import time
import wave
import contextlib
import pyexcel_ods

from types import SimpleNamespace
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip



####################################################
# 				Konfiguration				       #
####################################################
textAreaSize = 						(2000, 230)
multiParagraphHeight =				500
upscaleFactor =						2

customOffsetTop =					30
customOffsetLeft =					350

customOffsetTopMultiParagraph =		30
customOffsetLeftMultiParagraph =	100

lineMargin =						50

fadeInSpeed = 						40
fadeOutSpeed = 						60
framerate =							30
waitingTime =						15

fontPath =							"/home/gits/Dokumente/Dark Sky/PyTextbox/fonts/NotoSans.otf"
fontSize =							30
textColor = 						(0, 0, 0)

scriptPath =						"../script_resources/Fools_2_End.ods"
voiceTrackResourcesFolder =			"../voice_track_resources/Fools_2_End/"

customOutputFolder =				"/home/gits/Dokumente/Dark Sky/PyTextbox/animated_text/vv8/"

indexPositions =					10































#offset: Benutzerdefinierter Abstand in Config
#margin: Zusätzlicher, dynamisch definierter Abstand durch Code
def initFadeInOptions(param_margin = (0, 0), param_textBase = None, nameIndicatorImage = None, isMultiParagraph = False):
	global textAreaSize, textColor, fontPath, fontSize, fadeInSpeed, lineMargin, waitingTime, upscaleFactor, customOffsetTop, customOffsetLeft, framerate



	if isMultiParagraph:
		textAreaSizeUpscaled = (textAreaSize[0] * upscaleFactor, multiParagraphHeight * upscaleFactor)

		offsetTop = customOffsetTopMultiParagraph
		offsetLeft = customOffsetLeftMultiParagraph

		maxLineWidth = textAreaSizeUpscaled[0] - offsetLeft * 4 * upscaleFactor

		fontSizeFinal = int(fontSize * 1.2)

	else:
		textAreaSizeUpscaled = (textAreaSize[0] * upscaleFactor, textAreaSize[1] * upscaleFactor)

		offsetTop = customOffsetTop
		offsetLeft = customOffsetLeft

		maxLineWidth = textAreaSizeUpscaled[0] - offsetLeft * 2 * upscaleFactor

		fontSizeFinal = fontSize



	marginTop = param_margin[1]



	if param_textBase == None:		textBase = Image.new('RGBA', textAreaSizeUpscaled, (textColor[0], textColor[1], textColor[2], 0))
	else:							textBase = param_textBase



	return SimpleNamespace(
		textOverlay = 			Image.new('RGBA', textAreaSizeUpscaled, (textColor[0], textColor[1], textColor[2], 0)), #muss weg
		textBase = 				textBase,
		nameIndicatorImage =	nameIndicatorImage,
		upscaleFactor = 		upscaleFactor,
		font = 					ImageFont.truetype(fontPath, fontSizeFinal * upscaleFactor),
		maxLineWidth = 			maxLineWidth,
		waitingTime = 			waitingTime,
		speed =					fadeInSpeed,
		framerate =				framerate,
		lineMargin =			lineMargin,

		lineCoordinates = [
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*2),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*3),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*4),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*5),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*6),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*7),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*8),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*9),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*10),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*11),
			(offsetLeft*upscaleFactor, offsetTop*upscaleFactor + marginTop + lineMargin*upscaleFactor*12)
		]
	)

def initFadeOutOptions(param_lastFrame, param_scriptParagraphIndex, param_characterIndex, param_upscaleFactor, param_lastLineCoordinates):
	global fadeOutSpeed

	return SimpleNamespace(

		lastFrame = 					param_lastFrame,
		scriptParagraphIndex =			param_scriptParagraphIndex,
		characterIndex =				param_characterIndex,
		speed =							fadeOutSpeed,
		upscaleFactor =					param_upscaleFactor,
		lastLineCoordinates = 			param_lastLineCoordinates

	)




def fadeInParagraph(scriptParagraph, fadeInOptions):	
	#Lokale Variablen
	currentTextLine = 					""
	previousTextLine = 					""

	currentCharacterIndex = 			0

	currentLineCoordinatesIndex = 		0

	currentLineCoordinates = 			(0, 0)
	previousLineCoordinates =			(0, 0)

	currentTextWithNextWord =			""
	currentTextWithNextWordWidth = 		0

	remainingScriptParagraphWords =		scriptParagraph.text.split(" ")
	remainingScriptParagraphWords.pop	(0)



	for character in scriptParagraph.text + "          ":
		####################################################
		# 				Set Up der Daten			       #
		####################################################

		#aktuelle Textzeile mit aktuellen Character appenden
		currentTextLine += 			character

		#drawingManager initialisieren => drawingManager basiert IMMER auf textOverlay!
		drawingManager = 			ImageDraw.Draw(fadeInOptions.textOverlay)

		#Schauen ob nächstes Wort noch in die Zeile passt...
		if character == " " and len(remainingScriptParagraphWords) > 0:
			currentTextWithNextWord = 			currentTextLine + remainingScriptParagraphWords.pop(0)
			currentTextWithNextWordWidth =		drawingManager.textsize(currentTextWithNextWord, fadeInOptions.font)[0]


		
		#Zweig wird nur einmal bei Zeilenwechsel betreten, gleichzeitig muss sich im character ein Leerzeichen befinden
		if currentTextWithNextWordWidth > fadeInOptions.maxLineWidth:
			#Neuesten Character entfernen
			currentTextLine =					currentTextLine[:-1]

			#Text überschreitet Textarea => currentLineCoordinatesIndex erhöhen
			currentLineCoordinatesIndex += 		1

			#Aktuelle Textzeile sichern => alte muss weiter gezeichnet werden!
			previousTextLine = 					currentTextLine

			#currentTextLine wieder leeren um Platz zu machen für den Inhalt der nächsten Zeile
			currentTextLine = 					""

			#Zurücksetzen von currentTextWithNextWordWidth
			currentTextWithNextWordWidth = 		0



		#Koordinaten der aktuellen und letzten Textzeile setzen
		if True:                                currentLineCoordinates 		= 		fadeInOptions.lineCoordinates[currentLineCoordinatesIndex]
		if currentLineCoordinatesIndex > 0:		previousLineCoordinates 	= 		fadeInOptions.lineCoordinates[currentLineCoordinatesIndex - 1]




		####################################################
		# 				Verarbeiten der Daten			   #
		####################################################

		#Name-Indicator hinzufügen (Bild sollte bereits Transparenz haben)
		if fadeInOptions.nameIndicatorImage != None and currentCharacterIndex < 30:
			nameIndicatorImageUpscaled = 		fadeInOptions.nameIndicatorImage.resize((fadeInOptions.textBase.width, fadeInOptions.textBase.height), Image.ANTIALIAS)
			fadeInOptions.textBase = 			Image.alpha_composite(fadeInOptions.textBase, nameIndicatorImageUpscaled)

		#Zweig wird immer aufgerufen, wenn eine vorhergehende Textzeile existiert => Vorherige Zeile noch weiter Zeichnen
		if len(previousTextLine) > 0:		renderText(drawingManager, previousLineCoordinates, previousTextLine, (255, 255, 255, fadeInOptions.speed), fadeInOptions.font)

		#Text mit Transparenz zu textOverlay hinzufügen
		renderText							(drawingManager, currentLineCoordinates, currentTextLine, (255, 255, 255, fadeInOptions.speed), fadeInOptions.font)
		fadeInOptions.textBase = 			Image.alpha_composite(fadeInOptions.textBase, fadeInOptions.textOverlay)

		#Größe des downscaled Bildes ermitteln
		textBase = 							fadeInOptions.textBase
		textBaseSizeDownscaled =			(int(textBase.size[0] / fadeInOptions.upscaleFactor), int(textBase.size[1] / fadeInOptions.upscaleFactor))

		#textOverlay in /dev/shm/sequence/ speichern
		saveImage							(textBase, "/dev/shm/sequence/image_" + convertToLetters(scriptParagraph.index) + "_" + convertToLetters(currentCharacterIndex) + ".png", textBaseSizeDownscaled)

		#Index des aktuellen Characters erhöhen
		currentCharacterIndex +=	 		1



	#Legt die Zeit fest, in der der Text angezeigt wirdcurrentCharacterIndex
	currentCharacterIndex =				extendToWaitingTime(scriptParagraph.index, currentCharacterIndex, fadeInOptions.waitingTime)

	return initFadeOutOptions(fadeInOptions.textBase, scriptParagraph.index, currentCharacterIndex, fadeInOptions.upscaleFactor, currentLineCoordinates)




def fadeOutParagraph(fadeOutOptions):
	transparentImage = 			Image.new('RGBA', fadeOutOptions.lastFrame.size, (0, 0, 0, 0))

	if fadeOutOptions.speed > 0:
		for currentAlphaValue in range(255, -1, -fadeOutOptions.speed):
			fadedFrame =							Image.blend(fadeOutOptions.lastFrame, transparentImage, 1 - currentAlphaValue / 255)

			#Größe des downscaled Bildes ermitteln und damit speichern
			fadedFrameSizeDownscaled =				(int(fadedFrame.size[0] / fadeOutOptions.upscaleFactor), int(fadedFrame.size[1] / fadeOutOptions.upscaleFactor))
			saveImage								(fadedFrame, "/dev/shm/sequence/image_" + convertToLetters(fadeOutOptions.scriptParagraphIndex) + "_" + convertToLetters(fadeOutOptions.characterIndex) + ".png", fadedFrameSizeDownscaled)

			fadeOutOptions.characterIndex +=		1

	return fadeOutOptions


def animateParagraphs(scriptPath):
	sessionFolderName = "videos_version_" + str(len(os.listdir("../animated_text")))

	os.system("rm /dev/shm/voice_tracks/*.wav")
	os.system("rm /dev/shm/sequence/*.png")
	os.system("rm /dev/shm/animated_text_temp/to_be_stretched.mov")

	os.system("mkdir /dev/shm/voice_tracks")
	os.system("mkdir /dev/shm/sequence")
	os.system("mkdir /dev/shm/animated_text_temp")
	os.system("mkdir ../animated_text")
	os.system("mkdir ../animated_text/" + sessionFolderName)
	
	os.system("shnsplit -f " + voiceTrackResourcesFolder + "*.cue " + voiceTrackResourcesFolder + "*.wav -d /dev/shm/voice_tracks")
	os.system("cp /dev/shm/voice_tracks/*.wav ../voice_tracks")



	clearSequenceFolder()

	nameIndicatorImageDictonary = getNameIndicators()
	voiceTrackList = getVoiceTracks()



	currentScriptParagraphIndex = 0
	currentScriptParagraphCoordinates = (0, 0)  #Koordinaten des aktuellen Paragraphs (wenn mehrere Paragraphen "appended" werden)

	lastFrame = None



	scriptParagraphList = pyexcel_ods.get_data(scriptPath)["Paragraphs"]
	hasSelection = checkSelection(scriptParagraphList)



	for scriptParagraphRecordCurrent in scriptParagraphList:
		#Zuweisen des nächsten Paragraphen
		scriptParagraphRecordNext = scriptParagraphList[currentScriptParagraphIndex + 1]

		####################################################
		# 			Parsen von Paragraph-Argumenten		   #
		####################################################

		#Standard: Leerer Name => Keine Nameplate anzeigen!
		scriptParagraphName =			""

		#Standard: Keine Voiced-Line
		voiceTrack = 					None

		#nameInidcatorImage grundsätzlich mit None initialisieren => Standard: Keine Nameplate anzeigen!
		nameIndicatorImage = 			None

		#Standard: Kein Appenden
		toBeAppendedNext = 				False
		toBeAppendedCurrent = 			False



		#Verarbeiten der Felder
		if len(scriptParagraphRecordCurrent) > 0:
			#Zuweisen den Character-Namens an scriptParagraphName
			scriptParagraphName = 			scriptParagraphRecordCurrent[0]

		if len(scriptParagraphRecordCurrent) > 1:
			#Zuweisen der eigentlichen Textzeile an SciptParagraphText
			scriptParagraphText = 			scriptParagraphRecordCurrent[1]

		if len(scriptParagraphRecordCurrent) > 2 and scriptParagraphRecordCurrent[2] == 1 and len(voiceTrackList) > 0:
			#Zuweisen des Voiced-Line-Flag Wertes an voiceTrack
			voiceTrack = 					voiceTrackList.pop()

		if len(scriptParagraphRecordCurrent) > 3 and scriptParagraphRecordCurrent[3] == 1:
			#Zuweisen des Append-Flag-Wertes an toBeAppendedCurrent
			toBeAppendedCurrent =			True
			scriptParagraphName =			""

		if len(scriptParagraphRecordNext) > 3:
			#Zuweisen des Append-Flag-Wertes an toBeAppendedNext
			toBeAppendedNext = 				scriptParagraphRecordNext[3] == 1



		if hasSelection:
			#Verarbeiten des Selection-Flags => Nur rendern wenn gesetzt!
			if len(scriptParagraphRecordCurrent) > 4 and scriptParagraphRecordCurrent[4] == 1:
				pass
			else:
				currentScriptParagraphIndex += 1
				continue



		#Nur wenn Name UND nameplate definiert soll auch eine Nameplate angezeigt werden
		if len(scriptParagraphName) > 0 and scriptParagraphName in nameIndicatorImageDictonary.keys():
			nameIndicatorImage = 			nameIndicatorImageDictonary[scriptParagraphName]

		#Für den Fall, dass unbeabsichtigte Whitespaces vorhanden sind => entfernen
		#Außerdem: Standard-Anführungszeichen durch "schönere" Anführungszeichen ersetzen
		scriptParagraphText = scriptParagraphText.lstrip().replace("\"", "“", 1).replace("\"", "”", 1)






		####################################################
		# 				  Appenden managen				   #
		####################################################

		if toBeAppendedCurrent:
			#Dieser Paragraph wird appended
			scriptParagraph =						SimpleNamespace(text = scriptParagraphText, index = currentScriptParagraphIndex, voiceTrack = voiceTrack)

			fadeInOptions = 						initFadeInOptions(currentScriptParagraphCoordinates, lastFrame, nameIndicatorImage, True)
			fadeOutOptions = 						fadeInParagraph(scriptParagraph, fadeInOptions)

			if toBeAppendedNext:
				#Nächster Paragraph wird appended
				lastFrame =								fadeOutOptions.lastFrame
				currentScriptParagraphCoordinates = 	(fadeOutOptions.lastLineCoordinates[0], fadeOutOptions.lastLineCoordinates[1] + fadeInOptions.lineMargin * 1.5 * fadeInOptions.upscaleFactor)

			else:
				#Nächster Paragraph wird ersetzt
				fadeOutParagraph						(fadeOutOptions)

				lastFrame =								None
				currentScriptParagraphCoordinates = 	(0, 0)

		else:
			#Dieser Paragraph ersetzt den vorherigen
			scriptParagraphText = 					scriptParagraphText.rstrip()
			currentScriptParagraphCoordinates = 	(0, 0)
			scriptParagraph =						SimpleNamespace(text = scriptParagraphText, index = currentScriptParagraphIndex, voiceTrack = voiceTrack)
			fadeInOptions = 						initFadeInOptions(nameIndicatorImage = nameIndicatorImage)

			fadeOutOptions =						fadeInParagraph(scriptParagraph, fadeInOptions)
			fadeOutParagraph						(fadeOutOptions)






		####################################################
		# 				   Video erstellen				   #
		####################################################

		#MOV-Video erstellen und erstmal im Arbeitsspeicher ablegen...
		os.system("ffmpeg -r " + str(fadeInOptions.framerate) + " -f image2 -i /dev/shm/sequence/%*.png -vcodec png /dev/shm/animated_text_temp/to_be_stretched.mov")

		#...dann die ffmpeg Filter-Einstellungen ermitteln...
		if scriptParagraph.voiceTrack == None:		stretchFilter = ""
		else:										stretchFilter = '-filter:v "setpts=' + str(round(scriptParagraph.voiceTrack.length, 3) / getVideoLength("/dev/shm/animated_text_temp/to_be_stretched.mov") * 1.004) + '*PTS"'

		#...und, nachdem die Länge bekannt, ist an diese anpassen und im endgültigen Ausgabe-Ordner abspeichern
		os.system("ffmpeg -i /dev/shm/animated_text_temp/to_be_stretched.mov " + stretchFilter + " -vcodec png ../animated_text/" + sessionFolderName + "/" + convertToLetters(currentScriptParagraphIndex) + ".mov")

		if len(sys.argv) >= 2 and sys.argv[1] == "-c":
			os.system("yes | cp ../animated_text/" + sessionFolderName + "/*.mov '" + customOutputFolder + "'")

		#Jetzt noch die Ordner aufräumen...
		os.system("rm /dev/shm/sequence/*.png")
		os.system("rm /dev/shm/animated_text_temp/to_be_stretched.mov")






		####################################################
		# 				Iteration abschließen			   #
		####################################################

		#Nächste Iteration vorbereiten
		currentScriptParagraphIndex += 			1
		






#Hilfs-Funktionen

def clearSequenceFolder():
	folder = "/dev/shm/sequence"

	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)



def convertToLetters(digits):
	definedDigits = str(digits)
	prefixDigits = "0"*(indexPositions - len(definedDigits))

	letters = "".join(list(map(lambda letter:
		chr(int(letter) + 65)
	, prefixDigits + definedDigits)))

	return letters




def saveImage(image, fileName, scaledSize):
	image.resize((scaledSize), Image.ANTIALIAS).save(fileName, "PNG")




def getNameIndicators():
	nameIndicatorImageDictonary = {}
	nameIndicatorsPath = "../name_indicators"

	for fileName in os.listdir(nameIndicatorsPath):
		if os.path.isfile(os.path.join(nameIndicatorsPath, fileName)) and fileName.endswith(".png"):
			nameIndicatorImageDictonary[fileName[:-4]] = Image.open(os.path.join(nameIndicatorsPath, fileName))

	return nameIndicatorImageDictonary



def getMostRecentFilePath(path, format):
	list_of_files = glob.glob(path + "*." + format)
	return max(list_of_files, key=os.path.getctime)



#Erstellt Kopien eines durch paragraphIndex und characterIndex angegebenen Bildes, deren Anzahl durch waitingTime bestimmt wird
def extendToWaitingTime(paragraphIndex, characterIndex, waitingTime):
	for characterIndex in range(characterIndex, characterIndex + waitingTime):
		lastImage = "/dev/shm/sequence/image_" + convertToLetters(paragraphIndex) + "_" + convertToLetters(characterIndex - 1) + ".png"
		nextImage = "/dev/shm/sequence/image_" + convertToLetters(paragraphIndex) + "_" + convertToLetters(characterIndex) + ".png"

		os.system("cp " + lastImage + " " + nextImage)

	return characterIndex



def getVoiceTracks():
	voiceTrackList = []
	voiceTracksPath = "/dev/shm/voice_tracks"

	for fileName in os.listdir(voiceTracksPath):
		if os.path.isfile(os.path.join(voiceTracksPath, fileName)) and fileName.endswith(".wav"):
			voiceTrackPath = os.path.join(voiceTracksPath, fileName)

			voiceTrackList.append(SimpleNamespace(path = voiceTrackPath, length = getWaveAudioLength(voiceTrackPath)))

	return voiceTrackList



def getWaveAudioLength(path):
	with contextlib.closing(wave.open(path,'r')) as f: 
		frames = f.getnframes()
		rate = f.getframerate()
		length = frames / float(rate)    
	
	return length



def getVideoLength(filePath):
	return VideoFileClip(filePath).duration



def renderText(drawingManager, coordinates, text, color, font):
	#(255, 255, 255, fadeInOptions.speed), fadeInOptions.font
	offsetLeft = 0

	for character in text:
		coordinatesCurrentCharacter = (coordinates[0] + offsetLeft, coordinates[1])
		
		drawingManager.text(coordinatesCurrentCharacter, character, color, font)
		offsetLeft += font.getsize(character)[0]

def checkSelection(scriptParagraphList):
	for scriptParagraphRecord in scriptParagraphList:
		if len(scriptParagraphRecord) > 4 and scriptParagraphRecord[4] == 1:
			return True

	return False

#Einsprungpunkt
animateParagraphs				(scriptPath)
