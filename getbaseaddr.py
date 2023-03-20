#!/usr/bin/env python3
import keyboard
from ctypes import *
from ctypes.wintypes import *
import sys
import win32gui
import win32api
import win32process
import win32con
import ctypes as ct
from ctypes import wintypes as wt
import psutil

BYTE = c_ubyte
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
HANDLE = c_void_p
PVOID = c_void_p
LPVOID = c_void_p
UNIT_PTR = c_ulong
SIZE_T = c_ulong

PROCNAME = "Trickster.bin"

kernel32 = ct.windll.LoadLibrary("kernel32.dll")
PROCESS_VM_OPERATION = 0x0008 #   Required to perform an operation on the address space of a process = see VirtualProtectEx and WriteProcessMemory #.
PROCESS_VM_READ = 0x0010 #    Required to read memory in a process using ReadProcessMemory.
PROCESS_VM_WRITE = 0x0020 #   Required to write to memory in a process using WriteProcessMemory.

class MODULEINFO(ct.Structure):
    _fields_ = [
        ("lpBaseOfDll", ct.c_void_p),
        ("SizeOfImage", wt.DWORD),
        ("EntryPoint", ct.c_void_p),
    ]


get_module_information_func_name = "GetModuleInformation"
GetModuleInformation = getattr(ct.WinDLL("kernel32"), get_module_information_func_name,
                               getattr(ct.WinDLL("psapi"), get_module_information_func_name))
GetModuleInformation.argtypes = [wt.HANDLE, wt.HMODULE, ct.POINTER(MODULEINFO)]
GetModuleInformation.restype = wt.BOOL


def get_base_address_original(process_handle, module_handle):
    module_file_name = win32process.GetModuleFileNameEx(process_handle, module_handle)
    print("    File for module {0:d}: {1:s}".format(module_handle, module_file_name))
    module_base_address = win32api.GetModuleHandle(module_file_name)
    return module_base_address


def get_base_address_new(process_handle, module_handle):
    module_info = MODULEINFO()
    res = GetModuleInformation(process_handle.handle, module_handle, ct.byref(module_info))
    print("    Result: {0:}, Base: {1:d}, Size: {2:d}".format(res, module_info.lpBaseOfDll, module_info.SizeOfImage))
    if not res:
        print("    {0:s} failed: {1:d}".format(get_module_information_func_name,
                                               getattr(ct.WinDLL("kernel32"), "GetLastError")()))
    return module_info.lpBaseOfDll


def get_pid():
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME:
            return proc.pid


def read_process_memory(process_id, address, offsets=[], byte_size=2):
    """Read a process' memory based on its process id, address and offsets.
    Returns the address without offsets and the value."""
    # The handle to the program's process
    # This will allow to use ReadProcessMemory
    h_process = ct.windll.kernel32.OpenProcess(win32con.PROCESS_VM_READ, False, process_id)

    # This is a pointer to the data you want to read
    # Use `data.value` to get the value at this pointer
    # In this case, this value is an Integer with 4 bytes
    data = ct.c_uint16(0) if byte_size == 2 else ct.c_uint(0)

    # Size of the variable, it usually is 4 bytes
    bytesRead = ct.c_uint16(0) if byte_size == 2 else ct.c_uint(0)

    # Starting address
    current_address = address

    if offsets:
        # Append a new element to the offsets array
        # This will allow you to get the value at the last offset
        offsets.append(None)
        for offset in offsets:
            # Read the memory of current address using ReadProcessMemory
            # ct.windll.kernel32.ReadProcessMemory(h_process, current_address, ct.byref(data), ct.sizeof(data),
            #                                      ct.byref(bytesRead))
            ct.windll.kernel32.ReadProcessMemory(h_process, current_address, ct.byref(data), ct.sizeof(data),
                                                 None)
            # print('Offset is ', offset)
            # If current offset is `None`, return the value of the last offset
            if not offset:
                return current_address, data.value
            else:
                # Replace the address with the new data address
                current_address = data.value + offset
                print("data from ReadProcessMemory", data)
                print("Current address is ", hex(current_address))

    else:
        # Just read the single memory address
        # ct.windll.kernel32.ReadProcessMemory(h_process, current_address, ct.byref(data), ct.sizeof(data),
        #                                      ct.byref(bytesRead))
        ct.windll.kernel32.ReadProcessMemory(h_process, current_address, ct.byref(data), ct.sizeof(data),
                                             None)
    # Close the handle to the process
    ct.windll.kernel32.CloseHandle(h_process)

    # Return a pointer to the value and the value
    # The pointer will be used to write to the memory
    return current_address, data.value


def get_base_address():
    # pid = int(argv[0]) if argv and argv[0].isdecimal() else win32api.GetCurrentProcessId()
    pid = get_pid()
    print("Working on pid {0:d}".format(pid))
    process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    print("  Process handle: {0:d}".format(process_handle.handle))
    module_handles = win32process.EnumProcessModules(process_handle)
    module_handles_count = len(module_handles)
    print("  Loaded modules count: {0:d}".format(module_handles_count))
    module_index = 0  # 0 - the executable itself
    if module_index > module_handles_count:
        module_index = 0
    module_handle = module_handles[module_index]
    module_file_name = win32process.GetModuleFileNameEx(process_handle, module_handle)
    print("  File [{0:s}] (index {1:d}) is loaded at address 0x{2:016X} ({3:d})".format(module_file_name, module_index,
                                                                                        module_handle, module_handle))
    process_handle.close()
    base_address = int(hex(module_handle), 16)
    return base_address


def main(*argv):
    base = get_base_address()
    pid = get_pid()
    PlayerYpos = base + 0x93A002
    PlayerXpos = base + 0x93A000
    MouseXpos = base + 0x994124
    MouseYpos = base + 0x994126

    current_address, value = read_process_memory(pid, PlayerXpos)
    print("Address: {}, Value: {}".format(hex(current_address), value))
    current_address, value = read_process_memory(pid, PlayerYpos)
    print("Address: {}, Value: {}".format(hex(current_address), value))

    current_address, value = read_process_memory(pid, MouseXpos)
    print("Address: {}, Value: {}".format(hex(current_address), value))
    current_address, value = read_process_memory(pid, MouseYpos)
    print("Address: {}, Value: {}".format(hex(current_address), value))

    cursorStateBaseAddress = base + 0x0088A4D0
    cursorStateOffset = [0x1C, 0x48, 0x14, 0x2C4, 0x4, 0x164]
    cursor_address, value = read_process_memory(pid,
                                                cursorStateBaseAddress,
                                                cursorStateOffset,
                                                byte_size=4)
    temp, val = read_process_memory(pid,
                                    cursorStateBaseAddress,
                                    [],
                                    byte_size=4)
    print(temp)
    print(val)
    print("Address: {}, Value: {}".format(hex(cursor_address), value))
    targetIDoffset = [0x1C, 0x48, 0x14, 0x2C4, 0x4, 0x200]
    targetID_address, value = read_process_memory(pid,
                                                  cursorStateBaseAddress,
                                                  targetIDoffset,
                                                  byte_size=4)
    print("Address: {}, Value: {}".format(hex(targetID_address), value))


if __name__ == "__main__":
    # read_process_memory(get_pid(), )
    mem = get_base_address() + int(0x00994118)
    value = read_process_memory(get_pid(),
                                address=mem,
                                offsets=[],
                                byte_size=2)
    print(value)
