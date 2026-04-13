import os
from copy import deepcopy
import xml.etree.ElementTree as ET


def parse_fields(root):
    """Parse all field elements and extract name, x, y values."""
    fields = []
    for field in root.findall('.//field'):
        name_elem = field.find('name')
        x_elem = field.find('x')
        y_elem = field.find('y')
        page_elem = field.find('page')
        
        if name_elem is not None and name_elem.text:
            field_data = {
                'name': name_elem.text.strip(),
                'x': float(x_elem.text) if x_elem is not None and x_elem.text else 0,
                'y': float(y_elem.text) if y_elem is not None and y_elem.text else 0,
                'page': int(page_elem.text) if page_elem is not None and page_elem.text else 1
            }
            fields.append(field_data)
    
    return fields


def get_field_group_key(name):
    """Extract base prefix for grouping (remove column_row suffix)."""
    parts = name.rsplit('_', 2)
    if len(parts) >= 3:
        try:
            # Verify last two parts are numbers (column and row)
            int(parts[-1])
            int(parts[-2])
            return parts[0]  # Return base prefix (e.g., 'fld_partA')
        except ValueError:
            return None
    return None


def detect_field_groups(fields):
    """Detect all _1 to _2 ranges within grouped fields."""
    groups = {}
    
    for field in fields:
        name = field['name']
        prefix = get_field_group_key(name)
        
        if prefix is None:
            continue
        
        # Check if this field ends with _1 or _2 (row indicator)
        parts = name.rsplit('_', 2)
        row_indicator = parts[-1] if len(parts) >= 3 else None
        
        if row_indicator in ['1', '2']:
            if prefix not in groups:
                groups[prefix] = []
            groups[prefix].append(field)
    
    # Find ranges for each group
    detected_ranges = []
    
    for prefix, group_fields in sorted(groups.items()):
        # Sort by name to maintain order
        group_fields.sort(key=lambda f: f['name'])
        
        # Find _1 fields (start of range) and _2 fields (end of range)
        row_1_fields = [f for f in group_fields if f['name'].endswith('_1')]
        row_2_fields = [f for f in group_fields if f['name'].endswith('_2')]
        
        if not row_1_fields or not row_2_fields:
            continue
        
        # Get the first _1 field as start marker
        start_field = row_1_fields[0]
        
        # Find corresponding _2 fields (same column)
        start_col = start_field['name'].rsplit('_', 2)[-2]
        matching_row_2 = [f for f in row_2_fields if f['name'].rsplit('_', 2)[-2] == start_col]
        
        if not matching_row_2:
            continue
        
        end_field = matching_row_2[0]
        
        # Collect all fields with _1 or _2 suffix from this prefix
        range_fields = [f for f in group_fields if f['name'].endswith(('_1', '_2'))]
        
        detected_ranges.append({
            'prefix': prefix,
            'start_field': start_field['name'],
            'end_field': end_field['name'],
            'fields': sorted(range_fields, key=lambda f: f['name'])
        })
    
    return detected_ranges


def get_available_pages(fields):
    """Get list of unique page numbers from fields."""
    pages = set(f['page'] for f in fields)
    return sorted(pages)


def filter_fields_by_page(fields, page_number):
    """Filter fields to only include those on the specified page."""
    return [f for f in fields if f['page'] == page_number]


def find_consecutive_fields_by_suffix(root, page_filter=None, start_index=0, suffix="_1"):
    """Find consecutive fields ending with specified suffix from a starting index."""
    all_fields = parse_fields(root)
    
    # Apply page filter if provided
    if page_filter is not None:
        fields = filter_fields_by_page(all_fields, page_filter)
    else:
        fields = all_fields
    
    # Start from the given index and find consecutive fields ending with suffix
    result_fields = []
    
    for i in range(start_index, len(fields)):
        field = fields[i]
        if field['name'].endswith(suffix):
            result_fields.append(field)
        else:
            break  # Stop when we encounter a field that doesn't end with suffix
    
    return result_fields, len(result_fields)


def find_consecutive_fields_ending_with_suffix(root, page_filter=None, start_index=0, suffix="_1"):
    """Find consecutive fields ending with specified suffix from a starting index."""
    all_fields = parse_fields(root)
    
    # Apply page filter if provided
    if page_filter is not None:
        fields = filter_fields_by_page(all_fields, page_filter)
    else:
        fields = all_fields
    
    # Start from the given index and find consecutive fields ending with suffix
    result_fields = []
    
    for i in range(start_index, len(fields)):
        field = fields[i]
        if field['name'].endswith(suffix):
            result_fields.append(field)
        else:
            break  # Stop when we encounter a field that doesn't end with suffix
    
    return result_fields


def find_consecutive_fields_ending_with_suffix(root, page_filter=None, start_index=0, suffix="_1", display=True):
    """Find consecutive fields ending with specified suffix from a starting index."""
    all_fields = parse_fields(root)
    
    # Apply page filter if provided
    if page_filter is not None:
        fields = filter_fields_by_page(all_fields, page_filter)
    else:
        fields = all_fields
    
    # Start from the given index and find consecutive fields ending with suffix
    result_fields = []
    
    for i in range(start_index, len(fields)):
        field = fields[i]
        if field['name'].endswith(suffix):
            result_fields.append(field)
        else:
            break  # Stop when we encounter a field that doesn't end with suffix
    
    if display and not result_fields:
        print(f"No consecutive fields ending with '{suffix}' found at the start of the page.")
    
    if display:
        # Display results
        print(f"\nConsecutive Fields Ending with '{suffix}':")
        print("-" * 70)
        print(f"{'Field Name':<35} {'X':>12} {'Y':>12}")
        print("-" * 70)
        
        for field in result_fields:
            print(f"{field['name']:<35} {field['x']:>12.1f} {field['y']:>12.1f}")
        
        print("-" * 70)
        print(f"Total fields: {len(result_fields)}")
    
    # Return the index where processing stopped (first field that doesn't end with suffix)
    stop_index = len(result_fields) + start_index
    for i in range(start_index, len(fields)):
        if not fields[i]['name'].endswith(suffix):
            stop_index = i
            break
    
    return result_fields, stop_index


