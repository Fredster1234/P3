import sqlite3
import random
import time
import Database
#import spidev


#initiate spi
#spi = spidev.SpiDev()
#spi.open(0, 1)
#spi.max_speed_hz = 10000000

#definitions
file_name='errors.db'
db = sqlite3.connect(file_name) # either create or open database
cursor = db.cursor()
#Actuators     =[0x96, 0x5F,0xFF,0xFF, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00]
#ActuatorsOn   =[0x96, 0x5F,0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF]
#ActuatorsOff  =[0x96, 0x5F,0xFF,0xFF, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00]

ActuatorsOn  =[0x96, 0x5F,0xFF,0xFF, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00]
Actuators    =[0x96, 0x5F,0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF]
ActuatorsOff =[0x96, 0x5F,0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF]

error_ID=1
speed = 1000/600 # conveyor speed cm/s

def actuator(cm,state,Actuators) :
    byte1 = 27-2*(11-cm)
    byte2 = 26-2*(11-cm)
    if state is 1:
        Actuators[byte1] = 0x00
        Actuators[byte2] = 0x00
    elif state is 0:
        Actuators[byte1] = 0xFF
        Actuators[byte2] = 0xFF


#check for conveyor speed to be constant (manually by input in keyboard or digitally)

start = time.clock()
cursor.execute("SELECT * FROM errors")
c=cursor.fetchall()
print(c)
while 1:
    db = sqlite3.connect(file_name) # either create or open database
    cursor = db.cursor()
    cursor.execute('''SELECT X, Y, status FROM errors WHERE id=?''', (error_ID,))
    e = cursor.fetchone()
    db.close()
    while e is None:
        db = sqlite3.connect(file_name) # either create or open database
        cursor = db.cursor()
        cursor.execute('''SELECT X, Y, status FROM errors WHERE id=?''', (error_ID,))
        e = cursor.fetchone()
        #print("waiting fo data")
        db.close()

    errors, IDs, a=Database.sort(error_ID,file_name)
    print("actuate at:",a+0.5,"now at:",speed*(time.clock()-start))

    #write actuators into array
    for error in errors:
        actuator(error,1,Actuators)
        print("added error", error)
        print("ActuatorsIn", Actuators)
    print("ActuatorsOut", Actuators)

    #wait for position to actuate
    while speed*(time.clock()-start+0.03) <= a+0.5: #+0.5 because we cut the position instead of rounding. when we mark at a and one error lies at a+ >0.5 we are too a away from it
        0
    print(a+0.5,speed*(time.clock()-start),"Print now")
    print(time.clock())
    #spi.writebytes(Actuators)
    time.sleep(0.03)
    #spi.writebytes(ActuatorsOff)
    print(time.clock())
    print(a+0.5,speed*(time.clock()-start),"marked")

    print(Actuators)

    #reset actuator array
    Actuators     = [0x96, 0x5F,0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF, 0xFF,0xFF]
    print("RESET",Actuators)

    #write status in database (later also time since start, time, date )
    for ID in IDs:
        db = sqlite3.connect(file_name) # either create or open database
        cursor = db.cursor()
        cursor.execute('''UPDATE errors SET status = ? WHERE id = ? ''',(1, ID))
        print("0 to 1 for ID", ID)
        db.commit()
        db.close()

    #set new ID to look at in database
    error_ID = IDs[-1]+1 #last elemt of array

    #db = sqlite3.connect(file_name) # either create or open database
    #cursor = db.cursor()
    #cursor.execute("SELECT * FROM errors")
    #c=cursor.fetchall()
    #print(c)
