#include <Servo.h>

using namespace std;

// pin definitions
#define pin_ee 6
#define pin_j1 11
#define pin_j2 10
#define pin_base 9

// Servo objects
Servo ee, j1, j2, base;

// define default pose
#define DE_TH_EE 130
#define DE_TH_J1 90
#define DE_TH_J2 90
#define DE_TH_BASE 0

// define max and min for end effector
#define EE_CLOSE_TH 100
#define EE_OPEN_TH 70

// define lengths of arm links
#define LINK1 13
#define LINK2 10.5

// functions to manipulate the arm
void default_pose(){
  write_pose(DE_TH_J1, DE_TH_J2, DE_TH_BASE);
  clutch_object();
}

void write_pose(float th_j1, float th_j2, float th_base){
  // straighten up
  j2.write(DE_TH_J2);
  j1.write(DE_TH_J1);
  delay(1000);

  // set pose
  base.write(th_base);
  delay(1000);
  j2.write(th_j2);
  j1.write(th_j1);
  delay(1000);
}

float *get_angles(float distance){
  // calculate angles
  float cos_th_j1 = (pow(LINK1, 2) + pow(LINK2, 2) - pow(distance, 2)) / (2 * LINK1 * LINK2);
  float cos_th_j2 = (pow(distance, 2) + pow(LINK2, 2) - pow(LINK1, 2)) / (2 * distance * LINK2);

  // debug
//  Serial.print("cos(th_j1): ");
//  Serial.print(cos_th_j1);
//  Serial.print(" cos(th_j2): ");
//  Serial.println(cos_th_j2);

  // convert angles into degrees and store in array
  float *angles = new float[2];
  angles[0] = acos(cos_th_j1) * 180 / PI;
  angles[1] = acos(cos_th_j2) * 180 / PI;

  // debug
//  Serial.print("angle-1: ");
//  Serial.print(angles[0]);
//  Serial.print(" angle-2: ");
//  Serial.println(angles[1]);

  // return array
  return angles;
}

void set_pose_from_coords(float x, float y){
  // calculate pose from co-ordinates
  float th_base = atan(y / x) * 180 / PI;
  float distance = sqrt( pow(x, 2) + pow(y, 2) );
  float *angles = get_angles(distance);
  float th_j1 = angles[0], th_j2 = angles[1];

  Serial.println("base angle: " + String(th_base) + " angle-1: " + String(th_j1) + " angle-2: " + String(th_j2));

  // write pose
  write_pose(th_j1, 180 - th_j2, th_base);
}

void clutch_object(){
  ee.write(EE_CLOSE_TH);
  delay(1000);
}

void release_object(){
  ee.write(EE_OPEN_TH);
  delay(1000);
}

void pick_and_place(float *coords){
  release_object();
  float pick_x = coords[0], pick_y = coords[1];
  float place_x = coords[2], place_y = coords[3];

  Serial.println("pickup initiated from (" + String(pick_x) + ", " + String(pick_y) + ")");
  set_pose_from_coords(pick_x, pick_y);
  clutch_object();
  Serial.println("pickup done");
  delay(1000);
  
  Serial.println("place initiated to (" + String(place_x) + ", " + String(place_y) + ")");
  set_pose_from_coords(place_x, place_y);
  release_object();
  Serial.println("place done");
  delay(1000);

  default_pose();
}

void setup() {
  pinMode(pin_ee, OUTPUT);
  pinMode(pin_j1, OUTPUT);
  pinMode(pin_j2, OUTPUT);
  pinMode(pin_base, OUTPUT);

  Serial.begin(9600);

  ee.attach(pin_ee);
  j1.attach(pin_j1);
  j2.attach(pin_j2);
  base.attach(pin_base);

  // default pose
  default_pose();
  delay(3000);

  Serial.println("enter coordinates");
}

// input storage
char input[50];
int pos=0;

void loop() {

  while(Serial.available()){
    char ch = Serial.read();
    delay(500);
    input[pos] = ch;
    pos++;
  }

  if(pos){
    Serial.println("processing input...");
    float coords[4];
    pos = 0;
    for(int i=0;i<4;i++){
      char str[10] = "";
      int temp= 0;
      while(input[pos] != ';'){
        if(isDigit(input[pos]) || input[pos] == '.'){
          str[temp] = input[pos];
        }
        temp++;
        pos++;
      }
      pos++;
      coords[i] = atof(str);
      delay(500);
    }

    pick_and_place(coords);
  
    Serial.println("enter coordinates");
    pos = 0;
  }
  
}

// 2.3;3.1;3;4;
