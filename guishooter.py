#######################################
## Bogentimer mit GPIO - Ansteuerung ##
## v0.8 - 12.11.2016 - by mpoe       ##
#######################################

#Bibliotheken einbinden
import RPi.GPIO as GPIO			# Ansteuerung der GPIO-Pins
import time						# Zeitmodul
import tkinter as tk			# GUI-Modul
import tkinter.font as tkfont	# Fonts in der GUI
from PIL import Image			# Grafiken in der GUI
import _thread as thread		# Threading-Modul


#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#Warnungen ausschalten
GPIO.setwarnings(False)

#Font definieren

#GPIO Pin Belegung, Zahl ist die GPIO-PIN-Nr. auf dem Raspi
ROT = 18
GELB = 24
GRUEN = 22
PIEZO = 23
TASTER = 26

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(ROT, GPIO.OUT) 								#rot
GPIO.setup(GELB, GPIO.OUT) 								#gelb
GPIO.setup(GRUEN, GPIO.OUT) 							#gruen
GPIO.setup(PIEZO, GPIO.OUT) 							#piepser
GPIO.setup(TASTER, GPIO.IN, pull_up_down=GPIO.PUD_UP) 	#Taster

# alles abschalten
GPIO.output(PIEZO, False)
GPIO.output(ROT, False)
GPIO.output(GELB, False)
GPIO.output(GRUEN, False)

# Globals definieren
VORBEREITUNGK = 4		# Zeit in Sek. für die "rote" Phase im Kurzprogramm
SCHIESSENK = 4			# Zeit in Sek. für die "gruene" Phase im Kurzprogramm - Achtung: addiert mit WARNUNGK ergibt das die Gesamtschiesszeit !!!
WARNUNGK = 2			# Zeit in Sek. für die "orangene" Phase im Kurzprogramm 
ENDEZEITK = 2			# Zeit in Sek. zur "Abkuehlzeit" nach dem Schiessen

VORBEREITUNGL = 8		# Zeit in Sek. für die "rote" Phase im Langprogramm
SCHIESSENL = 8			# Zeit in Sek. für die "gruene" Phase im Langprogramm - Achtung: addiert mit WARNUNGK ergibt das die Gesamtschiesszeit !!!
WARNUNGL = 4			# Zeit in Sek. für die "orangene" Phase im Langprogramm
ENDEZEITL = 4			# Zeit in Sek. zur "Abkuehlzeit" nach dem Schiessen

state = 1				# Variable für die Statusabfrage beim Programmwechsel in den Threads
abbruchwert = 0			# 0 = alles normal , 1 = sofort das Schiessprogramm beenden
abbruchzeit = 5			# Zeit in Sek. für die Wartezeit in Rot nach einem Abbruch des Schiessens
warteblink = 0.3		# Intervall in Sek für das Blinken in der Warteschleife

def beep(beepcount):					# Piepsen definieren
	while beepcount>0:
		GPIO.output(PIEZO, True)
		time.sleep(0.3)
		GPIO.output(PIEZO, False)
		time.sleep(0.2)
		beepcount -= 1

def warte1sek(wartecount):				# 1 Sekunde warten
	while wartecount>0:
		time.sleep(1)
		wartecount -=1
		if abbruchwert == 1:
			abbruchanzeige()
			thread.exit()
			break

def abbruchanzeige(): 					# den angeforderten sofortigen Abbruch anzeigen und ausführen!
	print(abbruchwert)
	GPIO.output(ROT, True)
	GPIO.output(GELB, False)
	GPIO.output(GRUEN, False)
	beep(3)
	#warte1sek(abbruchzeit)
	global abbruchwert
	abbruchwert = 0
	print("geaendert: ", abbruchwert)
	thread.exit()
	#thread.abort(kurz)
	
def shortbeep(beepcount):				# Kurzes Piepsen definieren
	while beepcount>0:
		GPIO.output(PIEZO, True)
		time.sleep(0.05)
		GPIO.output(PIEZO, False)
		time.sleep(0.02)
		beepcount -= 1

