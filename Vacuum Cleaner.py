#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import *
import threading


myLock = threading.Lock()

mA = LargeMotor('outA')
mB = LargeMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')
ts1 = TouchSensor('in1') #"Connect a touch sensor to sensor port 1" North bumper
assert ts1.connected
ts2 = TouchSensor('in2') #"Connect a touch sensor to sensor port 2" South bumper
assert ts2.connected
ts3 = TouchSensor('in3') #"Connect a touch sensor to sensor port 3" East bumper
assert ts3.connected
ts4 = TouchSensor('in4') #""Connect a touch sensor to sensor port 4" West bumper
assert ts4.connected
btn = Button()

NSLock = threading.Lock()
EWLock = threading.Lock()


def driveControlNS():

	global driveNS
	#driveNS=ts.value()

	while True:
		sleep(.1)
		NSLock.acquire(True)
	
		if (driveNS>0):
		#Driving North
		mA.run_forever(speed_sp=150)
		mB.run_forever(speed_sp=150)
		elif(driveNS<0):
		#Driving South	
		mA.run_forever(speed_sp=-150)
		mB.run_forever(speed_sp=-150)
		NSLock.release()
		


def driveControlEW():
	global driveEW
	#drivenEW=ts.value()
	while True:
		sleep(.1)
		EWLock.acquire(True)
		
		if (driveEW>0):
		#Driving East
		mC.run_forever(speed_sp=150)
		mD.run_forever(speed_sp=150)
		elif(driveEW<0)
		#Driving West
		mC.run_forever(speed_sp=-150)
		mD.run_forever(speed_sp=-150)
		EWLock.release()

def vacuumControl():
	global driveEW
	global driveNS

	while (ts3.value()==0): #While East bumper is not pressed

		while (ts1.value()==0): #While north bumper is not pressed
			driveNS=1
			driveControlNS()

		if (ts1.value()==1):
			
			driveNS=0 
			NSLock.acquire(True) #Inside this lock, make the robot stop
			mA.stop(stop_action='brake') # then brake
			mB.stop(stop_action='brake')
			NSLock.release()
			
			driveEW=1 #Positive: Moving East
			sleep(1) #Wait for the vacuum to move slightly east for 1 second

			driveEW=0
			mC.stop(stop_action='brake') # then brake
			mD.stop(stop_action='brake')
			sleep(1)

			#NSLock.acquire(True)
			driveNS=-1 #Move South
			#NSLock.release()

		

		elif (ts2.value()==1) ##When the South bumper is Hit.
 
			driveNS=0 
			NSLock.acqurie(True) #Inside this lock, make the robot stop
			mA.stop(stop_action='brake') # then brake
			mB.stop(stop_action='brake')
			NSLock.release()

			driveEW=1 #Drive slightly East
			mC.stop(stop_action='brake') # then brake
			mD.stop(stop_action='brake')
			sleep(1) #Wait for the vacuum to move slightly east for 1 second

			#NSLock.acquire(True)
			driveNS=1 #Move North
			#NSLock.release()
		
			

	if(ts3.value()==1): #Out of the firstloop, if robot Bumped to East Wall! in the end. Yay!

		while(ts4.value()==0): #When West bumper is not hit

			if (ts1.value()==1): #If north bumper is pressed (Now the robot is in NorthEast corner)
				driveNS=0 
				NSLock.acqurie(True) #Inside this lock, make the robot stop
				mA.stop(stop_action='brake') # then brake
				mB.stop(stop_action='brake')
				NSLock.release()

				driveNS=-1 #After stop, move south

				#while(ts2.value==0):  #Move South until the South Bumper is pressed

					#driveEW=-1#Negative: Moving West

				if(ts2.value==1): #If south bumper is hit 
					driveNS=0
					NSLock.acqurie(True)
					mA.stop(stop_action='brake') # Stop moving South
					mB.stop(stop_action='brake')
					NSLock.release()

				driveEW=1 #Move WEST back to original position
			
			elif (ts2.value()==1): ##If the robot is in [SouthEastern corner]
				EWLock.acquire(True)	
				driveEW=-1 #Moving West

		
		#STOP EVERYTHING if West bumper is HIT		
		driveNS=0		
		NSLock.acquire(True)
		mA.stop(stop_action='brake') # end if West bumper ts4 is bumped.
		mB.stop(stop_action='brake')
		NSLock.release()
		driveEW=0
		EWLock.acquire(True)
		mC.stop(stop_action='brake') 
		mD.stop(stop_action='brake')
		EWLock.release()

driveNS_thread= threading.Thread(target=driveControlNS)
driveEW_thread= threading.Thread(target=driveControlEW)
Vacuum_thread=threading.Thread(target=vacuumControl)

driveNS_thread.start()
driveEW_thread.start()
Vacuum_thread.start()

driveNS_thread.join()
driveEW_thread.join()
Vacuum_thread.join()






		



		
			

			








	
		

