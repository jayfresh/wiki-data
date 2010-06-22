import logging

# expand this for MAD
recordFields = [
('avid', 'AVID', 'Avox identifier'),
#('avox_match_status', 'Avox Match Status', 'Match, Enrich, Collide against Client data'),
#('avox_entity_class', 'Avox Entity Class', 'Classification of entity. EG Corp, Bank etc.'),
#('avox_entity_type', 'Avox Entity Type', 'Type of entity within hierarchy, e.g. Ultimate Parent'),
#('record_source', 'Record Source', 'Source from which data was obtained (used in Avox audit trail) - free format text'),
('legal_name', 'Legal Name', 'Legal name as per the registration document'),
('previous_name_s_', 'Previous Name(s)', 'Previous legal names - Delimited by | if multiple values'),
('trades_as_name_s_', 'Trades As Name(s)', 'Names under which the company trades but which differ from their legal name - Delimited by | if multiple values'),
#('name_notes', 'Name Notes', 'Analyst notes about the company name(s)'),
#('legal_form', 'Legal Form', 'Examples include Partnership, Sole Proprietorship and Limited. This is typically defaulted from the legal name field - free format text'),
('trading_status', 'Trading Status', 'Defines the trading status of the entity: Active, In Administration, Inactive, Dissolved'),
('swift_bic', 'SWIFT BIC', 'Mixed alpha-numeric code from Swift - Bank Identifier Code'),
#('vat_number', 'VAT Number', 'Value added tax number applicable in countries such as the UK'),
#('tax_payer_id', 'Tax Payer ID', 'US identifier allocated to companies and individuals'),
('company_website', 'Company Website', 'URL'),
#('regulated_by', 'Regulated By', 'Financial regulators (E.G. FSA, SEC, BaFin...)'),
#('regulator_id', 'Regulator ID', 'Identifier assigned by the selected regulator'),
#('regulatory_status', 'Regulatory Status', 'Values linked to the specific regulator. (FSA example: EEA Authorised, Introducer AR, Schedule 5, No Longer Authorised, Authorised, Registered, Appointed Representative, Applied to Cancel)'),
#('registration_authority', 'Registration Authority', '(e.g. Companies House, SEDAR, Deleware Secretary of State)'),
#('registration_number__operational_', 'Registration Number (Operational)', 'Identification code assigned by the registration authority for the country (or US state) in which the entity operates.'),
('registration_number__jurisdiction_', 'Registration Number (Jurisdiction)', 'Identification code assigned by the registration authority for the country (or US state) of Jurisdiction for the entity'),
('date_of_registration', 'Date Of Incorporation', 'Date that the company was incorporated in the state or country of jurisdiction'), # used to be Date of Registration
('date_of_dissolution', 'Date Of Dissolution', 'Date that the company dissolved if it is no longer active'),
#('issuer_flag', 'Issuer Flag', 'Does the entity issue listed securities - Y/N'),
('primary_listing_exchange', 'Primary Listing Exchange', 'Primary exchange upon which the company\'s ordinary shares are listed'),
('ticker_code', 'Ticker Code', 'The symbol representing the company name on the primary exchange'),
#('cabre', 'CABRE', ''), # this is not being used
#('fiscal_year_end', 'Fiscal Year End', 'Financial statement information - Month of entity\'s year end'),
#('mifid_source', 'MIFID Source', 'Financial statement information'),
#('balance_sheet_date', 'Balance Sheet Date', 'Financial statement information'),
#('balance_sheet_currency', 'Balance Sheet Currency', 'Financial statement information'),
#('balance_sheet_total', 'Balance Sheet Total', 'Financial statement information'),
#('annual_net_turnover', 'Annual Net Turnover', 'Financial statement information'),
#('own_funds', 'Own Funds', 'Financial statement information'),
('operational_po_box', 'Operational PO Box', 'Operational address information'),
('operational_floor', 'Operational Floor', 'Operational address information'),
('operational_building', 'Operational Building', 'Operational address information'),
('operational_street_1', 'Operational Street 1', 'Operational address information'),
('operational_street_2', 'Operational Street 2', 'Operational address information'),
('operational_street_3', 'Operational Street 3', 'Operational address information'),
('operational_city', 'Operational City', 'Operational address information'),
('operational_state', 'Operational State', 'Operational State, Province, Region or Territory'),
('operational_country', 'Operational Country', 'Operational address information'), # "ISO country code" previously, changed to reflect display of country name
('operational_postcode', 'Operational Postcode', 'Operational address information'),
#('operational_address_notes', 'Operational Address Notes', 'Analyst notes about the operational address'),
('registered_agent_name', 'Registered Agent Name', 'Registered address information'),
('registered_po_box', 'Registered PO Box', 'Registered address information'),
('registered_floor', 'Registered Floor', 'Registered address information'),
('registered_building', 'Registered Building', 'Registered address information'),
('registered_street_1', 'Registered Street 1', 'Registered address information'),
('registered_street_2', 'Registered Street 2', 'Registered address information'),
('registered_street_3', 'Registered Street 3', 'Registered address information'),
('registered_city', 'Registered City', 'Registered address information'), # "Registered City" previously, changed for consistency
('registered_state', 'Registered State', 'Registered State, Province, Region or Territory'),
('registered_country', 'Registered Country', 'ISO country code'),
('registered_postcode', 'Registered Postcode', 'Registered address information'),
#('registered_address_notes', 'Registered Address Notes', 'Analyst notes about the registered address'),
('naics_code', 'NAICS Code', 'North American Industry Classification System code'),
('naics_description', 'NAICS Description', 'North American Industry Classification System description'),
('us_sic_code', 'US SIC Code', 'US Standard Industrial Classification code'),
('us_sic_description', 'US SIC Description', 'US Standard Industrial Classification description'),
#('nace_code', 'NACE Code', 'Nomenclature g&eacute;nerale des Activit&eacute;s &eacute;conomiques dans les Communaut&eacute;s Europ&eacute;ennes code'),
#('nace_description', 'NACE Description', 'Nomenclature g&eacute;nerale des Activit&eacute;s &eacute;conomiques dans les Communaut&eacute;s Europ&eacute;ennes description'),
('entity_type', 'Entity Type', 'Defines whether the entity is an Ultimate Parent, a subsidiary, or a branch or division'),
('immediate_parent_avid', 'Immediate Parent AVID', 'AVID of Immediate Parent record'),
('immediate_parent_name', 'Immediate Parent Name', 'Legal name from Immediate Parent record'),
#('immediate_parent_percentage ownership', 'Immediate Parent Percentage Ownership', 'Percentage of the entity that the Immediate Parent owns (must be greater than 50%)'),
#('immediate_parent_notes', 'Immediate Parent Notes', 'Analyst notes about the Immediate Parent relationship'),
('ultimate_parent_avid', 'Ultimate Parent AVID', 'AVID of Ultimate Parent record'),
('ultimate_parent_name', 'Ultimate Parent Name', 'Legal name from Ultimate Parent record'),
#('ultimate_parent_notes', 'Ultimate Parent Notes', 'Analyst notes about the Ultimate Parent relationship'),
#('general_notes', 'General Notes', 'General notes about this data record - free format text'),
];

def getFields(environ):
    fields = []
    openfields = environ['tiddlyweb.config']['mappingsql.open_fields']
    for field, label, tooltip in recordFields:
        if environ['tiddlyweb.usersign']['name'] == "GUEST":
            if field in openfields:
                fields.append((field,label,tooltip))
        else:
            fields.append((field,label,tooltip))
    logging.debug('fields passed: %s', fields)
    return fields
