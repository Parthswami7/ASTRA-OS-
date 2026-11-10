import ctypes
import sys

def authenticate():
    print("[BIOMETRICS] Waking ASUS Fingerprint Scanner...")
    
    try:
        # Connect directly to the core Windows Security DLLs
        credui = ctypes.windll.credui
        ole32 = ctypes.windll.ole32
    except Exception:
        print("[BIOMETRICS-ERROR] Cannot access core Windows Security modules.")
        return False

    # Define the exact data structure Windows requires for the popup
    class CREDUI_INFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("hwndParent", ctypes.c_void_p),
            ("pszMessageText", ctypes.c_wchar_p),
            ("pszCaptionText", ctypes.c_wchar_p),
            ("hbmBanner", ctypes.c_void_p),
        ]

    info = CREDUI_INFO()
    info.cbSize = ctypes.sizeof(CREDUI_INFO)
    info.hwndParent = None
    info.pszMessageText = "Please scan your Master Fingerprint or enter your PIN to unlock ASTRA."
    info.pszCaptionText = "ASTRA OS - Biometric Security Gate"
    info.hbmBanner = None

    # Memory pointers to catch the result
    auth_package = ctypes.c_ulong(0)
    out_auth_buffer = ctypes.c_void_p()
    out_auth_buffer_size = ctypes.c_ulong(0)
    save = ctypes.c_int(0)

    # 0x200 = Ask for Current User (PIN/Fingerprint)
    # 0x2   = Secure Desktop Prompt
    flags = 0x200 | 0x2  
    
    print("[BIOMETRICS] Awaiting Master Fingerprint...")
    
    # This triggers the native Windows Security popup!
    result = credui.CredUIPromptForWindowsCredentialsW(
        ctypes.byref(info),
        0,
        ctypes.byref(auth_package),
        None,
        0,
        ctypes.byref(out_auth_buffer),
        ctypes.byref(out_auth_buffer_size),
        ctypes.byref(save),
        flags
    )

    # Result 0 means the fingerprint or PIN was completely successful
    if result == 0:
        print("\n[BIOMETRICS] Fingerprint Matched - Access Granted!")
        # Free the memory buffer Windows used to prevent RAM leaks
        if out_auth_buffer:
            ole32.CoTaskMemFree(out_auth_buffer)
        return True
    else:
        print("\n[BIOMETRICS] ALERT: Authentication Failed or Canceled. Access Denied.")
        return False

if __name__ == "__main__":
    authenticate()