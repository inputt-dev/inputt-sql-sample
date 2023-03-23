from Inputt import Inputt
from Globals import Globals
from workerthreads import threads, workerThread, stopWatchStart, stopWatchStop, stopWatchStartTime
from DBThread import DB
import random
import sqlite3
import time
import datetime
import cv2

inputt = Inputt() #Start the interface
db = DB("db.db",'4') #Start the database manager
DB_File_Path = "db.db"
Globals.set("DB filename", DB_File_Path)
Globals.set("db", db)

"""
Define the menu option functions
"""
#[] Root menu
def root(): #Show running threads
	ret = []
	runningThreads = threads.iterable()
	for rt in runningThreads:
		ret.append(str(rt))
	return ret

#1. Select * from the table
def Select():
	selected = db.select_all()
	print(selected)
	return [str(selected)]

#2. Insert a new data row into the table
class Insert_Thread(workerThread):
	def __init__(self, *args, **kwargs):
		super(Insert_Thread, self).__init__(*args, **kwargs)
		self.count = 0 #How many inserts are done
		self.P.set("db", args[2])
	def __str__(self):
		return "{} inserts done".format(self.count)
	def run(self):
		db = self.P.get("db")
		self.count = 0
		while self.count < 2500 and self.stopped() == False:
			values = db.generate_random_record()
			sql = "INSERT INTO TEST VALUES(?,?,?,?);"
			index = db.addCommand(sql,values)
			self.P.set("output_Text", str(self))
			self.count += 1
			time.sleep(.1)
			
#Check if an insert thread is running, if not create it
def Insert():
	Inserting = Insert_Thread("Insert", inputt.menuLevel, db)
	Inserting.start()
	ret = str(Inserting)
	return [ret]

#3. Randomly update a row with random information
class Update_Thread(workerThread):
	def __init__(self, *args, **kwargs):
		super(Update_Thread, self).__init__(*args, **kwargs)
		self.count = 0 #How many inserts are done
		self.P.set("db", args[2])

	def __str__(self):
		return "{} updates done".format(self.count)
	def run(self):
		db = self.P.get("db")
		self.count = 0
		while self.count < 2500 and self.stopped() == False:
			values = db.generate_random_record()
			values = list(values)
			values[1] = "Updated"
			values = tuple(values)
			record = db.get_random_record()
			sql = "UPDATE TEST SET ID = ?, NAME = ?, DATA = ?, VALUE = ? WHERE ID = ? AND NAME = ? AND DATA = ? AND VALUE = ?;"
			values = values + record
			index = db.addCommand(sql, values)
			self.P.set("output_Text", str(self))
			self.count += 1
			time.sleep(.1)
def Update():
	#Select an existing record, at random.  
	#Get a list of the IDS and pick one at random
	Updating = Update_Thread("Updating", inputt.menuLevel, db)
	Updating.start()
	ret = str(Updating)
	return [ret]

class Delete_Thread(workerThread):
	def __init__(self, *args, **kwargs):
		super(Delete_Thread, self).__init__(*args, **kwargs)
		self.count = 0 #How many inserts are done
		self.P.set("db", args[2])

	def __str__(self):
		return "{} deletes done".format(self.count)
	def run(self):
		db = self.P.get("db")
		self.count = 0
		while self.count < 2500 and self.stopped() == False:
			values = db.get_random_record()
			sql = "DELETE FROM TEST WHERE ID = ? AND NAME = ? AND DATA = ? AND VALUE = ?;"
			index = db.addCommand(sql, values)
			self.P.set("output_Text", str(self))
			self.count += 1
			time.sleep(.1)
def delete():
	Deleting = Delete_Thread("Deleting", inputt.menuLevel, db)
	Deleting.start()
	ret = str(Deleting)
	return [ret]


#4. Initialize database, from the file with the create table code
def database_utilities():
	Inserting = threads.get("Insert")
	return [str(Inserting)]

