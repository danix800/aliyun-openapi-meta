import json
import os
import sys

def convert_type(param_schema):
    """Converts parameter type based on schema."""
    param_type = param_schema.get('type', 'string')
    param_format = param_schema.get('format')
    if param_type == 'integer' and param_format == 'int64':
        return 'Long'
    return param_type.capitalize()

def transform_api(lang, api_name, api_details):
    """Transforms a single API definition."""
    parameters = []
    if 'parameters' in api_details:
        for param in api_details['parameters']:
            if 'schema' in param:
                p = {
                    'name': param.get('name'),
                    'position': param.get('in', '').capitalize(),
                    'type': convert_type(param['schema']),
                    'required': param['schema'].get('required', False),
                }

                if lang != "metadatas":
                    p["description"] = param['schema'].get('description', '')

                parameters.append(p)

    methods = api_details.get('methods', api_details.get('method', []))
    protocols = api_details.get('schemes', api_details.get('protocol', []))

    return {
        'name': api_name,
        'protocol': '|'.join(p.upper() for p in protocols),
        'method': '|'.join(m.upper() for m in methods),
        'pathPattern': api_details.get('pathPattern', ''),
        'parameters': parameters
    }

def main():
    """Main function to run the conversion."""
    if len(sys.argv) < 2:
        print("Usage: python convert_api.py <product_name>")
        sys.exit(1)

    product_name = sys.argv[1]
    source_file = f'apis/{product_name}.apis.json'

    if not os.path.exists(source_file):
        print(f"Source file {source_file} not found.")
        sys.exit(1)

    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    product_info = source_data.get('info', {})
    product_code = product_info.get('title', product_name).capitalize()

    for lang in ['zh-CN', 'en-US', 'metadatas']:
        output_dir = f'../{lang}/{product_name}/'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        apis = source_data.get('apis', {})
        api_names = list(apis.keys())

        for api_name, api_details in apis.items():
            transformed_data = transform_api(lang, api_name, api_details)
            output_file = os.path.join(output_dir, f"{api_name}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(transformed_data, f, indent=2, ensure_ascii=False)
            print(f"Successfully converted {api_name} to {output_file}")

        products_file = f'../{lang}/products.json'
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
        else:
            products_data = {"products": []}

        product_entry = next((p for p in products_data['products'] if p['code'] == product_code), None)

        if product_entry:
            product_entry['apis'] = sorted(list(set(product_entry.get('apis', []) + api_names)))
        else:
            endpoints = source_data.get('endpoints', [])
            regional_endpoints = {e['regionId']: e['endpoint'] for e in endpoints}

            product_entry = {
                "code": product_code,
                "version": product_info.get('version', ''),
                "name": {
                    "en": product_info.get('title', ''),
                    "zh": product_info.get('title', '')
                },
                "location_service_code": "",
                "regional_endpoints": regional_endpoints,
                "global_endpoint": "",
                "api_style": "rpc",
                "apis": sorted(api_names)
            }
            products_data['products'].append(product_entry)

        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully updated {products_file}")

if __name__ == '__main__':
    main()
