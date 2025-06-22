#include <AccelStepper.h>

// Stepper motors (STEP, DIR)
AccelStepper stepperU(1, 13, 12);   // Up
AccelStepper stepperD(1, 3, 2);     // Down
AccelStepper stepperF(1, 5, 4);     // Front
AccelStepper stepperB(1, 7, 6);     // Back
AccelStepper stepperL(1, 9, 8);     // Left
AccelStepper stepperR(1, 11, 10);   // Right

// Steps per 90-degree turn
#define STEPS_PER_90_DEG 50 

String inputCommand = "";

void setup() {
  Serial.begin(115200);
  Serial.println("Rubik's Cube Stepper Controller Ready.");
  Serial.println("Enter move string (e.g. UDBFLRRL2UBD3R2U):");

  // Set max speed and acceleration
  stepperU.setMaxSpeed(5000); stepperU.setAcceleration(5000);
  stepperD.setMaxSpeed(5000); stepperD.setAcceleration(5000);
  stepperF.setMaxSpeed(5000); stepperF.setAcceleration(5000);
  stepperB.setMaxSpeed(5000); stepperB.setAcceleration(5000);
  stepperL.setMaxSpeed(5000); stepperL.setAcceleration(5000);
  stepperR.setMaxSpeed(5000); stepperR.setAcceleration(5000);
}

void moveMotor(AccelStepper &motor, int steps) {
  motor.move(steps);
  while (motor.distanceToGo() != 0) {
    motor.run();
  }
}

void processMoves(String command) {
  command.trim();
  Serial.print("Processing: "); Serial.println(command);

  for (int i = 0; i < command.length(); i++) {
    char move = command[i];
    int steps = STEPS_PER_90_DEG;

    // If next character is '2' or '3', apply the multiplier
    if (i + 1 < command.length()) {
      char nextChar = command[i + 1];
      if (nextChar == '2') {
        steps *= 2;
        i++;
      } else if (nextChar == '3') {
        steps *= 3;
        i++;
      }
    }

    switch (move) {
      case 'U': moveMotor(stepperU, steps); break;
      case 'D': moveMotor(stepperD, steps); break;
      case 'F': moveMotor(stepperF, steps); break;
      case 'B': moveMotor(stepperB, steps); break;
      case 'L': moveMotor(stepperL, steps); break;
      case 'R': moveMotor(stepperR, steps); break;
      default:
        Serial.print("Invalid move: "); Serial.println(move);
    }
  }

  Serial.println("Done. Enter another move string:");
}

void loop() {
  if (Serial.available()) {
    inputCommand = Serial.readStringUntil('\n');
    processMoves(inputCommand);
  }
}
