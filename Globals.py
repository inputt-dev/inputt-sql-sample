from parameters import Parameters

Globals = Parameters({}) #Create a blank parameters object

def status():
	db = Globals.get("db")
	self.updateMenuItem([], "Database settings-{}".format(len(db.commands)))
	try:
		Inserting = threads.get("Insert")
		if Inserting.stopped() == True:
			onoff = "OFF"
		else:
			onoff = "ON"
		self.updateMenuItem(['2'], "Inserting is {} {}".format(onoff,Inserting.count))
	except Exception as e:
		self.updateMenuItem(['2'], "Inserting is OFF 0")
	try:
		Updating = threads.get("Update")
		if Updating.stopped() == True:
			onoff = "OFF"
		else:
			onoff = "ON"
		self.updateMenuItem(['3'], "Updating is {} {}".format(onoff,Inserting.count))
	except Exception as e:
		self.updateMenuItem(['3'], "Updating is OFF 0")		
	try:
		Deleting = threads.get("Delete")
		if Deleting.stopped() == True:
			onoff = "OFF"
		else:
			onoff = "ON"
		self.updateMenuItem(['4'], "Deleting is {} {}".format(onoff,Inserting.count))
	except Exception as e:
		self.updateMenuItem(['4'], "Deleting is OFF 0")