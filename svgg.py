# import os
# import re
# # NOTE: The SVG_DATA list is defined directly within this script for convenience.

# # --- Configuration ---
# OUTPUT_DIR = "extracted_svg_icons"

# def sanitize_filename(name):
#     """
#     Converts a descriptive name into a safe filename.
#     Replaces spaces and hyphens with underscores and removes invalid characters.
#     """
#     # Replace spaces and hyphens with underscores, and remove multiple underscores
#     name = re.sub(r'[\s\-]+', '_', name)
#     # Remove any characters that are not alphanumeric or underscores
#     name = re.sub(r'[^\w_]', '', name)
#     return name.lower()

# def save_svg_from_data(svg_data_list):
#     """
#     Creates an output directory and saves each SVG item in the list
#     as a separate .svg file.
#     """
#     print(f"Starting SVG extraction process...")

#     # 1. Create the output directory if it doesn't exist
#     try:
#         # Use a temporary name to avoid confusion with the output directory if this function is run multiple times
#         current_output_dir = os.path.join(os.getcwd(), OUTPUT_DIR)
#         os.makedirs(current_output_dir, exist_ok=True)
#         print(f"Output directory created or exists: '{current_output_dir}'")
#     except OSError as e:
#         print(f"Error creating directory {current_output_dir}: {e}")
#         return

#     # 2. Iterate through the data and write files
#     file_count = 0
#     for item in svg_data_list:
#         name = item.get("name")
#         code = item.get("code")

#         if not name or not code:
#             print("Skipping item with missing name or code.")
#             continue

#         # Sanitize the name and create the full file path
#         sanitized_name = sanitize_filename(name)
#         file_path = os.path.join(current_output_dir, f"{sanitized_name}.svg")

#         # Write the SVG content to the file
#         try:
#             # Add XML declaration for robust SVG file creation
#             if not code.strip().startswith('<?xml'):
#                 # Ensure the SVG tag is the one that gets saved
#                 match = re.search(r'(<svg.*?</svg>)', code, re.DOTALL | re.IGNORECASE)
#                 if match:
#                     svg_content = match.group(1)
#                 else:
#                     svg_content = code

#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(svg_content)
#             # print(f"Successfully saved: {file_path}") # Suppress excessive printing
#             file_count += 1
#         except IOError as e:
#             print(f"Error writing file {file_path}: {e}")

#     print(f"\nProcessing complete. {file_count} SVG files saved to '{current_output_dir}/'")

# # --- Function to adapt for CSV (retained from original request) ---
# def read_and_save_svgs_from_csv(csv_filepath, name_column='name', code_column='code'):
#     """
#     Example of how to adapt the script to read from a CSV file (requires pandas).
#     """
#     print(f"\n[CSV ADAPTER MODE]: Reading from {csv_filepath}...")
#     try:
#         import pandas as pd
#     except ImportError:
#         print("Error: pandas library is required for CSV functionality.")
#         print("Install it with: pip install pandas")
#         return

#     try:
#         df = pd.read_csv(csv_filepath)
#         # Reformat DataFrame records into the expected list of dictionaries
#         csv_data = [
#             {"name": row[name_column], "code": row[code_column]}
#             for index, row in df.iterrows()
#             if pd.notna(row[name_column]) and pd.notna(row[code_column])
#         ]
#         save_svg_from_data(csv_data)
#     except FileNotFoundError:
#         print(f"Error: CSV file not found at {csv_filepath}")
#     except Exception as e:
#         print(f"An unexpected error occurred during CSV processing: {e}")


