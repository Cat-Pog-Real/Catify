from ctypes import wintypes, WinDLL, byref, create_unicode_buffer

# Define constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MAX_PATH = 260

# Load required libraries
psapi = WinDLL('Psapi.dll')
user32 = WinDLL('User32.dll')
kernel32 = WinDLL('Kernel32.dll')

def get_exe_name_from_hwnd(hwnd):
    """Get the executable name of the process owning the given HWND."""
    # Get the process ID from the HWND
    process_id = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, byref(process_id))  # Corrected to use user32.dll

    # Open the process with required permissions
    process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, process_id.value)
    if not process_handle:
        return None

    # Get the executable name
    exe_name = create_unicode_buffer(MAX_PATH)
    if psapi.GetModuleFileNameExW(process_handle, None, exe_name, MAX_PATH) == 0:
        kernel32.CloseHandle(process_handle)
        return None

    # Close the process handle
    kernel32.CloseHandle(process_handle)

    # Return the executable name
    return exe_name.value

def window_focused():
    """Returns path to focused window."""
    # Get the HWND of the currently focused window
    foreground_hwnd = user32.GetForegroundWindow()

    # Get the executable name of the focused window
    exe_name = get_exe_name_from_hwnd(foreground_hwnd)

    # Compare the two HWNDs
    return exe_name