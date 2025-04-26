import json

# Function to remove entries with duplicate descriptions
def remove_duplicate_descriptions(input_file, output_file):
    # Read the data from the pins.json file
    with open(input_file, 'r', encoding='utf-8') as json_file:
        pins = json.load(json_file)

    # Create a set to track unique descriptions
    seen_descriptions = set()
    unique_pins = []

    # Loop through the pins and keep only unique descriptions
    for pin in pins:
        description = pin.get('description')
        if description and description not in seen_descriptions:
            unique_pins.append(pin)
            seen_descriptions.add(description)

    # Save the unique pins back to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(unique_pins, json_file, ensure_ascii=False, indent=4)

    print(f"Removed duplicates. {len(pins) - len(unique_pins)} duplicates were removed.")
    print(f"Updated pins saved to {output_file}.")

# Specify input and output files
input_file = 'pins.json'
output_file = 'pins_no_duplicates.json'

# Run the function
remove_duplicate_descriptions(input_file, output_file)
