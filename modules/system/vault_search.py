import os

def search_and_open(query):
    query = query.lower().strip()
    
    # Define high-priority search territories (User folders and D: Drive)
    user_profile = os.environ.get('USERPROFILE')
    search_paths = [
        os.path.join(user_profile, "Desktop"),
        os.path.join(user_profile, "Documents"),
        os.path.join(user_profile, "Downloads"),
        "D:\\"
    ]

    # Blacklist massive hidden directories to prevent the search from hanging
    exclude_dirs = {'$RECYCLE.BIN', 'System Volume Information', 'Windows', 'Program Files', 'Program Files (x86)', 'AppData', 'node_modules', '.git'}

    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
        
        for root, dirs, files in os.walk(search_path):
            # Filter out the blacklisted directories in-place
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # 1. Check folder names first
            for d in dirs:
                if query in d.lower():
                    full_path = os.path.join(root, d)
                    os.startfile(full_path)
                    return f"Vault search successful. I have opened the {d} directory, Sir."
                    
            # 2. Check file names
            for f in files:
                # Strip the extension for easier matching (e.g., "science project" matches "science project.pdf")
                file_name_without_ext = os.path.splitext(f)[0].lower()
                if query in file_name_without_ext:
                    full_path = os.path.join(root, f)
                    os.startfile(full_path)
                    return f"Vault search successful. I have opened {f}."
                    
    return f"Sorry Sir, I could not locate anything matching {query} in the vault."