def Warteschleife(): 					# Lauflicht signalisiert die Startbereitschaft
	# print("Warteschleife")
	GPIO.setmode(GPIO.BOARD)
	GPIO.output(ROT, True)
	time.sleep(warteblink)
	GPIO.output(ROT, False)
	#time.sleep(warteblink)
	GPIO.output(GRUEN, True)
	time.sleep(warteblink)
	GPIO.output(GRUEN, False)
	#time.sleep(warteblink)
	GPIO.output(GELB, True)
	time.sleep(warteblink)
	GPIO.output(GELB, False)

def shootingkurz():						# Kernprogramm Ampelablauf mit "kurzen" Zeiten
	print("Schiess-Zyklus 'kurz' gestartet ! Status=",state)
	#print("Zeiten in Sek.: ", VORBEREITUNGK,SCHIESSENK,WARNUNGK,ENDEZEITK)
	#Phase 2 - Vorbereitungsphase
	beep(2)
	GPIO.output(ROT, True)
	GPIO.output(GELB, False)
	GPIO.output(GRUEN, False)
	print("Vorbereitungs-Phase in Sek.: ",VORBEREITUNGK)
	warte1sek(VORBEREITUNGK)

	#Phase 3 - normales Schiessen
	beep(1)
	GPIO.output(GRUEN, True)
	GPIO.output(ROT, False)
	GPIO.output(GELB, False)
	print("Schiessen-Phase in Sek.: ",SCHIESSENK)
	warte1sek(SCHIESSENK)

	#Phase 4 - Schiessen mit Warnung
	GPIO.output(GELB, True)
	GPIO.output(GRUEN, False)
	print("Warn-Phase in Sek.: ",WARNUNGK)
	warte1sek(WARNUNGK)
	beep(3)
	print("Ende des Schiess-Zyklus .... Pfeile holen, ",ENDEZEITK," Sek.")
	#zurueck zu Phase 1 - Schluss und Pfeile holen
	GPIO.output(ROT, True)
	GPIO.output(GELB, False)
	GPIO.output(GRUEN, False)
	warte1sek(ENDEZEITK)
	print("Bitte neuen Zyklusstart auslösen, Programm wechseln oder ENDE")

def shootinglang():						# Kernprogramm Ampelablauf mit "langen" Zeiten
	print("Schiess-Zyklus 'lang' gestartet ! Status=",state)
	beep(2)
	GPIO.output(ROT, True)
	GPIO.output(GELB, False)
	GPIO.output(GRUEN, False)
	print("Vorbereitungs-Phase in Sek.: ",VORBEREITUNGL)
	warte1sek(VORBEREITUNGL)

	#Phase 3 - normales Schiessen
	beep(1)
	print("Schiessen-Phase in Sek.: ",SCHIESSENL)
	GPIO.output(GRUEN, True)
	GPIO.output(ROT, False)
	GPIO.output(GELB, False)
	warte1sek(SCHIESSENL)

	#Phase 4 - Schiessen mit Warnung
	print("Warn-Phase in Sek.: ",WARNUNGL)
	GPIO.output(GELB, True)
	GPIO.output(GRUEN, False)
	warte1sek(WARNUNGL)
	beep(3)
	print("Ende des Schiess-Zyklus .... Pfeile holen, ",ENDEZEITL," Sek.")
	#zurueck zu Phase 1 - Schluss und Pfeile holen
	GPIO.output(ROT, True)
	GPIO.output(GELB, False)
	GPIO.output(GRUEN, False)
	warte1sek(ENDEZEITL)
	print("Bitte neuen Zyklusstart auslösen, Programm wechseln oder ENDE")

def sofortabbruch():
	global abbruchwert
	abbruchwert = 1

def kurzthread():						# Status setzen und Thread starten
	global state
	state = 2
	print("Statusänderung:", state)
	thread.start_new_thread(kurz,(),)	# neuen Thread starten, damit die GUI noch aktiv und ansprechbar bleibt!

def langthread():						# Status setzen und Thread starten
	global state
	state = 3  							# den Wert state aendern, damit Aenderungen über die GUI bemerkt werden!
	print("Statusänderung:", state)
	thread.start_new_thread(lang,(),)	# neuen Thread starten, damit die GUI noch aktiv und ansprechbar bleibt!

