import logging

# expand this for MAD
recordFields = [
('avid', 'AVID', 'Avox identifier'),
('legal_name', 'Legal Name', 'Legal name as per the registration document'),
('previous_name_s_', 'Previous Name(s)', 'Previous legal names'),
('trades_as_name_s_', 'Trades As Name(s)', 'Names under which the company trades but which differ from their legal name'),
('trading_status', 'Trading Status', 'Defines the trading status of the entity, e,g, Active'),
('company_website', 'Company Website', 'URL'),
('operational_po_box', 'Operational PO Box', 'Operational address information'),
('operational_floor', 'Operational Floor', 'Operational address information'),
('operational_building', 'Operational Building', 'Operational address information'),
('operational_street_1', 'Operational Street 1', 'Operational address information'),
('operational_street_2', 'Operational Street 2', 'Operational address information'),
('operational_street_3', 'Operational Street 3', 'Operational address information'),
('operational_city', 'Operational City', 'Operational City'),
('operational_state', 'Operational State', 'Operational State, Province, Region or Territory'),
('operational_country', 'Operational Country', 'Operational address information'),
('operational_postcode', 'Operational Postcode', 'Operational address information'),
('registered_country', 'Registered Country', 'Registered address information')
];

def getFields(environ):
    fields = []
    openfields = environ['tiddlyweb.config']['mappingsql.open_fields']
    for field, label, tooltip in recordFields:
        if field in openfields:
            fields.append((field,label,tooltip))
    logging.debug('fields passed: %s', fields)
    return fields
