// 7-Segment-Countdown with external triggers using the sparkfun large digit driver-Modules
 
//GPIO declarations
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
byte segmentLatch = 5;       //BUS-Ports for 7Segment
byte segmentClock = 6;
byte segmentData = 7;

const int buttonyel = 2;     // the number of the trigger pin
const int buttongre = 3;

const int yelPin =  13;      // the number of the LED pin
const int grePin =  12;
const int redPin =  11;

//definiere Zeiten:
const int lang = 240;        // time definitions in seconds
const int kurz = 120;
const int prepare = 10;

int stopstate = 0;
int counttime = 0;
int buttonStateyel = 0;      // variable for reading the pushbutton status
int buttonStategre = 0;
int x = 0;
int start = 0;



void setup()
{
  Serial.begin(9600);
  Serial.println("Outdevice Device is starting");
  pinMode(segmentClock, OUTPUT);
  pinMode(segmentData, OUTPUT);
  pinMode(segmentLatch, OUTPUT);
  pinMode(yelPin, OUTPUT);
  pinMode(grePin, OUTPUT);
  pinMode(redPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonyel, INPUT);
  pinMode(buttongre, INPUT);

  digitalWrite(segmentClock, LOW);
  digitalWrite(segmentData, LOW);
  digitalWrite(segmentLatch, LOW);

  showNumber(0);
  delay(2000);

}

void loop()
{
    //Serial.println("loop started");
    showNumber(0);
    delay(150);
    stopstate = 0;
    getStart();
    if (start == 1)
      {
      countDown();
      start = 0;
      }
    else return;
    
}


void getStop()
{
  // read the state of the pushbutton value:
  buttonStateyel = digitalRead(buttonyel);
  buttonStategre = digitalRead(buttongre);
   
    if (buttonStategre == HIGH && buttonStateyel == HIGH)
    {
      // STOP ausgelöst
      stopstate = 1;
      counttime = 0;
      //Serial.print("Stopstate: ");
      //Serial.println(stopstate); //for debugging
    }
    return;
} 



void getStart()
{
  // read the state of the pushbutton value:
  buttonStateyel = digitalRead(buttonyel);
  buttonStategre = digitalRead(buttongre);
   
    if (buttonStategre == HIGH && buttonStateyel == LOW)
    {
      // LANGES Programm ausgelöst
      counttime = 4 * lang; 
      //Serial.println("counttime lang"); //for debugging
      start = 1;
    }
    if (buttonStategre == LOW && buttonStateyel == HIGH)
    {
      // kurzes Programm ausgelöst
      counttime = 4 * kurz; 
      //Serial.println("counttime kurz"); //for debugging
      start = 1;
    }
    return;
} 


void showNumber(float value)   //Takes a number and displays the numbers. Displays absolute value (no negatives)
{
    int number = abs(value); //Remove negative signs and any decimals

    //Serial.print("number: ");
    //Serial.println(number);

    for (byte x = 0 ; x < 3 ; x++)
      {
      int remainder = number % 10;
      postNumber(remainder, false);
      //Serial.print("remainder: ");
      //Serial.println(remainder);
      number /= 10;
      }
      //Latch the current segment data
      digitalWrite(segmentLatch, LOW);
      digitalWrite(segmentLatch, HIGH); //Register moves storage register on the rising edge of RCK
}

  
void postNumber(byte number, boolean decimal)  //Given a number, or '-', shifts it out to the display
{
  //Serial.print("postNumber |");
  //    -  A
  //   / / F/B
  //    -  G
  //   / / E/C
  //    -. D/DP

  #define a  1<<0
  #define b  1<<6
  #define c  1<<5
  #define d  1<<4
  #define e  1<<3
  #define f  1<<1
  #define g  1<<2
  #define dp 1<<7

  byte segments;

  switch (number)
  {
    case 1: segments = b | c; break;
    case 2: segments = a | b | d | e | g; break;
    case 3: segments = a | b | c | d | g; break;
    case 4: segments = f | g | b | c; break;
    case 5: segments = a | f | g | c | d; break;
    case 6: segments = a | f | g | e | c | d; break;
    case 7: segments = a | b | c; break;
    case 8: segments = a | b | c | d | e | f | g; break;
    case 9: segments = a | b | c | d | f | g; break;
    case 0: segments = a | b | c | d | e | f; break;
    case ' ': segments = 0; break;
    case 'c': segments = g | e | d; break;
    case '-': segments = g; break;
  }

  if (decimal) segments |= dp;

  //Clock these bits out to the drivers
  for (byte x = 0 ; x < 8 ; x++)
    {
    digitalWrite(segmentClock, LOW);
    digitalWrite(segmentData, segments & 1 << (7 - x));
    digitalWrite(segmentClock, HIGH); //Data transfers to the register on the rising edge of SRCK
    }
}


void countDown()

  {
  //Serial.print("Start Countdown...");
  //Serial.print("prepare !");
  showNumber(prepare);
  delay(750);
  for (int prep = prepare * 4 ; prep > -1; prep--)
  {
    showNumber(prep/4); //Test pattern
    //Serial.println(prep); //For debugging
    delay(250);
    getStop();
    if (stopstate == 1)
      break;
  }
  showNumber(counttime/4);
  delay(750);
  //Serial.print("count !");
  for (int count = counttime; count > -1; count--)
  {
    showNumber(count/4); //Test pattern
    //Serial.print("counttime: ");
    //Serial.println(count); //For debugging
    delay(250);
    getStop();
    if (stopstate == 1)
      return;
  }
  return;
  
  start = 0;
  return;
  }
 // while (stopstate != 0);
 // return;
 // }
