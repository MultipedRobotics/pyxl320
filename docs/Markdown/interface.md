# Hardware Interface

The xl-320 servos use a half duplex, single master, multi-slave
serial interface between all of the servos. There are multiple designs on the interweb
you can build (or buy) to connect a computer or microcontroller to the servos.

## Robotis Suggested

![](../../pics/circuit-old.png)

This uses a 74HC126 tri state buffer to interconnect the data line with a standard uart.
To switch betwen the Tx and Rx signals, a third signal (direction port) is used. In my
software, I use the `pyserial` RTS signal for the direction signal. **Unfortunately, 
not all USB serial interfaces breakout the RTS pin**

## Pixl

The [Poppy Project](https://www.poppy-project.org) designed an ingenious board call [Pixl](https://github.com/poppy-project/pixl)
that allows a standard uart (without the extra direction pin) to talk to the servos.
This is the hardware design I am currently using.

![](./pics/power-board.png)

I am currently using a 74AHCT126 tri-state buffer with a Vcc of 5V. I plan to find
a 3.3V buffer that is 5V tolerant (maybe 74LVX126) and remove my current need for
a logic level converter.

Now, this is more than an interface, it also produces all of the necessary voltages
(3.3V, 5V, and 7.5V) needed to talk to the servo. I use this one for debugging and
software development of `pyxl320` when I am on my Macbook. 
