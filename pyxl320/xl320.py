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
XL320_PING   = 0x01
XL320_READ   = 0x02
XL320_WRITE  = 0x03
XL320_RESET  = 0x06
XL320_REBOOT = 0x08
XL320_STATUS = 0x55

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
XL320_PRESENT_POSITION = 37  # current servo angle
XL320_PESENT_LOAD      = 41  # current load
XL320_PESENT_VOLTAGE   = 45  # current voltage

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