def Reset_database():
	db = sqlite3.connect(DB_File_Path)
	with open("create_db.sql", 'r') as sql_file:
			sql_script = sql_file.read()

	cursor = db.cursor()
	cursor.executescript(sql_script)
	db.commit()
	ret = []
	ret.append("Database file {} reset".format(DB_File_Path))
	ret.append("Table created {}".format(sql_script))
	return ret

def test_and_config():
	return ["Test the speed and configure the interface"] 

stopWatchStartTime = 0
def stopWatchStart():
	global stopWatchStartTime
	curr_dt = datetime.datetime.now()
	stopWatchStartTime = curr_dt.timestamp()
def stopWatchStop():
	global stopWatchStartTime
	curr_dt = datetime.datetime.now()
	stopWatchEndTime = curr_dt.timestamp()
	return stopWatchEndTime - stopWatchStartTime

def speed_test():
	#Generate a random screen and redraw it as soon as possible
	
	cols = 80
	rows = int(cols*9/16)
	inputt.gui.setFontSize(19)
	inputt.gui.resize(cols,rows)
	stopWatchStart()
	cursor_row = 0
	cursor_col = 0
	frames = 0
	draws = 100
	while frames < draws:
		inputt.gui.updatingBuffer(True)
		while cursor_row < rows:
			while cursor_col < cols:
				bg_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
				fg_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
				text = chr(random.randrange(0,255))
				inputt.gui.addToBuffer(cursor_col, cursor_row, text, fg_color = fg_color, bg_color = bg_color)
				cursor_col += 1
			cursor_row += 1
			cursor_col = 0
		cursor_row = 0
		inputt.gui.updatingBuffer(False)
		while inputt.gui.bufferUpdated == True:
			pass
		frames += 1
	t = stopWatchStop()
	text = "{} draws in {} seconds. FPS = {}".format(draws,t,int(draws/t))
	print(text)
	return [text]

def set_default_colors():
	return ["Set default text color for text(forground)", "Set default background color, when not set by special text"]

def set_foreground_color():
	color = inputt.getColor(inputt.gui.fg_color)
	inputt.gui.fg_color = color
	inputt.gui.bufferUpdated = True
	return ["Foreground color set to {}".format(color)]

def set_background_color():
	color = inputt.getColor(inputt.gui.bg_color)
	inputt.gui.bg_color = color
	inputt.gui.bufferUpdated = True
	return ["Background color set to {}".format(color)]

"""
Define the menu hierarchy and supply the functions that go with each
"""
inputt.addMenuItem([], name = "DB workerthread", func = root)
inputt.addMenuItem(['1'], name = "Select", func = Select)
inputt.addMenuItem(['2'], name = "Insert", func = Insert)
inputt.addMenuItem(['3'], name = "Update", func = Update)
inputt.addMenuItem(['4'], name = "Delete", func = delete)
inputt.addMenuItem(['5'], name = "database utilities", func = database_utilities)
inputt.addMenuItem(['5', '1'], name = "Reset database", func = Reset_database)
inputt.addMenuItem(['t'], name = "Test and Config", func = test_and_config)
inputt.addMenuItem(['t', '1'], name = "Speed Test", func = speed_test)
inputt.addMenuItem(['t', '2'], name = "Set default colors", func = set_default_colors)
inputt.addMenuItem(['t', '2', '1'], name = "Set default background color", func = set_background_color)
inputt.addMenuItem(['t', '2', '2'], name = "Set default foreground color", func = set_foreground_color)


inputt.startGui()

#The inputt main loop update menu to show current state, process the current menu item, and get the next line of input
while True:
	db.flush_command_buffer()
	output = inputt.outputProcessed()
	if inputt.endProgram:
		break
	userInput = inputt.nextLine()

#Shut down the running threads
runningThreads = threads.iterable()
for rt in runningThreads:
	rt.stop()
				