def kurz():
	print("Kurzes Programm gewaehlt....")
	shortbeep(3)
	while state == 2:
		#Phase 1 - Warten auf Tastendruck"
		Warteschleife()
		#Status des Tasters einlesen
		tasterStatus = GPIO.input(TASTER)	#Status des Tasters einlesen
		if (tasterStatus):
			time.sleep(0.1)
		else:
			time.sleep(0.1)
			shootingkurz()

def lang():


	print("Langes Programm gewaehlt....")
	shortbeep(3)
	while state == 3:
		#Phase 1 - Warten auf Tastendruck
		Warteschleife()
		tasterStatus = GPIO.input(TASTER) 	#Status des Tasters einlesen
		if (tasterStatus):
			time.sleep(0.1)
		else:
			time.sleep(0.1)
			shootinglang()

#Endlosschleife

root = tk.Tk()

class GUI1:								# Fenster für die GUI definieren und starten
	def __init__(self, master):

		background = tk.PhotoImage(file="/home/pi/python/images/bg800.gif")
		background_image=tk.PhotoImage("/home/pi/python/images/bg800.gif")
		self.master = master
		#self.master.geometry("800x450")
		master.attributes('-fullscreen', True)
		master.title("Bogentimer v0.8")		# Titel des Fensters

		self.background = tk.Label(master, image=background)
		background.image = background
		self.background.place(x=0, y=0, relwidth=1, relheight=1)

		# Überschrift über den Buttons:

		self.label1 = tk.Label(master, text="  --== BMW-Bogenschützen ==--  ", font="Helvetica 25 bold", bg="black", fg="medium spring green")
		self.label1.grid(row=0, columnspan=5)

		# Überschrift über den Buttons:
		self.label1 = tk.Label(master, text="   Bitte den Turniermodus waehlen:    ", font="Helvetica 20")
		self.label1.grid(row=1, columnspan=5)

		# Überschrift über den Buttons:
		self.label1 = tk.Label(master, text="", font="Helvetica 2")
		self.label1.grid(row=2, columnspan=2)

		#Button 1 (ENDE)
		self.close_button = tk.Button(master, text="ENDE", command=master.quit, height = 5, width = 12, bg="orange", fg="black", activebackground="firebrick", relief="raised", font="Helvetica 14 bold")
		self.close_button.grid(row=6, column=2)
		
		#Button 1 (SCHIESS-STOP)
		self.close_button = tk.Button(master, text="SOFORT-\nABBRUCH", command=sofortabbruch, height = 5, width = 12, bg="red", fg="black", activebackground="firebrick", relief="raised", font="Helvetica 14 bold")
		self.close_button.grid(row=6, column=1)
		
		

		#Button 2 (KURZ - 120s)
		self.kurz_button = tk.Button(master, text="KURZ\n'Liga'\n120s", command=kurzthread, height = 7, width = 12, bg="pale green", fg="black", activebackground="green", relief="raised", font="Helvetica 14 bold")
		self.kurz_button.grid(row=4, column=0)

		# Überschrift über den Buttons:
		self.label1 = tk.Label(master, text="", font="Helvetica 2")
		self.label1.grid(row=5, columnspan=2)

		
		#Button 3 (LANG - 240s)
		self.lang_button = tk.Button(master, text="LANG\n'FITA'\n240s", command=langthread, height = 7, width = 12, bg="cyan", fg="black", activebackground="blue", relief="raised", font="Helvetica 14 bold")
		self.lang_button.grid(row=4, column=1)
		
		#path = "/home/pi/python/images/bmw200.jpg"

		#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
		logo = tk.PhotoImage(file="/home/pi/python/images/bmw200.gif")

		#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
		self.label2 = tk.Label(master, image = logo)
		self.label2.image = logo
		#The Pack geometry manager packs widgets in rows or columns.
		self.label2.grid(row=6, column=0)
		
		self.label3 = tk.Label(master, text="", font="Helvetica 6")
		self.label3.grid(row=7, column=0)
		
		self.label3 = tk.Label(master, text="Version 0.8 (c) M.Pöschl, 2016", font="Helvetica 6")
		self.label3.grid(row=8, column=0)

my_gui = GUI1(root)


root.mainloop()
    
GPIO.cleanup()
print("Programm Ende")
