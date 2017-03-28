# Software Interface

The xl-320 servos use a half duplex uart serial interface to send packets
of back and forth between the servo and the controlling computer.

## Packet Basics

|Header                  | ID | Length        | Instruction | Parameter                     | CRC |
|------------------------|----|---------------|-------------|-------------------------------|-----|
| [0xFF, 0xFF, 0xFD, 0x00] | ID | [LEN_L, LEN_H] | INST | [PARAM 1, PARAM 2, ..., PARAM N] | [CRC_L, CRC_H] |

Packet format:

[0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]

- Header: 0xFF, 0xFF, 0xFD
- Reserved byte: 0x00
- Servo ID: ID
- Packet Length: Len_l, len_h
- Instruction: INST
- Parameters: Param 1 ... Param N
- CRC: crc_l, crc_h

A status packet back from the servo follows the same format, but the instruction
is always `0x55` and maybe followed by error codes if something is wrong.
The length of the packet is aways the entire length minus header, id, and crc.
Also remember, the packets are little-endian, so place numbers in the packet
as `[LSB, MSB]`. You can use the function `le()` in `Packet` to accomplish
this. You can also use `word()` to reverse `le()`.

See the references below for more details on the instructions, error codes, etc.

## Packet Constructors

There are basic several packet constructors:

- `makePacket(ID, instr, reg=None, params=None)` - The most generic and the basis for everything
- `makeWritePacket(ID, reg, params=None)` - Makes a packet that writes to a servo register
- `makeReadPacket(ID, reg, params=None)` - Makes a packet that contains an instruction to read from a servo register
- `makePingPacket(ID)` - Makes a packet with the ping instruction in it, forcing servos to repond and let you know what servos are available
- `makeResetPacket(ID, param)` - Makes a packet to reset a servo to its factory default condition ... **becareful**
- `makeRebootPacket(ID)` - Makes a packet that forces a servo to reboot

Now the funciton params are:

- ID - servo ID number
- instr - instruction
- reg - either the RAM or EEPROM register you are writing to or reading from
- params - the packet parameters, some packets have optional parameters

Beyond this, there are more specialized packet constructors for things I use the most.
Some examples are:

- `makeServoIDPacket(curr_id, new_id)` - Sets a servo to a new ID ... **becareful**
- `makeServoPacket(ID, angle)` - Commands a servo to a specified `angle`
- `makeLEDPacket(ID, color)` - Lights up the servo's LED to the specified `color`

I keep adding more, so take a look in the `pyxl320.Packet` folder to see what is already
done for you.


# References:

Unfortunately the Dynamixel references below are **not written well** (many typos
and errors throughout), so please be careful or you will drive yourself crazy trying to fix bugs.
Also they have disappeared on me, so if you get a `404` error, hopefully the docs
will come back.

- [XL-320 e-Manual](http://support.robotis.com/en/techsupport_eng.htm#product/actuator/dynamixel_x/xl_series/xl-320.htm)
- [XL-320 hardware and half duplex circuit](http://support.robotis.com/en/product/actuator/dynamixel_x/xl-series_main.htm)
- [Dynamixel Protocol Ver. 2](http://support.robotis.com/en/product/actuator/dynamixel_pro/communication/instruction_status_packet.htm)
- [PySerial](http://pyserial.readthedocs.io/en/latest/index.html)

---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>
