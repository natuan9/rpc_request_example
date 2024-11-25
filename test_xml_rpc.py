# Read more: https://www.odoo.com/documentation/18.0/developer/reference/external_api.html
import xmlrpc.client


# Param
url='http://127.0.18.1:8069'
db='v18c_rpc_helper'
username='admin'
password='admin'

# Check version
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
#print("Version: ", version)

# Login
uid = common.authenticate(db, username, password, {})
print("UID", uid)

# Read Record
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
result_read = models.execute_kw(db, uid, password, 'res.partner', 'read', [27], {'fields': ['name', 'country_id', 'comment']})
print("--- Read Record ---")
print("Result: ", result_read)
