import json
import re

def parse_txt_to_jsonl(input_file, output_file):
    with open(input_file, "r") as file:
        content = file.read()
    
    # Split the content by each ID block
    blocks = re.split(r'#+\s*ID:\s*\d+\s*#+', content)

    json_data = []

    for block in blocks[1:]:  # Skip the first empty block
        # Extract the fields using regular expressions, and handle potential None cases
        data = {}
        
        case_match = re.search(r'Project:\s*(.*)', block)
        data['Project'] = case_match.group(1).replace("##", "").strip() if case_match else None


        client_pin_match = re.search(r'Client Pin:\s*(\d+)', block)
        data['Client Pin'] = client_pin_match.group(1).strip() if client_pin_match else None

        client_name_match = re.search(r'Client Name:\s*(.*)', block)
        data['Client Name'] = client_name_match.group(1).strip() if client_name_match else None

        user_name_match = re.search(r'User Name:\s*(.*)', block)
        data['User Name'] = user_name_match.group(1).strip() if user_name_match else None

        password_match = re.search(r'Password:\s*(.*)', block)
        data['Password'] = password_match.group(1).strip() if password_match else None

        db_server_match = re.search(r'DB Server:\s*(.*)', block)
        data['DB Server'] = db_server_match.group(1).strip() if db_server_match else None

        instance_match = re.search(r'Instance:\s*(.*)', block)
        data['Instance'] = instance_match.group(1).strip() if instance_match else None

        db_name_match = re.search(r'DB Name:\s*(.*)', block)
        data['DB Name'] = db_name_match.group(1).strip() if db_name_match else None

        webshare_match = re.search(r'Webshare:\s*(.*)', block)
        data['Webshare'] = webshare_match.group(1).strip() if webshare_match else None

        # last_login_match = re.search(r'Last Login:\s*(.*)', block)
        # data['Last Login'] = last_login_match.group(1).strip() if last_login_match else ""

        # Add to JSON data list
        json_data.append(data)
    
    # Write to JSONL file
    with open(output_file, "w") as jsonl_file:
        for entry in json_data:
            jsonl_file.write(json.dumps(entry) + "\n")

    print(f"Data has been successfully written to {output_file}")



parse_txt_to_jsonl('docs\chewbaca.txt', 'docs\parsed_chewbaca.jsonl')