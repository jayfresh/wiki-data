import logging

recordFields = [
        ('legal_name', 'Legal Name'),
        ('previous_name_s_', 'Previous Name(s)'),
        ('trades_as_name_s_', 'Trades As Name(s)'),
        ('trading_status', 'Trading Status'),
        ('company_website', 'Company Website'),
        ('operational_po_box', 'Operational PO Box'),
        ('operational_floor', 'Operational Floor'),
        ('operational_building', 'Operational Building'),
        ('operational_street_1', 'Operational Street 1'),
        ('operational_street_2', 'Operational Street 2'),
        ('operational_street_3', 'Operational Street 3'),
        ('operational_city', 'Operational City'),
        ('operational_state', 'Operational State'),
        ('operational_country', 'Operational Country'),
        ('operational_postcode', 'Operational Postcode'),
        ('registered_country', 'Registered Country')
]

def getFields(environ):
    fields = []
    openfields = environ['tiddlyweb.config']['mappingsql.open_fields']
    for field, label in recordFields:
        if field in openfields:
            fields.append((field, label))
    logging.debug('fields passed: %s', fields)
    return fields