# if __name__ == "__main__":
#     # --- CONSOLIDATED SVG DATA LIST (INCLUDING IMAGES 1-63) ---
svg_data_list = [
        # Custom-defined Workspace Logo (from previous response)
        {"name": "Workspace-Logo-DD", "code": '<svg data-r2k="true" data-qa="team-icon" aria-hidden="false" viewBox="0 0 20 20" style="height: 36px; width: 36px; min-width: 36px; font-size: 20px; line-height: 36px; white-space: nowrap;"><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="12" fill="currentColor">DD</text></svg>'},

        # SVG Images 1-63
        {"name": "Arrow_Left", "code": '<svg data-r2k="true" data-qa="arrow-left" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M9.768 5.293a.75.75 0 0 0-1.036-1.086l-5.5 5.25a.75.75 0 0 0 0 1.085l5.5 5.25a.75.75 0 1 0 1.036-1.085L5.622 10.75H16.25a.75.75 0 0 0 0-1.5H5.622z" clip-rule="evenodd"></path></svg>'},
        {"name": "Arrow_Right", "code": '<svg data-r2k="true" data-qa="arrow-right" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M11.268 15.793a.75.75 0 0 1-1.036-1.085l4.146-3.958H3.75a.75.75 0 0 1 0-1.5h10.628l-4.146-3.957a.75.75 0 0 1 1.036-1.086l5.5 5.25a.75.75 0 0 1 0 1.085z" clip-rule="evenodd"></path></svg>'},
        {"name": "History_Clock", "code": '<svg data-r2k="true" data-qa="history" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M2.5 2.5v2.524A9 9 0 1 1 10 19a.75.75 0 0 1 0-1.5A7.5 7.5 0 1 0 3.239 6.75H6.75a.75.75 0 0 1 0 1.5h-5A.75.75 0 0 1 1 7.5v-5a.75.75 0 0 1 1.5 0m11.363 3.333a.75.75 0 1 0-1.226-.866l-3.25 4.6a.75.75 0 0 0 .083.963l3 3a.75.75 0 1 0 1.06-1.06l-2.553-2.553zM1.875 12a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5m1.875 2.5a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m2 3.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5" clip-rule="evenodd"></path></svg>'},
        {"name": "Search", "code": '<svg data-r2k="true" data-qa="search" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M9 3a6 6 0 1 0 0 12A6 6 0 0 0 9 3M1.5 9a7.5 7.5 0 1 1 13.307 4.746l3.473 3.474a.75.75 0 1 1-1.06 1.06l-3.473-3.473A7.5 7.5 0 0 1 1.5 9" clip-rule="evenodd"></path></svg>'},
        {"name": "Help_Question_Mark", "code": '<svg data-r2k="true" data-qa="help-icon" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M10 2.5a7.5 7.5 0 1 0 0 15 7.5 7.5 0 0 0 0-15M1 10a9 9 0 1 1 18 0 9 9 0 0 1-18 0m7.883-2.648c-.23.195-.383.484-.383.898a.75.75 0 0 1-1.5 0c0-.836.333-1.547.91-2.04.563-.48 1.31-.71 2.09-.71.776 0 1.577.227 2.2.729.642.517 1.05 1.294 1.05 2.271 0 .827-.264 1.515-.807 2.001-.473.423-1.08.623-1.693.703V12h-1.5v-1c0-.709.566-1.211 1.18-1.269.507-.048.827-.18 1.013-.347.162-.145.307-.39.307-.884 0-.523-.203-.87-.492-1.104C10.951 7.148 10.502 7 10 7c-.497 0-.876.146-1.117.352M10 15a1 1 0 1 0 0-2 1 1 0 0 0 0 2" clip-rule="evenodd"></path></svg>'},
        {"name": "Plus_Filled", "code": '<svg data-r2k="true" data-qa="plus-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M11 3.5a1 1 0 1 0-2 0V9H3.5a1 1 0 0 0 0 2H9v5.5a1 1 0 1 0 2 0V11h5.5a1 1 0 1 0 0-2H11z" clip-rule="evenodd"></path></svg>'},
        {"name": "Home_Filled", "code": '<svg data-r2k="true" data-qa="home-filled" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="m3 7.649-.33.223a.75.75 0 0 1-.84-1.244l7.191-4.852a1.75 1.75 0 0 1 1.958 0l7.19 4.852a.75.75 0 1 1-.838 1.244L17 7.649v7.011c0 2.071-1.679 3.84-3.75 3.84h-6.5C4.679 18.5 3 16.731 3 14.66zM11 11a1 1 0 0 1 1-1h1a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1z" clip-rule="evenodd"></path></svg>'},
        {"name": "Direct_Messages_Filled", "code": '<svg data-r2k="true" data-qa="direct-messages" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M7.675 6.468a4.75 4.75 0 1 1 8.807 3.441.75.75 0 0 0-.067.489l.379 1.896-1.896-.38a.75.75 0 0 0-.489.068 5 5 0 0 1-.648.273.75.75 0 1 0 .478 1.422q.314-.105.611-.242l2.753.55a.75.75 0 0 0 .882-.882l-.55-2.753A6.25 6.25 0 1 0 6.23 6.064a.75.75 0 1 0 1.445.404M6.5 8.5a5 5 0 0 0-4.57 7.03l-.415 2.073a.75.75 0 0 0 .882.882l2.074-.414A5 5 0 1 0 6.5 8.5m-3.5 5a3.5 3.5 0 1 1 1.91 3.119.75.75 0 0 0-.49-.068l-1.214.243.243-1.215a.75.75 0 0 0-.068-.488A3.5 3.5 0 0 1 3 13.5" clip-rule="evenodd"></path></svg>'},
        {"name": "Activity_Notifications", "code": '<svg data-r2k="true" data-qa="notifications" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M9.357 3.256c-.157.177-.31.504-.36 1.062l-.05.558-.55.11c-1.024.204-1.691.71-2.145 1.662-.485 1.016-.736 2.566-.752 4.857l-.002.307-.217.217-2.07 2.077c-.145.164-.193.293-.206.374a.3.3 0 0 0 .034.199c.069.12.304.321.804.321h4.665l.07.672c.034.327.17.668.4.915.214.232.536.413 1.036.413.486 0 .802-.178 1.013-.41.227-.247.362-.588.396-.916l.069-.674h4.663c.5 0 .735-.202.804-.321a.3.3 0 0 0 .034-.199c-.013-.08-.061-.21-.207-.374l-2.068-2.077-.216-.217-.002-.307c-.015-2.291-.265-3.841-.75-4.857-.455-.952-1.123-1.458-2.147-1.663l-.549-.11-.05-.557c-.052-.558-.204-.885-.36-1.062C10.503 3.1 10.31 3 10 3s-.505.1-.643.256m-1.124-.994C8.689 1.746 9.311 1.5 10 1.5s1.31.246 1.767.762c.331.374.54.85.65 1.383 1.21.369 2.104 1.136 2.686 2.357.604 1.266.859 2.989.894 5.185l1.866 1.874.012.012.011.013c.636.7.806 1.59.372 2.342-.406.705-1.223 1.072-2.103 1.072H12.77c-.128.39-.336.775-.638 1.104-.493.538-1.208.896-2.12.896-.917 0-1.638-.356-2.136-.893A3 3 0 0 1 7.23 16.5H3.843c-.88 0-1.697-.367-2.104-1.072-.433-.752-.263-1.642.373-2.342l.011-.013.012-.012 1.869-1.874c.035-2.196.29-3.919.894-5.185.582-1.22 1.475-1.988 2.684-2.357.112-.533.32-1.009.651-1.383" clip-rule="evenodd"></path></svg>'},
        {"name": "Files_Canvas_Browser", "code": '<svg data-r2k="true" data-qa="canvas-browser" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M4.836 3A1.836 1.836 0 0 0 3 4.836v7.328c0 .9.646 1.647 1.5 1.805V7.836A3.336 3.336 0 0 1 7.836 4.5h6.133A1.84 1.84 0 0 0 12.164 3zM1.5 12.164a3.337 3.337 0 0 0 3.015 3.32A3.337 3.337 0 0 0 7.836 18.5h3.968c.73 0 1.43-.29 1.945-.805l3.946-3.946a2.75 2.75 0 0 0 .805-1.945V7.836a3.337 3.337 0 0 0-3.015-3.32A3.337 3.337 0 0 0 12.164 1.5H4.836A3.336 3.336 0 0 0 1.5 4.836zM7.836 6A1.836 1.836 0 0 0 6 7.836v7.328C6 16.178 6.822 17 7.836 17H11.5v-4a1.5 1.5 0 0 1 1.5-1.5h4V7.836A1.836 1.836 0 0 0 15.164 6zm8.486 7H13v3.322z" clip-rule="evenodd"></path></svg>'},
        {"name": "Ellipsis_Horizontal", "code": '<svg data-r2k="true" data-qa="ellipsis-horizontal-filled" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" d="M14.5 10a1.75 1.75 0 1 1 3.5 0 1.75 1.75 0 0 1-3.5 0m-6.25 0a1.75 1.75 0 1 1 3.5 0 1.75 1.75 0 0 1-3.5 0M2 10a1.75 1.75 0 1 1 3.5 0A1.75 1.75 0 0 1 2 10"></path></svg>'},
        {"name": "Caret_Down_General", "code": '<svg data-r2k="true" data-qa="caret-down" aria-hidden="true" aria-label="caret-down" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M5.72 7.47a.75.75 0 0 1 1.06 0L10 10.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-3.75 3.75a.75.75 0 0 1-1.06 0L5.72 8.53a.75.75 0 0 1 0-1.06" clip-rule="evenodd"></path></svg>'},
        {"name": "Settings_Gear", "code": '<svg data-r2k="true" data-qa="settings" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="m9.151 3.676.271-1.108a2.5 2.5 0 0 1 1.156 0l.271 1.108a2 2 0 0 0 3.022 1.252l.976-.592a2.5 2.5 0 0 1 .817.817l-.592.975a2 2 0 0 0 1.252 3.023l1.108.27c.09.38.09.777 0 1.157l-1.108.27a2 2 0 0 0-1.252 3.023l.592.975a2.5 2.5 0 0 1-.817.818l-.976-.592a2 2 0 0 0-3.022 1.251l-.271 1.109a2.5 2.5 0 0 1-1.156 0l-.27-1.108a2 2 0 0 0-3.023-1.252l-.975.592a2.5 2.5 0 0 1-.818-.818l.592-.975a2 2 0 0 0-1.252-3.022l-1.108-.271a2.5 2.5 0 0 1 0-1.156l1.108-.271a2 2 0 0 0 1.252-3.023l-.592-.975a2.5 2.5 0 0 1 .818-.817l.975.592A2 2 0 0 0 9.15 3.676m2.335-2.39a4 4 0 0 0-2.972 0 .75.75 0 0 0-.45.518l-.372 1.523-.004.018a.5.5 0 0 1-.758.314l-.016-.01-1.34-.813a.75.75 0 0 0-.685-.048 4 4 0 0 0-2.1 2.1.75.75 0 0 0 .047.685l.814 1.34.01.016a.5.5 0 0 1-.314.759l-.018.004-1.523.372a.75.75 0 0 0-.519.45 4 4 0 0 0 0 2.971.75.75 0 0 0 .519.45l1.523.373.018.004a.5.5 0 0 1 .314.758l-.01.016-.814 1.34a.75.75 0 0 0-.048.685 4 4 0 0 0 2.101 2.1.75.75 0 0 0 .685-.048l1.34-.813.016-.01a.5.5 0 0 1 .758.314l.004.018.372 1.523a.75.75 0 0 0 .45.518 4 4 0 0 0 2.972 0 .75.75 0 0 0 .45-.518l.372-1.523.004-.018a.5.5 0 0 1 .758-.314l.016.01 1.34.813a.75.75 0 0 0 .685.049 4 4 0 0 0 2.101-2.101.75.75 0 0 0-.048-.685l-.814-1.34-.01-.016a.5.5 0 0 1 .314-.758l.018-.004 1.523-.373a.75.75 0 0 0 .519-.45 4 4 0 0 0 0-2.97.75.75 0 0 0-.519-.45l-1.523-.373-.018-.004a.5.5 0 0 1-.314-.759l.01-.015.814-1.34a.75.75 0 0 0 .048-.685 4 4 0 0 0-2.101-2.101.75.75 0 0 0-.685.048l-1.34.814-.016.01a.5.5 0 0 1-.758-.315l-.004-.017-.372-1.524a.75.75 0 0 0-.45-.518M8 10a2 2 0 1 1 4 0 2 2 0 0 1-4 0m2-3.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7" clip-rule="evenodd"></path></svg>'},
        {"name": "Compose_Pencil", "code": '<svg data-r2k="true" data-qa="compose" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M16.707 3.268a1 1 0 0 0-1.414 0l-.482.482 1.439 1.44.482-.483a1 1 0 0 0 0-1.414zM15.19 6.25l-1.44-1.44-5.068 5.069-.431 1.872 1.87-.432zm-.957-4.043a2.5 2.5 0 0 1 3.536 0l.025.025a2.5 2.5 0 0 1 0 3.536l-6.763 6.763a.75.75 0 0 1-.361.2l-3.25.75a.75.75 0 0 1-.9-.9l.75-3.25a.75.75 0 0 1 .2-.361zM5.25 4A2.25 2.25 0 0 0 3 6.25v8.5A2.25 2.25 0 0 0 5.25 17h8.5A2.25 2.25 0 0 0 16 14.75v-4.5a.75.75 0 0 1 1.5 0v4.5a3.75 3.75 0 0 1-3.75 3.75h-8.5a3.75 3.75 0 0 1-3.75-3.75v-8.5A3.75 3.75 0 0 1 5.25 2.5h4.5a.75.75 0 0 1 0 1.5z" clip-rule="evenodd"></path></svg>'},
        {"name": "Hourglass_Trial_Icon", "code": '<svg data-r2k="true" data-qa="hourglass" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M3.46 5.22A3.473 3.473 0 0 1 6.924 1.5h6.178a3.45 3.45 0 0 1 3.44 3.694 2.55 2.55 0 0 1-.638 1.511l-2.967 3.339a.25.25 0 0 0 .01.342l2.867 2.867c.428.429.688.997.731 1.602a3.403 3.403 0 0 1-3.394 3.645H6.876a3.43 3.43 0 0 1-3.42-3.672 2.54 2.54 0 0 1 .68-1.553l2.712-2.893a.25.25 0 0 0 .01-.331l-2.81-3.372A2.57 2.57 0 0 1 3.46 5.22M6.924 3c-1.145 0-2.05.971-1.968 2.113.016.223.102.435.245.606l2.81 3.372a1.75 1.75 0 0 1-.069 2.317L5.23 14.3c-.162.173-.26.397-.277.634A1.93 1.93 0 0 0 6.876 17h6.275a1.903 1.903 0 0 0 1.898-2.039 1.02 1.02 0 0 0-.296-.647l-2.867-2.867a1.75 1.75 0 0 1-.07-2.4l2.967-3.338c.154-.173.246-.392.262-.622A1.95 1.95 0 0 0 13.102 3zM13.5 15.65c0 .35-.887.35-3.5.35s-3.5 0-3.5-.35c0-.933 2.345-3.15 3.5-3.15 1.19 0 3.5 2.228 3.5 3.15m-1-9.025c0 .45-1.875 2.5-2.5 2.5s-2.5-2.1-2.5-2.5C7.5 6 8.125 6 10 6s2.5 0 2.5.625" clip-rule="evenodd"></path></svg>'},
        {"name": "Caret_Right", "code": '<svg data-r2k="true" data-qa="caret-right" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 24px;"><path fill="currentColor" fill-rule="evenodd" d="M7.72 5.72a.75.75 0 0 1 1.06 0l3.75 3.75a.75.75 0 0 1 0 1.06l-3.75 3.75a.75.75 0 0 1-1.06-1.06L10.94 10 7.72 6.78a.75.75 0 0 1 0-1.06" clip-rule="evenodd"></path></svg>'},
        {"name": "User_Directory_People", "code": '<svg data-r2k="true" data-qa="user-directory" aria-hidden="true" viewBox="0 0 20 20" class="is-inline" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M4.75 1.5A1.75 1.75 0 0 0 3 3.25v.5a.75.75 0 0 0 1.5 0v-.5A.25.25 0 0 1 4.75 3h10c.69 0 1.25.56 1.25 1.25v11.5c0 .69-.56 1.25-1.25 1.25h-10a.25.25 0 0 1-.25-.25v-.5a.75.75 0 0 0-1.5 0v.5c0 .966.784 1.75 1.75 1.75h10a2.75 2.75 0 0 0 2.75-2.75V4.25a2.75 2.75 0 0 0-2.75-2.75zM2.25 6a.75.75 0 0 0 0 1.5h2a.75.75 0 0 0 0-1.5zm-.75 4a.75.75 0 0 1 .75-.75h2a.75.75 0 0 1 0 1.5h-2A.75.75 0 0 1 1.5 10m.75 2.5a.75.75 0 0 0 0 1.5h2a.75.75 0 0 0 0-1.5zm5.79.472.02.01q.037.016.09.018h4.7a.23.23 0 0 0 .11-.028 2.1 2.1 0 0 0-.736-.991c-.372-.271-.92-.481-1.724-.481-.805 0-1.353.21-1.724.481a2.1 2.1 0 0 0-.736.991m4.12-2.702q.117-.13.218-.268C12.784 9.437 13 8.712 13 8c0-1.624-1.287-2.5-2.5-2.5S8 6.376 8 8c0 .712.217 1.437.622 2.002q.1.139.219.268-.53.191-.949.5a3.6 3.6 0 0 0-1.285 1.755 1.42 1.42 0 0 0 .294 1.431 1.68 1.68 0 0 0 1.249.544h4.7a1.68 1.68 0 0 0 1.249-.544 1.42 1.42 0 0 0 .293-1.431 3.6 3.6 0 0 0-2.233-2.255M9.5 8c0-.65.463-1 1-1s1 .35 1 1c0 .426-.133.838-.34 1.127-.203.282-.434.398-.66.398s-.457-.116-.66-.398A2 2 0 0 1 9.5 8" clip-rule="evenodd"></path></svg>'},
        {"name": "Starred_Section", "code": '<svg data-r2k="true" data-qa="star" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M9.044 4.29c-.393.923-.676 2.105-.812 3.065a.75.75 0 0 1-.825.64l-.25-.027c-1.066-.12-2.106-.236-2.942-.202-.45.018-.773.079-.98.167-.188.08-.216.15-.227.187-.013.042-.027.148.112.37.143.229.4.497.77.788.734.579 1.755 1.128 2.66 1.54a.75.75 0 0 1 .35 1.036c-.466.87-1.022 2.125-1.32 3.239-.15.56-.223 1.04-.208 1.396.015.372.113.454.124.461l.003.001a.2.2 0 0 0 .042.006.9.9 0 0 0 .297-.06c.297-.1.678-.319 1.116-.64.87-.635 1.8-1.55 2.493-2.275a.75.75 0 0 1 1.085 0c.692.724 1.626 1.639 2.5 2.275.44.32.822.539 1.12.64a.9.9 0 0 0 .3.06q.038-.003.044-.006h.002c.011-.009.109-.09.123-.46.013-.357-.06-.836-.212-1.397-.303-1.114-.864-2.368-1.33-3.24a.75.75 0 0 1 .35-1.037c.903-.41 1.92-.96 2.652-1.54.369-.292.625-.56.768-.787.139-.223.124-.329.112-.37-.012-.038-.039-.107-.226-.186-.206-.088-.527-.149-.976-.167-.835-.034-1.874.082-2.941.201l-.246.027a.75.75 0 0 1-.825-.64c-.136-.96-.42-2.142-.813-3.064-.198-.464-.405-.82-.605-1.048-.204-.232-.319-.243-.34-.243s-.135.01-.34.243c-.2.228-.407.584-.605 1.048m-.522-2.036c.343-.39.833-.754 1.467-.754s1.125.363 1.467.754c.348.396.63.914.858 1.449.359.84.627 1.83.798 2.723.913-.1 1.884-.192 2.708-.158.521.021 1.052.094 1.503.285.47.2.902.556 1.076 1.14.177.597-.004 1.153-.279 1.592-.271.434-.676.826-1.108 1.168-.662.524-1.482 1.003-2.256 1.392.41.85.836 1.884 1.1 2.856.17.625.286 1.271.264 1.846-.021.56-.182 1.218-.749 1.623-.555.398-1.205.316-1.7.148-.51-.173-1.034-.493-1.523-.849-.754-.55-1.523-1.261-2.158-1.896-.634.634-1.4 1.346-2.15 1.895-.487.356-1.01.677-1.518.85-.495.168-1.144.25-1.699-.148-.565-.405-.727-1.062-.75-1.62-.024-.574.09-1.22.257-1.846.261-.972.684-2.007 1.093-2.858-.775-.389-1.597-.867-2.262-1.39-.433-.342-.84-.734-1.111-1.168-.276-.44-.457-.997-.28-1.595.174-.585.608-.941 1.079-1.141.45-.191.983-.264 1.505-.285.826-.033 1.799.059 2.713.159.17-.893.439-1.882.797-2.723.228-.535.51-1.053.858-1.449" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Section_Collapse", "code": '<svg data-r2k="true" data-qa="channel-section-collapse" aria-hidden="true" viewBox="0 0 20 20" class="is-inline"><path fill="currentColor" d="M13.22 9.423a.75.75 0 0 1 .001 1.151l-4.49 3.755a.75.75 0 0 1-1.231-.575V6.25a.75.75 0 0 1 1.23-.575z"></path></svg>'},
        {"name": "Ellipsis_Vertical", "code": '<svg data-r2k="true" data-qa="ellipsis-vertical-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10 5.5A1.75 1.75 0 1 1 10 2a1.75 1.75 0 0 1 0 3.5m0 6.25a1.75 1.75 0 1 1 0-3.5 1.75 1.75 0 0 1 0 3.5m-1.75 4.5a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Section_Expand", "code": '<svg data-r2k="true" data-qa="channel-section-collapse" aria-hidden="true" viewBox="0 0 20 20" class="is-inline"><path fill="currentColor" d="M13.22 9.423a.75.75 0 0 1 .001 1.151l-4.49 3.755a.75.75 0 0 1-1.231-.575V6.25a.75.75 0 0 1 1.23-.575z"></path></svg>'},
        {"name": "Ellipsis_Vertical_Channels", "code": '<svg data-r2k="true" data-qa="ellipsis-vertical-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10 5.5A1.75 1.75 0 1 1 10 2a1.75 1.75 0 0 1 0 3.5m0 6.25a1.75 1.75 0 1 1 0-3.5 1.75 1.75 0 0 1 0 3.5m-1.75 4.5a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Hashtag_1", "code": '<svg data-r2k="true" data-qa="sidebar-channel-icon-prefix" aria-hidden="true" data-sidebar-channel-icon="channel" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M9.74 3.878a.75.75 0 1 0-1.48-.255L7.68 7H3.75a.75.75 0 0 0 0 1.5h3.67L6.472 14H2.75a.75.75 0 0 0 0 1.5h3.463l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.228l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.765a.75.75 0 0 0 0-1.5h-3.506l.948-5.5h3.558a.75.75 0 0 0 0-1.5h-3.3l.54-3.122a.75.75 0 0 0-1.48-.255L12.43 7H9.2zM11.221 14l.948-5.5H8.942L7.994 14z" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Hashtag_2", "code": '<svg data-r2k="true" data-qa="sidebar-channel-icon-prefix" aria-hidden="true" data-sidebar-channel-icon="channel" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M9.74 3.878a.75.75 0 1 0-1.48-.255L7.68 7H3.75a.75.75 0 0 0 0 1.5h3.67L6.472 14H2.75a.75.75 0 0 0 0 1.5h3.463l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.228l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.765a.75.75 0 0 0 0-1.5h-3.506l.948-5.5h3.558a.75.75 0 0 0 0-1.5h-3.3l.54-3.122a.75.75 0 0 0-1.48-.255L12.43 7H9.2zM11.221 14l.948-5.5H8.942L7.994 14z" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Hashtag_3", "code": '<svg data-r2k="true" data-qa="sidebar-channel-icon-prefix" aria-hidden="true" data-sidebar-channel-icon="channel" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M9.74 3.878a.75.75 0 1 0-1.48-.255L7.68 7H3.75a.75.75 0 0 0 0 1.5h3.67L6.472 14H2.75a.75.75 0 0 0 0 1.5h3.463l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.228l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.765a.75.75 0 0 0 0-1.5h-3.506l.948-5.5h3.558a.75.75 0 0 0 0-1.5h-3.3l.54-3.122a.75.75 0 0 0-1.48-.255L12.43 7H9.2zM11.221 14l.948-5.5H8.942L7.994 14z" clip-rule="evenodd"></path></svg>'},
        {"name": "Channel_Hashtag_4", "code": '<svg data-r2k="true" data-qa="sidebar-channel-icon-prefix" aria-hidden="true" data-sidebar-channel-icon="channel" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M9.74 3.878a.75.75 0 1 0-1.48-.255L7.68 7H3.75a.75.75 0 0 0 0 1.5h3.67L6.472 14H2.75a.75.75 0 0 0 0 1.5h3.463l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.228l-.452 2.623a.75.75 0 0 0 1.478.255l.496-2.878h3.765a.75.75 0 0 0 0-1.5h-3.506l.948-5.5h3.558a.75.75 0 0 0 0-1.5h-3.3l.54-3.122a.75.75 0 0 0-1.48-.255L12.43 7H9.2zM11.221 14l.948-5.5H8.942L7.994 14z" clip-rule="evenodd"></path></svg>'},
        {"name": "DM_Section_Collapse", "code": '<svg data-r2k="true" data-qa="channel-section-collapse" aria-hidden="true" viewBox="0 0 20 20" class="is-inline"><path fill="currentColor" d="M13.22 9.423a.75.75 0 0 1 .001 1.151l-4.49 3.755a.75.75 0 0 1-1.231-.575V6.25a.75.75 0 0 1 1.23-.575z"></path></svg>'},
        {"name": "Plus_DM_Section", "code": '<svg data-r2k="true" data-qa="plus" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10.75 3.25a.75.75 0 0 0-1.5 0v6H3.251L3.25 10v-.75a.75.75 0 0 0 0 1.5V10v.75h6v6a.75.75 0 0 0 1.5 0v-6h6a.75.75 0 0 0 0-1.5h-6z" clip-rule="evenodd"></path></svg>'},
        {"name": "Ellipsis_Vertical_DMs", "code": '<svg data-r2k="true" data-qa="ellipsis-vertical-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10 5.5A1.75 1.75 0 1 1 10 2a1.75 1.75 0 0 1 0 3.5m0 6.25a1.75 1.75 0 1 1 0-3.5 1.75 1.75 0 0 1 0 3.5m-1.75 4.5a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Avatar_Mask_Small_DND", "code": '<svg class="sr-only"><clipPath id="mask__small-member-dnd" clipPathUnits="objectBoundingBox"><path d="M1,0 H0 V1 H0.752 C0.701,0.949,0.669,0.878,0.669,0.8 C0.669,0.674,0.752,0.567,0.867,0.531 C0.888,0.48,0.938,0.444,0.997,0.444 H1 V0"></path></clipPath></svg>'},
        {"name": "Presence_Away_DND", "code": '<svg data-r2k="true" data-qa="presence_indicator" aria-hidden="false" title="Away, notifications snoozed" aria-label="Away, notifications snoozed" data-qa-type="status-member-dnd" data-qa-presence-self="false" data-qa-presence-active="false" data-qa-presence-dnd="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M11.25 3.5a.75.75 0 0 0 0 1.5h1.847l-2.411 2.756A.75.75 0 0 0 11.25 9h3.5a.75.75 0 0 0 0-1.5h-1.847l2.411-2.756A.75.75 0 0 0 14.75 3.5zM7 10a3 3 0 0 1 3-3V5.5a4.5 4.5 0 1 0 4.5 4.5H13a3 3 0 1 1-6 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Avatar_Mask_Small_DND_2", "code": '<svg class="sr-only"><clipPath id="mask__small-member-dnd" clipPathUnits="objectBoundingBox"><path d="M1,0 H0 V1 H0.752 C0.701,0.949,0.669,0.878,0.669,0.8 C0.669,0.674,0.752,0.567,0.867,0.531 C0.888,0.48,0.938,0.444,0.997,0.444 H1 V0"></path></clipPath></svg>'},
        {"name": "Presence_Active_DND", "code": '<svg data-r2k="true" data-qa="presence_indicator" aria-hidden="false" title="Active, notifications snoozed" aria-label="Active, notifications snoozed" data-qa-type="status-member-dnd-filled" data-qa-presence-self="true" data-qa-presence-active="true" data-qa-presence-dnd="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M11.25 3.5a.75.75 0 0 0 0 1.5h1.847l-2.411 2.756A.75.75 0 0 0 11.25 9h3.5a.75.75 0 0 0 0-1.5h-1.847l2.411-2.756A.75.75 0 0 0 14.75 3.5zM9.557 6.768C10.18 6.055 10 5.5 9.406 5.54a4.5 4.5 0 1 0 5.067 4.96H11.25a2.25 2.25 0 0 1-1.693-3.73" clip-rule="evenodd"></path></svg>'},
        {"name": "Apps_Section_Collapse", "code": '<svg data-r2k="true" data-qa="channel-section-collapse" aria-hidden="true" viewBox="0 0 20 20" class="is-inline"><path fill="currentColor" d="M13.22 9.423a.75.75 0 0 1 .001 1.151l-4.49 3.755a.75.75 0 0 1-1.231-.575V6.25a.75.75 0 0 1 1.23-.575z"></path></svg>'},
        {"name": "Ellipsis_Vertical_Apps", "code": '<svg data-r2k="true" data-qa="ellipsis-vertical-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10 5.5A1.75 1.75 0 1 1 10 2a1.75 1.75 0 0 1 0 3.5m0 6.25a1.75 1.75 0 1 1 0-3.5 1.75 1.75 0 0 1 0 3.5m-1.75 4.5a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Avatar_Mask_Small_DND_3", "code": '<svg class="sr-only"><clipPath id="mask__small-member-dnd" clipPathUnits="objectBoundingBox"><path d="M1,0 H0 V1 H0.752 C0.701,0.949,0.669,0.878,0.669,0.8 C0.669,0.674,0.752,0.567,0.867,0.531 C0.888,0.48,0.938,0.444,0.997,0.444 H1 V0"></path></clipPath></svg>'},
        {"name": "Presence_Harsh_DND", "code": '<svg data-r2k="true" data-qa="presence_indicator" aria-hidden="false" title="Away, notifications snoozed" aria-label="Away, notifications snoozed" data-qa-type="status-member-dnd" data-qa-presence-self="false" data-qa-presence-active="false" data-qa-presence-dnd="true" viewBox="0 0 20 20" class="is-inline" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M11.25 3.5a.75.75 0 0 0 0 1.5h1.847l-2.411 2.756A.75.75 0 0 0 11.25 9h3.5a.75.75 0 0 0 0-1.5h-1.847l2.411-2.756A.75.75 0 0 0 14.75 3.5zM7 10a3 3 0 0 1 3-3V5.5a4.5 4.5 0 1 0 4.5 4.5H13a3 3 0 1 1-6 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Huddle_Button_Slider", "code": '<svg xmlns="http://www.w3.org/2000/svg" height="26" width="57" class="p-huddle_channel_header_button__slider_container" aria-hidden="true"><clipPath id="sliderClip"><rect width="100%" height="100%" rx="6"></rect></clipPath><g clip-path="url(#sliderClip)"><rect id="p-huddle_channel_header_button__slider" class="p-huddle_channel_header_button__slider" width="100%" height="100%"></rect></g></svg>'},
        {"name": "Huddle_Start_Headphones", "code": '<svg data-r2k="true" data-qa="headphones" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M5.094 4.571C3.785 5.825 3 7.444 3 8.966v1.371A3.45 3.45 0 0 1 5.25 9.5h.5c1.064 0 1.75.957 1.75 1.904v5.192c0 .947-.686 1.904-1.75 1.904h-.5c-2.168 0-3.75-1.99-3.75-4.211v-.578q0-.105.005-.211H1.5V8.966c0-2.02 1.024-4.01 2.556-5.478C5.595 2.014 7.711 1 10 1s4.405 1.014 5.944 2.488C17.476 4.956 18.5 6.945 18.5 8.966V13.5h-.005q.005.105.005.211v.578c0 2.221-1.582 4.211-3.75 4.211h-.5c-1.064 0-1.75-.957-1.75-1.904v-5.192c0-.947.686-1.904 1.75-1.904h.5c.864 0 1.635.316 2.25.837V8.966c0-1.522-.785-3.141-2.094-4.395C13.602 3.322 11.844 2.5 10 2.5s-3.602.822-4.906 2.071m9.016 6.508a.5.5 0 0 0-.11.325v5.192c0 .145.05.257.11.325.057.066.109.079.14.079h.5c1.146 0 2.25-1.11 2.25-2.711v-.578C17 12.11 15.896 11 14.75 11h-.5c-.031 0-.083.013-.14.08M3 13.711C3 12.11 4.105 11 5.25 11h.5c.031 0 .083.013.14.08.06.067.11.18.11.324v5.192a.5.5 0 0 1-.11.325c-.057.066-.109.079-.14.079h-.5C4.105 17 3 15.89 3 14.289z" clip-rule="evenodd"></path></svg>'},
        {"name": "Huddle_Options_Caret", "code": '<svg data-r2k="true" data-qa="caret-down" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M5.72 7.47a.75.75 0 0 1 1.06 0L10 10.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-3.75 3.75a.75.75 0 0 1-1.06 0L5.72 8.53a.75.75 0 0 1 0-1.06" clip-rule="evenodd"></path></svg>'},
        {"name": "View_Header_Actions_Menu", "code": '<svg data-r2k="true" data-qa="ellipsis-vertical-filled" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M10 5.5A1.75 1.75 0 1 1 10 2a1.75 1.75 0 0 1 0 3.5m0 6.25a1.75 1.75 0 1 1 0-3.5 1.75 1.75 0 0 1 0 3.5m-1.75 4.5a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0" clip-rule="evenodd"></path></svg>'},
        {"name": "Tab_Messages_Icon", "code": '<svg data-r2k="true" data-qa="message-filled" aria-hidden="true" viewBox="0 0 20 20" class="is-inline" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M10 1.5a8.5 8.5 0 1 0 3.859 16.075l3.714.904a.75.75 0 0 0 .906-.906l-.904-3.714A8.5 8.5 0 0 0 10 1.5" clip-rule="evenodd"></path></svg>'},
        {"name": "Tab_More_Options_Caret", "code": '<svg data-r2k="true" data-qa="caret-down" aria-hidden="true" viewBox="0 0 20 20" class=""><path fill="currentColor" fill-rule="evenodd" d="M5.72 7.47a.75.75 0 0 1 1.06 0L10 10.69l3.22-3.22a.75.75 0 1 1 1.06 1.06l-3.75 3.75a.75.75 0 0 1-1.06 0L5.72 8.53a.75.75 0 0 1 0-1.06" clip-rule="evenodd"></path></svg>'},
        {"name": "Tab_Add_Filled_Plus", "code": '<svg data-r2k="true" data-qa="plus-filled" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M11 3.5a1 1 0 1 0-2 0V9H3.5a1 1 0 0 0 0 2H9v5.5a1 1 0 1 0 2 0V11h5.5a1 1 0 1 0 0-2H11z" clip-rule="evenodd"></path></svg>'},
        {"name": "Canvas_File_Icon", "code": '<svg data-r2k="true" data-qa="canvas-content" aria-hidden="true" viewBox="0 0 20 20" class="" style="--s: 16px;"><path fill="currentColor" fill-rule="evenodd" d="M3 5.25A2.25 2.25 0 0 1 5.25 3h9.5A2.25 2.25 0 0 1 17 5.25v5.5h-4.75a1.5 1.5 0 0 0-1.5 1.5V17h-5.5A2.25 2.25 0 0 1 3 14.75zm9.25 11.003 4.003-4.003H12.25zM5.25 1.5A3.75 3.75 0 0 0 1.5 5.25v9.5a3.75 3.75 0 0 0 3.75 3.75h5.736c.729 0 1.428-.29 1.944-.805l4.765-4.765a2.75 2.75 0 0 0 .805-1.944V5.25a3.75 3.75 0 0 0-3.75-3.75zm.25 4.75a.75.75 0 0 1 .75-.75h7.5a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1-.75-.75m.75 2.25a.75.75 0 0 0 0 1.5h2a.75.75 0 0 0 0-1.5z" clip-rule="evenodd"></path></svg>'},
        {"name": "Message_Pane_Harsh_DND", "code": '<svg data-r2k="true" data-qa="presence_indicator" aria-hidden="false" title="Away, notifications snoozed" aria-label="Away, notifications snoozed" data-qa-type="status-member-dnd" data-qa-presence-self="false" data-qa-presence-active="false" data-qa-presence-dnd="true" viewBox="0 0 20 20" class="is-inline" style="--s: 20px;"><path fill="currentColor" fill-rule="evenodd" d="M11.25 3.5a.75.75 0 0 0 0 1.5h1.847l-2.411 2.756A.75.75 0 0 0 11.25 9h3.5a.75.75 0 0 0 0-1.5h-1.847l2.411-2.756A.75.75 0 0 0 14.75 3.5zM7 10a3 3 0 0 1 3-3V5.5a4.5 4.5 0 1 0 4.5 4.5H13a3 3 0 1 1-6 0" clip-rule="evenodd"></path></svg>'}]
        

import os
import re
import csv
from tqdm import tqdm

# === SETTINGS ===
OUTPUT_DIR = "extracted_svgs"
CSV_FILE = None  # or e.g. "icons.csv" if using CSV input


# === SANITIZE FILENAMES ===
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


# === READ FROM CSV (optional) ===
def read_from_csv(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "name" in row and "code" in row:
                data.append({"name": row["name"], "code": row["code"]})
    return data


# === MAIN FUNCTION TO SAVE SVG FILES ===
def save_svg_from_data(svg_data_list):
    print("Starting SVG extraction process...")
    output_path = os.path.join(os.getcwd(), OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)
    print(f"Output directory: '{output_path}'")

    file_count = 0

    for item in tqdm(svg_data_list, desc="Saving SVGs"):
        name, code = item.get("name"), item.get("code")
        if not name or not code:
            continue

        sanitized_name = sanitize_filename(name) or "unnamed_icon"
        file_path = os.path.join(output_path, f"{sanitized_name}.svg")

        # Skip if file already exists
        if os.path.exists(file_path):
            continue

        # Extract SVG content properly
        svg_content = code
        if not code.strip().startswith("<?xml"):
            match = re.search(r"(<svg.*?</svg>)", code, re.DOTALL | re.IGNORECASE)
            if match:
                svg_content = match.group(1)

        try:
            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(svg_content)
            file_count += 1
        except IOError as e:
            print(f"Error writing {file_path}: {e}")

    print(f"\n✅ {file_count} SVG files saved to '{output_path}/'")


# === SAMPLE DATA ===



# === RUN SCRIPT ===
if __name__ == "__main__":
    if CSV_FILE and os.path.exists(CSV_FILE):
        svg_data_list = read_from_csv(CSV_FILE)
    save_svg_from_data(svg_data_list)
