import json
import os
import sys
import glob
from natsort import natsorted

def merge_api_files(product_name):
    """
    Merges multiple API version files for a product into a single file.

    The merging strategy is as follows:
    1.  Files are sorted by version in descending order (latest first).
    2.  Info: The 'info' block from the latest version file is used.
    3.  APIs: API definitions are merged. If an API with the same name
        exists in multiple files, the definition from the newest version
        is kept, and older ones are discarded.
    4.  Endpoints: All endpoints from all files are collected and then
        deduplicated to create a unique list.
    """
    source_pattern = f'apis/{product_name}-*.apis.json'
    file_list = glob.glob(source_pattern)

    if not file_list:
        print(f"No files found for product '{product_name}' with pattern '{source_pattern}'")
        # If a single file like `workorder.apis.json` exists, we can just rename it.
        single_file = f'apis/{product_name}.apis.json'
        if os.path.exists(single_file):
             print(f"Found single file {single_file}, no merge needed.")
        return

    # Sort files naturally to handle version numbers correctly
    sorted_files = natsorted(file_list, reverse=True)
    
    print(f"Found {len(sorted_files)} files to merge for product '{product_name}':")
    for f in sorted_files:
        print(f"- {f}")

    merged_data = {
        "info": {},
        "apis": {},
        "endpoints": []
    }

    all_endpoints = []

    for file_path in sorted_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Merge APIs
            if 'apis' in data:
                for api_name, api_details in data['apis'].items():
                    if api_name not in merged_data['apis']:
                        merged_data['apis'][api_name] = api_details

            # Collect endpoints
            if 'endpoints' in data:
                all_endpoints.extend(data['endpoints'])

    # Use the info from the latest version file (first in sorted list)
    if sorted_files:
        with open(sorted_files[0], 'r', encoding='utf-8') as f:
            latest_data = json.load(f)
            merged_data['info'] = latest_data.get('info', {})

    # Deduplicate endpoints
    unique_endpoints = {}
    for endpoint in all_endpoints:
        # Use a tuple of items as a key to handle unhashable dicts
        endpoint_key = tuple(sorted(endpoint.items()))
        if endpoint_key not in unique_endpoints:
            unique_endpoints[endpoint_key] = endpoint
    
    merged_data['endpoints'] = list(unique_endpoints.values())

    output_file = f'apis/{product_name}.apis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully merged files into '{output_file}'")
    print(f"Total APIs: {len(merged_data['apis'])}")
    print(f"Total Endpoints: {len(merged_data['endpoints'])}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python merge_apis.py <product_name>")
        sys.exit(1)
    
    product_name = sys.argv[1]
    merge_api_files(product_name)

if __name__ == '__main__':
    main()
