import os
import re
import shutil

def normalize_name(name):
    # Ignore hidden files/dirs
    if name.startswith("."):
        return None
        
    # Remove "slides" (case insensitive)
    name = re.sub(r"[-_ ]?slides[-_ ]?", "", name, flags=re.IGNORECASE)
    
    # Extract year (2 or 4 digits) from the end
    year_match = re.search(r"(?:^|[-_ ]|[a-zA-Z])(20\d{2}|\d{2})$", name)
    year = None
    if year_match:
        year_str = year_match.group(1)
        if len(year_str) == 2:
            year = "20" + year_str
        else:
            year = year_str
        name = name[:name.rfind(year_str)]

    # Standardize specific conference names
    parts = [p for p in re.split(r"[^a-zA-Z0-9]", name) if p]
    normalized_parts = []
    
    for part in parts:
        split_camel = re.sub(r"([a-z])([A-Z])", r"\1 \2", part).split()
        for sub in split_camel:
            sub_title = sub.title()
            
            if sub_title.lower() == "recon":
                sub_title = "Recon"
            elif sub_title.lower() == "usa":
                sub_title = "USA"
                
            normalized_parts.append(sub_title)
    
    final_name = "_".join(normalized_parts)
    final_name = final_name.replace("Blackhat", "Black_Hat")
    final_name = re.sub(r"Offensive_?Con", "Offensive_Con", final_name, flags=re.IGNORECASE)
    final_name = final_name.strip("_")

    if year:
        final_name = f"{final_name}_{year}"
        
    return final_name

def main():
    root_dir = "."
    changes = []
    
    for item in os.listdir(root_dir):
        if not os.path.isdir(item) or item.startswith(".") or item == "scripts":
            continue
            
        normalized = normalize_name(item)
        if normalized and normalized != item:
            changes.append((item, normalized))
    
    for original, new in changes:
        print(f"Syncing: {original} -> {new}")
        os.makedirs(new, exist_ok=True)
        for file_name in os.listdir(original):
            src = os.path.join(original, file_name)
            dst = os.path.join(new, file_name)
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            shutil.move(src, dst)
        os.rmdir(original)

if __name__ == "__main__":
    main()
