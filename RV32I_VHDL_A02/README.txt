Things to add
* L1 cache
* Pipelined implementation
* 32-bit wide simulated external memory
* Memory-Mapped GPIO
* Boot from flash
* Test program using GPIO
* Example program which shows how the running program would look in C

How would the program look in C?

Address 0x1000 starts the GPIO configuration
GPIO start with an enable address, followed by a direction address, followed by a status address

Enable Address:
The enable address directly toggles whether the corresponding GPIO pin is enabled or not. When
the bit position is set to 1, the corresponding GPIO is enabled. Otherwise, it is disabled.

Direction Address:
The direction address specifies whether the pin is to be used as an input or an output. This is 
important to specify because it determines whether to drive the pin at low impedance or high impedance.
In other words, is the user driving the state of the pin or is its state being driven? A 0 in any given 
bit position sets the pin to output, and a 1 sets the pin to input.

Status Address:
The status address is the address directly mapped to the GPIO. When any given bit is set to input, 
the incoming signal is mapped directly to this address. Then set to output, values can be written to this
address to output occordingly.

For the sake of this program, we will assume the use of a HAL so that all memory is set accordingly. The 
structure of the main program is loosely based on the structure of an Arduino program.


---------------------- Program Start -----------------------

#include <math.h>
#include "ArtyA7_HAL.h"

void setup();
void loop();

void readInputs();
void clearLED();
void menu();
void play(int);
void win();
void lose();

typedef enum
{
    menu,
    starting,
    go,
    win,
    lose
} gameState;

int BTN0val, BTN1val, BTN2val, BTN3val, SW0val, SW1val, SW2val, SW3val;
int counter;
gameState state;



int main()
{
    setup()
    while(true)
    {
        loop()
    }
} 

void setup()
{
// Set the inputs
    pinMode(BTN0, INPUT);
    pinMode(BTN1, INPUT);
    pinMode(BTN2, INPUT);
    pinMode(BTN3, INPUT);
    pinMode(SW0, INPUT);
    pinMode(SW1, INPUT);
    pinMode(SW2, INPUT);
    pinMode(SW3, INPUT);
    
// Set the outputs
    pinMode(LED0_RED, OUTPUT);
    pinMode(LED1_RED, OUTPUT);
    pinMode(LED2_RED, OUTPUT);
    pinMode(LED3_RED, OUTPUT);
    pinMode(LED0_GREEN, OUTPUT);
    pinMode(LED1_GREEN, OUTPUT);
    pinMode(LED2_GREEN, OUTPUT);
    pinMode(LED3_GREEN, OUTPUT);
    pinMode(LED4, OUTPUT);
    pinMode(LED5, OUTPUT);
    pinMode(LED6, OUTPUT);
    pinMode(LED7, OUTPUT); 
}

void loop()
{
    menu();
    play();
}

void readInputs()
{
    BTN0val = readInput(BTN0);
    BTN1val = readInput(BTN1);
    BTN2val - readInput(BTN2);
    BTN3val = readInput(BTN3);
    SW0val = readInput(SW0);
    SW1val = readInput(SW1);
    SW2val = readInput(SW2);
    SW3val = readInput(SW3);
}

void menu()
{
    const int base = 2;
    int difficulty = 0;
    int bit0, bit1, bit2, bit3, displayCount;
    
// Set the game state    
    state = menu;

// Read the inputs
    readInputs();

// Calculate difficulty    
    bit0 = SW0val;
    bit1 = pow(base, 1) * SW1val; // 2^1 (=2) * (0 or 1) = 0 or 2;
    bit2 = pow(base, 2) * SW2val;
    bit3 = pow(base, 3) * SW2val;
    difficulty = bit0 + bit1 + bit2 + bit3;
    
// Update menu display | progressing white lights or rolling effect
    displayCount = count % 4;
    switch(displayCount)
    {
        case 0:
            clearLED();
            writeOutput(LED7, 1);
            break;
        case 1:
            clearLED();
            writeOutput(LED6, 1);
            break;
        case 2:
            clearLED();
            writeOutput(LED5, 1);
            break;
        case 3:
            clearLED();
            writeOutput(LED4, 1);
            break;
    }
    count++;

// If play button pressed, play game
    if(BTN0) play(difficulty);
}

void play(difficulty)
{
    double delayMultiplyer = pow(0.9, difficulty);
    double delay = 0.5 * delayMultiplier // seconds
    int startingTime = 2;
    
    state = starting
    
// flash the red lights 3 times, then solid green
// If you press before green, you lose
// If you press after green but before bright lights, you win
// If you press after bright lights, you lose
    while(true)
    {
        // Determine the state
        // The waiting state lasts 2 seconds then the state advances to go
        // The go state lasts for the duration of the delay, or until the player presses the button. Whichever comes first.
        // The next state is either the win state or lose state. The rules of the game determine which you enter. Each lasts 2 seconds
        // Finally, the loop breaks and you are returned to the menu state
        // Read the inputs
        readInputs();
        // update state
    }
    
}

----------------------- Program End -------------------------    