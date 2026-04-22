import json

filepath = r'c:\Users\VICTUS\Downloads\Fraud-Risk Sentinel – Scores suspicious high-value order.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['name'] == 'True':
        node['type'] = 'n8n-nodes-base.code'
        node['typeVersion'] = 2
        node['parameters'] = {
            'jsCode': "return items.map(item => {\n  item.json.action = 'Zendesk ticket + Hold order';\n  return item;\n});"
        }
    elif node['name'] == 'False':
        node['type'] = 'n8n-nodes-base.code'
        node['typeVersion'] = 2
        node['parameters'] = {
            'jsCode': "return items.map(item => {\n  item.json.action = 'Continue';\n  return item;\n});"
        }
    
    # Also fix the JS Code so shipping names aren't strictly lowercase for UI appearance
    if node['name'] == 'Code in JavaScript':
        code = node['parameters'].get('jsCode', '')
        code = code.replace('shipping = shipping.trim().toLowerCase();', 'let shipCompare = shipping.trim().toLowerCase();')
        code = code.replace('billing = billing.trim().toLowerCase();', 'let billCompare = billing.trim().toLowerCase();')
        code = code.replace('shipping !== billing', 'shipCompare !== billCompare')
        node['parameters']['jsCode'] = code

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('Successfully rebuilt True and False nodes as bulletproof Code nodes!')
