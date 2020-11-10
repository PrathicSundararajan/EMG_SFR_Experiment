 /* 
 Saving Values from Arduino to a .csv File Using Processing - Pseduocode
 Thing to set before running:
   Upload Arduino Sketch 
   Enter Correct Com Port 
   Choose a new filename
To View Excel File:
  Click on Sketch --> Show Sketch Folder 
  It will be in the data folder
To-Do: 
Figure out why can't run script continously multiple times
Maybe add automatic file reader
Misc Notes: 
If it says serial port is busy, unplug device and retry
  
 */

import processing.serial.*;
String fileName = "data/sfr1.csv";
//String portName = "/dev/cu.usbmodem14101"; //MAKE SURE TO CHANGE THIS TO YOUR PORT
String portName = "/dev/cu.wchusbserial1410"; 
int totalDesiredMinutesRecorded=1;

Serial myPort; //creates a software serial port on which you will listen to Arduino
Table table; //table where we will read in and store values. You can name it something more creative!
int numReadings = 500; //keeps track of how many readings you'd like to take before writing the file. 
int readingCounter = 0; //counts each reading to compare to numReadings. 
int startTimeMillis = -1;
int totalMicros;
float seconds;
int minutes;
void setup()
{
  //String portName = Serial.list()[1];
  table = new Table();
  myPort = new Serial(this, portName, 500000); //set up your port to listen to the serial port  
  myPort.clear();
  //the following are dummy columns for each data value. Add as many columns as you have data values. Customize the names as needed. Make sure they are in the same order as the order that Arduino is sending them!
  table.addColumn("id");
  table.addColumn("Total Microseconds");
  table.addColumn("Minute");
  table.addColumn("Seconds");
  table.addColumn("Value");
}
//1 min total
void serialEvent(Serial myPort) {
  try {
    String val = myPort.readStringUntil('\n'); //The newline separator separates each Arduino loop. We will parse the data by each newline separator. 
    if (val!= null) { //We have a reading! Record it.
        val = trim(val); //gets rid of any whitespace or Unicode nonbreakable space
        //println(val); //Optional, useful for debugging. If you see this, you know data is being sent. Delete if  you like. 
        float dataReadIn[] = float(split(val, ','));
        float currVal = dataReadIn[0];
        //println(val);  
        totalMicros = int(dataReadIn[1]);
        //println(totalMicros);
        seconds = (totalMicros / 1000000.0);
        println(seconds);
        minutes = (totalMicros / (1000000*60)) % 60;
        //println(minutes);         
        TableRow newRow = table.addRow();
        newRow.setInt("id", table.getRowCount() - 1);
        //println(seconds);
        //println("Data Read In: " + val + " & Calculated seconds: " + seconds);
        newRow.setInt("Minute", minutes);
        newRow.setFloat("Seconds", seconds);
        newRow.setInt("Total Microseconds", totalMicros);
        newRow.setFloat("Value", currVal);
        readingCounter++; //optional, use if you'd like to write your file every numReadings reading cycles
        if (totalDesiredMinutesRecorded == minutes)//The % is a modulus, a math operator that signifies remainder after division. The if statement checks if readingCounter is a multiple of numReadings (the remainder of readingCounter/numReadings is 0)
        {
        println("saved to " + fileName);
        saveTable(table, fileName); //Woo! save it to your computer. It is ready for all your spreadsheet dreams.
        exit();
        }
    }
  }
  catch(RuntimeException e) {
    e.printStackTrace();
  }
}

void draw()
{ 
  //visualize your sensor data in real time here! In the future we hope to add some cool and useful graphic displays that can be tuned to different ranges of values.
}
