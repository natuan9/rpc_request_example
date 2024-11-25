import json
import random
import urllib.request

# Param
URL = 'http://127.0.18.1:8069'
DB = 'v18c_rpc_helper'
USER = 'admin'
PASS = 'admin'

# See function details in Web Services Odoo documentation
def json_rpc(url, method, params):
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
        "Content-Type":"application/json",
    })
    reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
    if reply.get("error"):
        raise Exception(reply["error"])
    return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

# Log in the given database
url = f"{URL}/jsonrpc"
uid = call(url, "common", "login", DB, USER, PASS)

# List Partner records
result_list = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'search', [[['is_company', '=', True]]])
print("\n--- List Records ---")
print("Id: ", result_list)

# Pagination Partner records
result_pagination = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'search', [[['is_company', '=', True]]], {'offset': 3, 'limit': 5})
print("\n--- Pagination Records ---")
print("Id: ", result_pagination)

# Count Partner records
result_count = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'search_count', [[['is_company', '=', True]]])
print("\n--- Count Records ---")
print("Id: ", result_count)

# Read Partner record
result_read = call(url, "object", "execute", DB, uid, PASS, 'res.partner', 'read', [27])
print("\n--- Read Record ---")
print("Id: ", result_read[0]['id'])
print("Name: ", result_read[0]['name'])

# Read Partner with execute_kw method
# execute_kw is an enhanced version of execute that supports both positional arguments and keyword arguments, providing more flexibility.
result_read_kw = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'read', 
              [27], 
              {'fields': ['name', 'email']})
print("\n--- Read Record with kw ---")
print("Result read kw: ", result_read_kw)

# List record fields
result_list_fields = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'fields_get', [], {'attributes': ['string', 'type']})
print("\n--- List record fields ---")
print("Id: ", result_list_fields)

# Search and read
result_search_read = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'search_read', [[['is_company', '=', True]]], 
                          {'fields': ['name', 'country_id', 'comment'], 'limit': 5})
print("\n--- Search and read ---")
print("Id: ", result_search_read)

# Create records
# result_create = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'create', [{'name': "New Partner"}])
# print("\n--- Create records ---")
# print("Id: ", result_create)

# Update records
# result_update = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'write', [[42], {'name': "Newer partner"}])
# result_update = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'read', [[42], ['display_name']])
# print("\n--- Update records ---")
# print("Id: ", result_update)

# Delete records
# result_delete = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'unlink', [[42]])
# result_delete = call(url, "object", "execute_kw", DB, uid, PASS, 'res.partner', 'search', [[['id', '=', 42]]])
# print("\n--- Delete records ---")
# print("Id: ", result_delete)