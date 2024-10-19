import yaml
import os

# Path to your strings file (adjust path if needed)
strings_file_path = "strings/strings/en.yml"

# Function to wrap text with <blockquote> for beautification
def beautify_text(text):
    return f"<blockquote>{text}</blockquote>"

# Load the YAML file
with open(strings_file_path, "r", encoding="utf-8") as file:
    strings_data = yaml.safe_load(file)

# Beautify each string
for key, value in strings_data.items():
    if isinstance(value, str):  # Ensure the value is a string
        strings_data[key] = beautify_text(value)

# Write the updated content back to the file
with open(strings_file_path, "w", encoding="utf-8") as file:
    yaml.dump(strings_data, file, allow_unicode=True)

print(f"Beautified strings in {strings_file_path}")
