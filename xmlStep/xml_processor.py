import os
from copy import deepcopy
import xml.etree.ElementTree as ET


def find_elements_range(root):
    """Option 1: Find elements from first _1 to first _2"""
    found_elements = []
    in_range = False
    
    for elem in root.iter():
        if elem.tag.endswith('_1'):
            in_range = True
        
        if in_range:
            found_elements.append(elem.tag)
        
        if in_range and elem.tag.endswith('_2'):
            break
    
    print(f"Elements from _1 to _2: {found_elements}")


def skip_to_next_block(root):
    """Option 2: Skip to next block logic"""
    print("Skipping to next block logic...")
    # Placeholder for future implementation


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

    while True:
        print("\nProcessing Options:")
        print("1 - Finding elements in the previously described range")
        print("2 - Skip to the next block to find the ranged elements")
        print("3 - Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            find_elements_range(root)
        elif choice == '2':
            skip_to_next_block(root)
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

    # Output modified XML
    output_path = f"{xml_filepath}.modified"
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Modified XML saved to: {output_path}")


if __name__ == "__main__":
    main()
