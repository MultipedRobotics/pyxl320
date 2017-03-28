##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

"""
This information is specific to Dynamixel's XL-320 servo motor.
http://support.robotis.com/en/product/dynamixel/xl-series/xl-320.htm
"""
# --------- INSTRUCTIONS -----
XL320_PING      = 0x01
XL320_READ      = 0x02
XL320_WRITE     = 0x03
XL320_REG_WRITE = 0x04
XL320_ACTION    = 0x05
XL320_RESET     = 0x06
XL320_REBOOT    = 0x08
XL320_STATUS    = 0x55
XL320_SYNC_READ  = 0x82
XL320_SYNC_WRITE = 0x83
XL320_BULK_READ  = 0x92
XL320_BULK_WRITE = 0x93

# -------- EEPROM -------------
XL320_MODEL_NUMBER    = 0
XL320_VER_FIRMWARE    = 2
XL320_ID              = 3
XL320_BAUD_RATE       = 4
XL320_DELAY_TIME      = 5
XL320_CW_ANGLE_LIMIT  = 6   # min angle, default 0
XL320_CCW_ANGLE_LIMIT = 8   # max angle, default 300
XL320_CONTROL_MODE    = 11  # joint or wheel mode, default joint (servo)
XL320_MAX_TORQUE      = 15
XL320_RETURN_LEVEL    = 17

# -------- RAM ----------------
XL320_TORQUE_ENABLE    = 24  # servo mode on/off - turn into wheel
XL320_LED              = 25
XL320_GOAL_POSITION    = 30
XL320_GOAL_VELOCITY    = 32
XL320_GOAL_TORQUE      = 35
XL320_PRESENT_POSITION = 37  # current servo angle
XL320_PRESENT_SPEED    = 39  # current speed
XL320_PESENT_LOAD      = 41  # current load
XL320_PESENT_VOLTAGE   = 45  # current voltage
XL320_PESENT_TEMP      = 46  # current temperature
XL320_MOVING           = 49
XL320_HW_ERROR_STATUS  = 50
XL320_PUNCH            = 51

# --------- OTHER -------------
XL320_RESET_ALL                  = 0xFF
XL320_RESET_ALL_BUT_ID           = 0x01
XL320_RESET_ALL_BUT_ID_BAUD_RATE = 0x02
XL320_LED_WHITE                  = 7
XL320_LED_BLUE_GREEN             = 6
XL320_LED_PINK                   = 5
XL320_LED_BLUE                   = 4
XL320_LED_YELLOW                 = 3
XL320_LED_GREEN                  = 2
XL320_LED_RED                    = 1
XL320_LED_OFF                    = 0
XL320_BROADCAST_ADDR             = 0xfe  # a packet with this ID will go to all servos
XL320_WHEEL_MODE                 = 1
XL320_JOINT_MODE                 = 2  # normal servo
XL320_9600                       = 0  # 0: 9600, 1:57600, 2:115200, 3:1Mbps
XL320_57600                      = 1
XL320_115200                     = 2
XL320_1000000                    = 3

# Conversions from values to strings for debugging

Baudrates = {
	0: '9.6 kbps',
	1: '57.6 kbps',
	2: '115 kbps',
	3: '1 Mbps'
}

Modes = {
	1: 'Wheel',
	2: 'Joint'
}

ReturnTypes = {
	0: 'No Return',
	1: 'Only Read',
	2: 'Return All'
}

LEDColors = {
	0: 'Off',
	1: 'Red',
	2: 'Green',
	3: 'Yellow',
	4: 'Blue',
	5: 'Pink',
	6: 'Blue-Green',
	7: 'White'
}

Moving = {
	0: 'Completed',
	1: 'Moving'
}

ErrorMsg = {
	0: None,
	1: 'ERROR_OVERLOAD',
	2: 'ERROR_OVER_HEATING',
	4: 'ERROR_INPUT_VOLTAGE'
}

# I don't trust these error number, I bet the documentation is wrong
ErrorStatusMsg = {
	-1: 'Not a status packet',
	0: None,
	1: 'ERROR_RAIL_FAIL',
	2: 'ERROR_INTRUCTION',
	3: 'ERROR_CRC',
	4: 'ERROR_DATA_RANGE',
	5: 'ERROR_DATA_LENGTH',
	6: 'ERROR_DATA_LIMIT',
	7: 'ERROR_ACCEESS',
	128: 'ALERT'
}

InstrToStr = {
	1: 'Ping',
	2: 'Read',
	3: 'Write',
	6: 'Reset',
	8: 'Reboot',
	85: 'Status'
}
