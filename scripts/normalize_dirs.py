import os
import re
import shutil

def normalize_name(name):
    # Ignore hidden files/dirs
    if name.startswith('.'):
        return None
        
    # Remove 'slides' (case insensitive)
    name = re.sub(r'[-_ ]?slides[-_ ]?', '', name, flags=re.IGNORECASE)
    
    # Extract year (2 or 4 digits) from the end
    # Improved regex: allow attached numbers (e.g. Con24)
    # We strip it out first
    year_match = re.search(r'(?:^|[-_ ]|[a-zA-Z])(20\d{2}|\d{2})$', name)
    year = None
    if year_match:
        # Capture the actual digits from the match group 1
        year_str = year_match.group(1)
        
        # Verify it's not part of a larger word if we matched on [a-zA-Z] boundary?
        # Actually simplest is just to grab the last digits.
        if len(year_str) == 2:
            year = "20" + year_str
        else:
            year = year_str
            
        # Remove the year from the name (only the matched digits at the end)
        # Be careful not to cut the 'n' in 'Con24' if we matched 'n24'
        # We matched the group(1) which is just digits.
        # Find the last occurrence of these digits
        name = name[:name.rfind(year_str)]

    # Standardize specific conference names
    parts = re.split(r'[^a-zA-Z0-9]', name)
    parts = [p for p in parts if p]
    
    normalized_parts = []
    
    for part in parts:
        # Split CamelCase
        split_camel = re.sub(r'([a-z])([A-Z])', r'\1 \2', part).split()
        for sub in split_camel:
            sub_title = sub.title()
            
            # Corrections
            if sub_title.lower() == 'recon':
                sub_title = 'Recon'
            elif sub_title.lower() == 'usa':
                sub_title = 'USA'
                
            normalized_parts.append(sub_title)
    
    # Reassemble
    final_name = "_".join(normalized_parts)
    
    # Specific fix for Black_Hat and Offensive_Con
    final_name = final_name.replace("Blackhat", "Black_Hat")
    final_name = final_name.replace("Black_Hat", "Black_Hat")
    final_name = re.sub(r'Offensive_?Con', 'Offensive_Con', final_name, flags=re.IGNORECASE)
    
    # Trim checks
    final_name = final_name.strip('_')

    if year:
        final_name = f"{final_name}_{year}"
        
    return final_name

def main():
    root_dir = "."  # Current directory
    
    changes = []
    
    for item in os.listdir(root_dir):
        if not os.path.isdir(item) or item.startswith('.') or item == 'scripts':
            continue
            
        normalized = normalize_name(item)
        if normalized and normalized != item:
             changes.append((item, normalized))
    
    # Execute renames
    for original, new in changes:
        if os.path.exists(new):
            print(f"Skipping {original} -> {new}: Target already exists")
            continue
            
        print(f"Renaming: {original} -> {new}")
        shutil.move(original, new)

if __name__ == "__main__":
    main()