def skip_to_next_block(root, page_filter=None):
    """Skip to next block logic - search for specific field pattern."""
    all_fields = parse_fields(root)
    
    # Apply page filter if provided
    if page_filter is not None:
        fields = filter_fields_by_page(all_fields, page_filter)
    else:
        fields = all_fields
    
    groups = detect_field_groups(fields)
    
    if not groups:
        print("No valid _1 to _2 ranges found in the XML file.")
        return
    
    print("\nDetected Field Groups:")
    print("-" * 70)
    for i, group in enumerate(groups, 1):
        print(f"{i}. {group['prefix']}: {group['start_field']} to {group['end_field']} ({len(group['fields'])} fields)")
    print()
    
    choice = input("Enter group number to analyze: ").strip()
    
    if not choice.isdigit():
        print("Invalid input.")
        return
    
    group_number = int(choice)
    if group_number < 1 or group_number > len(groups):
        print(f"Invalid selection. Please choose a number between 1 and {len(groups)}.")
        return
    
    selected_group = groups[group_number - 1]
    
    print(f"\nFields in range: {selected_group['prefix']} ({selected_group['start_field']} to {selected_group['end_field']})")
    print("-" * 70)
    print(f"{'Field Name':<35} {'X':>12} {'Y':>12}")
    print("-" * 70)
    
    for field in selected_group['fields']:
        print(f"{field['name']:<35} {field['x']:>12.1f} {field['y']:>12.1f}")
    
    print("-" * 70)
    print(f"Total fields: {len(selected_group['fields'])}")


def main():
    # Ask for XML filepath input
    xml_filepath = input("Enter the XML file path: ").strip()

    if not os.path.exists(xml_filepath):
        print(f"Error: File '{xml_filepath}' does not exist.")
        return

    # Create backup of original file
    backup_path = f"{xml_filepath}.backup"
    with open(xml_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Backup saved to: {backup_path}")

    # Parse the XML file
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    # Get available pages and ask user which page to process
    all_fields = parse_fields(root)
    available_pages = get_available_pages(all_fields)
    
    print(f"\nAvailable pages in XML: {available_pages}")
    
    while True:
        try:
            page_input = input("Enter the page number to process: ").strip()
            if not page_input:
                print("Page number required.")
                continue
            selected_page = int(page_input)
            if selected_page in available_pages:
                break
            else:
                print(f"Invalid page. Please choose from {available_pages}")
        except ValueError:
            print("Please enter a valid number.")

    # Track state for sequential processing
    current_start_index = 0
    last_suffix_used = "_1"  # Default to _1 if no previous suffix
    
    while True:
        print("\nProcessing Options:")
        print(f"1 - Find consecutive fields ending with specific suffix")
        print(f"2 - Continue from previous position (next suffix after {last_suffix_used})")
        print("3 - Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Ask user which suffix number they want to search for
            while True:
                try:
                    suffix_input = input("Enter the numerical suffix to find (e.g., 1, 2, 3): ").strip()
                    if not suffix_input:
                        print("Suffix number required.")
                        continue
                    suffix_num = int(suffix_input)
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            suffix = f"_{suffix_num}"
            result_fields, stop_index = find_consecutive_fields_ending_with_suffix(root, page_filter=selected_page, start_index=0, suffix=suffix, display=True)
            if result_fields is not None:
                current_start_index = stop_index
                last_suffix_used = suffix  # Update the last suffix used
        elif choice == '2':
            # Determine next suffix (increment from last used)
            if current_start_index > 0:
                # Use the tracked last_suffix_used value
                try:
                    last_num = int(last_suffix_used[1:])
                    next_num = last_num + 1
                    next_suffix = f"_{next_num}"
                except (ValueError, IndexError):
                    next_suffix = "_2"
                
                start_index = current_start_index
            else:
                # Option 2 chosen first - find the first instance of _2 on the page
                all_fields = parse_fields(root)
                if selected_page is not None:
                    fields = filter_fields_by_page(all_fields, selected_page)
                else:
                    fields = all_fields
                
                # Find the first field ending with _2
                next_suffix = "_2"
                start_index = 0
                for i, field in enumerate(fields):
                    if field['name'].endswith(next_suffix):
                        start_index = i
                        break
            
            print(f"\nContinuing from index {start_index} with suffix '{next_suffix}'")
            
            result_fields, stop_index = find_consecutive_fields_ending_with_suffix(root, page_filter=selected_page, 
                                                                                   start_index=start_index, 
                                                                                   suffix=next_suffix, display=True)
            
            # Update the last suffix used for next prompt
            last_suffix_used = next_suffix
            
            if not result_fields:
                print(f"No consecutive fields ending with '{next_suffix}' found starting from index {current_start_index}.")
            else:
                # Display results
                print("\nConsecutive Fields Ending with '{}':".format(next_suffix))
                print("-" * 70)
                print(f"{'Field Name':<35} {'X':>12} {'Y':>12}")
                print("-" * 70)
                
                for field in result_fields:
                    print(f"{field['name']:<35} {field['x']:>12.1f} {field['y']:>12.1f}")
                
                print("-" * 70)
                print(f"Total fields: {len(result_fields)}")
            
            # Update state - the next time option 2 is used, it will increment from this suffix
            current_start_index = stop_index
            
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
