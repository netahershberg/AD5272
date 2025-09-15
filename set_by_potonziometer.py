import sys
import time
import pyvisa
import os
import TLPy3
import subprocess
import numpy as np
sys.path.append(r'C:\EV_WORK\ccd_ev-common\DAL\DALGT')
from DALGT_TestStand_Python37 import *
x = input(" where are you? PTK or IDC ")
if x == "PTK":
    DMM = InitInstrument('USB0::0x0957::0x0607::MY53002858::0::INSTR', 'dmm', '34401')
elif x == "IDC":
    DMM = InitInstrument('USB0::0x0957::0x0607::MY53000311::0::INSTR', 'dmm', '34401')
psu_visa_address = 'USB0::0x0957::0x0907::MY43021979::0::INSTR'

#for color and Table
class bcolors:
        # Standard Colors
        RESET = "\033[0m"  # Reset to default color
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        RED = "\033[31m"  # Red text
        GREEN = "\033[32m"  # Green text
        YELLOW = "\033[33m"  # Yellow text
        BLUE = '\033[34m'
        CYAN = '\033[36m'
        BLACK = "\033[30m"
        MAGENTA = "\033[35m"
        WHITE = "\033[37m"
        GRAY = "\033[38;5;238m"
        ORANGE = "\033[38;5;214m"
        PINK = "\033[38;5;213m"
        PURPLE = "\033[38;5;129m"
        TEAL = "\033[38;5;30m"
        BROWN = "\033[38;5;94m"
        # Bright Colors
        BRIGHT_BLACK = "\033[90m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_BLUE = "\033[94m"
        BRIGHT_MAGENTA = "\033[95m"
        BRIGHT_CYAN = "\033[96m"
        BRIGHT_WHITE = "\033[97m"

num = TLPy3.TLPy_MPSSE_Init()

voltage_target_ASVR = 1.2
# voltage_target_ASVR = sys.argv[1]

pot_value_target_in_dec_intial = 0
global arr
dict_to_find = {}
minimum_element = None

if (num == 0):
    print("found no devices")
    exit()
try:
    handle = TLPy3.TLPy_MPSSE_I2C_Open_channel(1) # Open i2c channel
except Exception as e:
    print("failed connecting to device")
    print(str(e))

def swap_endianness(hex_value):
    # Convert the hex value to bytes and swap endianness
    hex_bytes = hex_value.to_bytes((hex_value.bit_length() + 7) // 8, byteorder='little')
    swapped_bytes = hex_bytes[::-1]
    # Convert the swapped bytes back to an integer
    swapped_value = int.from_bytes(swapped_bytes, byteorder='little')
    return swapped_value

def phars_command(address,WR, op_code, data):
    shifted_addr = (address << 1) | WR
    upper_2_bits_opcode = (op_code >> 2) & 0x03
    lower_2_bits_opcode = op_code & 0x03
    upper_2_bits_data = (data >> 8) & 0x03
    opcod_2lsb_data_2msb = (lower_2_bits_opcode << 2) | upper_2_bits_data
    combined_word = (shifted_addr << 16) | (upper_2_bits_opcode << 12) | (opcod_2lsb_data_2msb << 8) | (data & 0xFF)
    hex_word = combined_word & 0xFFFFFF
    return hex_word

def set_asvr_1v2_code_via_i2c(pot_value):
    # TODO don't touch
    """ sending initial command - Enable update of wiper position and 50-TP memory contents through digital interface """
    code0 = 0x5E1C02
    code_swap = swap_endianness(code0)
    buffer0 = TLPy3.TLPy_AllocateUserMemory(4)
    TLPy3.TLPy_WriteDwordToUserMemory(buffer0,4, 0, code_swap, 0xffffff)
    TLPy3.TLPy_MPSSE_I2C_Device_write(handle,buffer0,3)
    time.sleep(0.1)

    """ sending data to config the wiper """
    address = 0x2F # Write
    WR = 0x0 # 0 for write, 1 for Read
    """ OP_Code_map"""
    op_code = 0x1 # Write contents of serial register data to RDAC
    # op_code = 0x3 # Store wiper setting: store RDAC setting to 50-TP
    # op_code = 0x4 # Software reset: refresh RDAC with the last 50-TP memory stored value
    # op_code = 0x5 # Read contents of 50-TP from the SDA output in the next frame.
    # op_code = 0x6 # Read address of the last 50-TP programmed memory location
    """ Data of wiper"""
    data = pot_value # maximum value = 3FF(10 bit) giving the lowest voltage value
    code = phars_command(address, WR, op_code, data)
    # print(f"hex code: {change_upper(hex(code))}")
    code_swap = swap_endianness(code)
    """ write the op_code + data to the POT"""
    buffer = TLPy3.TLPy_AllocateUserMemory(4)
    TLPy3.TLPy_WriteDwordToUserMemory(buffer,4, 0, code_swap, 0xffffff)
    TLPy3.TLPy_MPSSE_I2C_Device_write(handle,buffer,3)
    time.sleep(0.8)

def set_asvr_1v2_code_via_i2c_on_wiper(pot_value):
    # TODO don't touch
    """ sending initial command - Enable update of wiper position and 50-TP memory contents through digital interface """
    code0 = 0x5E1C03
    code_swap = swap_endianness(code0)
    buffer0 = TLPy3.TLPy_AllocateUserMemory(4)
    TLPy3.TLPy_WriteDwordToUserMemory(buffer0,4, 0, code_swap, 0xffffff)
    TLPy3.TLPy_MPSSE_I2C_Device_write(handle,buffer0,3)

    """ sending data to config the wiper """
    address = 0x2F # Write
    WR = 0x0 # 0 for write, 1 for Read
    """ OP_Code_map"""
    op_code = 0x1 # Write contents of serial register data to RDAC
    # TODO - change to code 3 to store on wiper
    # op_code = 0x3 # Store wiper setting: store RDAC setting to 50-TP
    """ Data of wiper"""
    data = pot_value # maximum value = 3FF(10 bit) giving the lowest voltage value
    code = phars_command(address,WR, op_code, data)
    # print(f"hex code: {change_upper(hex(code)}")
    code_swap = swap_endianness(code)
    """ write the op_code + data to the POT"""
    buffer = TLPy3.TLPy_AllocateUserMemory(4)
    TLPy3.TLPy_WriteDwordToUserMemory(buffer,4, 0, code_swap, 0xffffff)
    TLPy3.TLPy_MPSSE_I2C_Device_write(handle,buffer,3)
    time.sleep(0.8)

    print("set asvr to wiper value ", data )

def change_upper(hex_string):
    return hex_string[:2].lower() + hex_string[2:].upper()

def calculate_value_dec(voltage_target_ASVR):
    Rup = 24.9*1e3
    Rdown = Rup/(voltage_target_ASVR/0.6-1)
    Value_in_DEC = Rdown/(49*1e3/1024)
    # print("approximate resistance of rheostat Value for start position in hex is", hex(int(Value_in_DEC)), ",in decimal it's ",int(Value_in_DEC))
    return int(Value_in_DEC)

def asvr_1v2_check(vol, dmm):
    print(bcolors.CYAN + bcolors.BOLD + "asvr_1v2_voltage_from_dmm is: " + str(dmm) + bcolors.RESET)
    if type(vol) == type('string'):
        vol = float(vol)
    if type(dmm) == type('string'):
        dmm = float(dmm)
    res = dmm - vol
    if (res <= 0.002) and (res >= -0.002):
        print(bcolors.YELLOW + bcolors.BOLD + "The voltage delta of " + str(res) + " is below SVR resolution, data will be stored" + bcolors.RESET)
        print("SVR complete")
        return 0
    else:
        print("the SVR delta still far from the POT resolution capabilities ")
        return 1

def asvr_1v2_control(vol, dmm, pot_value_target_in_dec):
    if dmm == "new":
        print(f"pot value_in_dec on new is calculate by component equation for start position ")
        pot_value_target_in_dec = calculate_value_dec(voltage_target_ASVR)
    elif vol > dmm:
        pot_value_target_in_dec -= 1
        print(f"change will be made pot value target_in_dec now will be -1 is: {pot_value_target_in_dec}")
    elif vol < dmm:
        pot_value_target_in_dec += 1
        print(f"change will be made pot value target_in_dec now will be +1 is: {pot_value_target_in_dec}")
    set_asvr_1v2_code_via_i2c(int(pot_value_target_in_dec))
    return pot_value_target_in_dec

def store_data(vol_in_dec, dmm,voltage_target_ASVR):
    global minimum_element
    dict_to_find[vol_in_dec] = abs(dmm-voltage_target_ASVR)
    print(dict_to_find)
    if len(dict_to_find.keys()) == 2:
        minimum_element = np.min(np.array(list(dict_to_find.values())))
        return False
    else:
        return True

def PS_Toggle_5V(psu_visa_address):
    rm = pyvisa.ResourceManager()
    PSU_N6700C = rm.open_resource(psu_visa_address)
    print('PS7 off - 5V')
    PSU_N6700C.write(':OUTPut:STATe %d,(%s)' % (0, '@3'))  # turn on 5V
    time.sleep(1)
    print('PS on - 5V')
    PSU_N6700C.write(':OUTPut:STATe %d,(%s)' % (1, '@3'))  # turn on 5V
    time.sleep(1)

def config_svr(flag):
    counter = 0

    while flag:
        print("\n\n" + bcolors.ORANGE + bcolors.BOLD + bcolors.UNDERLINE + "counter value is : " + str(counter) + bcolors.RESET)

        asvr_1v2_voltage_from_dmm = float(DMM.InstrObject.getvoltage())
        print(bcolors.CYAN + bcolors.BOLD + "asvr_1v2_voltage_from_dmm at start loop is:" + str(asvr_1v2_voltage_from_dmm) + bcolors.RESET)

        if counter == 0:
            asvr_1v2_voltage_from_dmm = "new"
            pot_value_target_in_dec = asvr_1v2_control(vol=voltage_target_ASVR, dmm=asvr_1v2_voltage_from_dmm,pot_value_target_in_dec=pot_value_target_in_dec_intial)
            print(bcolors.BLUE + bcolors.BOLD + "pot value target in dec is : " + str(pot_value_target_in_dec) + bcolors.RESET)
            print(bcolors.PINK + bcolors.BOLD + "wait for ASVR 1 sec dmm on new" + bcolors.RESET)
        else:
            pot_value_target_in_dec = asvr_1v2_control(vol=voltage_target_ASVR, dmm=asvr_1v2_voltage_from_dmm,pot_value_target_in_dec=pot_value_target_in_dec)
            print(bcolors.BLUE + bcolors.BOLD + "pot value target in dec is : " + str(
                pot_value_target_in_dec) + bcolors.RESET)
            print(bcolors.PINK + bcolors.BOLD + "wait for ASVR 1 se" + bcolors.RESET)

        asvr_1v2_voltage_from_dmm = float(DMM.InstrObject.getvoltage())
        print(bcolors.MAGENTA + bcolors.BOLD + "asvr_1v2_voltage_from_dmm after change wiper code:" + str(pot_value_target_in_dec) + ", is: " + str(asvr_1v2_voltage_from_dmm) + bcolors.RESET)

        if counter != 0:
            print("checking asvr delta")
            if asvr_1v2_check(voltage_target_ASVR, asvr_1v2_voltage_from_dmm) == 0:
                flag = store_data(pot_value_target_in_dec, asvr_1v2_voltage_from_dmm, voltage_target_ASVR)
            elif counter > 29:
                flag = False
            else:
                flag = True
        counter += 1
        if counter >= 30:
            print(
                "\n" + bcolors.RED + bcolors.BOLD + bcolors.UNDERLINE + "   error asvr couldn't config" + bcolors.RESET)
            flag = False
    time.sleep(1)

    """ The correspond key to the lowest res(voltage_target_ASVR-dmm) """
    if minimum_element is None:
        # Handle the case where minimum_element is None
        result_key = None  # or some other appropriate default value
        print(
            "\n\nbcolors.RED + bcolors.BOLD ********** warning no result_key had been found - can cause by only 2 argument that smaller than 0.0002, or pot not function well or set_asvr_functin haven't been activated *********** + bcolors.RESET")
        exit(0)
    else:
        result_key = list(dict_to_find.keys())[list(dict_to_find.values()).index(minimum_element)]

        return result_key

def call_mux_1v2():
    p1 = subprocess.Popen(
        ['c:\Python38\python.exe', r'C:\EV_WORK\ccd_ev_orchestrator\voltage_mux_control_RBR.py', '1.2'], shell=True)
    p1.wait(30)
    print('wait for voltage MUX 3 sec')
    time.sleep(3)


def intial_check():
    asvr_1v2_voltage_from_dmm = float(DMM.InstrObject.getvoltage())
    if asvr_1v2_check(voltage_target_ASVR, asvr_1v2_voltage_from_dmm) == 0:
        print("\n#########################################"
              "\n\tvolt is already at target volt: " + str(asvr_1v2_voltage_from_dmm) + \
              "\n#########################################\n")
        exit(0)

if __name__ == "__main__":
    call_mux_1v2()
    intial_check()
    flag = True
    result_key = config_svr(flag)

    print("\n\n" + bcolors.GREEN + bcolors.BOLD  +"The correspond dec value for the POT to burn on wiper is : " +str(result_key) +", for the minimum_element res that is: \n\n\n\t\t\t\t\t\t\t\t"+str(minimum_element) + bcolors.RESET)
    set_asvr_1v2_code_via_i2c(result_key)
    time.sleep(0.8)



    #TODO don't use this function unless authrized by NETA Hershberg"""
    # set_asvr_1v2_code_via_i2c_on_wiper(result_key)
    # PS_Toggle_5V(psu_visa_address)

    asvr_1v2_voltage_from_dmm = float(DMM.InstrObject.getvoltage())
    print("\n#########################################"
    "\n\t\tfinal volt is: " + str(asvr_1v2_voltage_from_dmm)+ \
    "\n#########################################\n")

    TLPy3.TLPy_MPSSE_I2C_Close_channel(handle)

    # return result_key


