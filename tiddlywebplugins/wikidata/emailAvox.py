import logging
from tiddlywebplugins.wikidata import recordFields
from tiddlywebplugins.wikidata.sendEmail import send

def emailAvox(query, domain='wiki-data.com'):
    domainStem = domain.split('.')[0]
    requestType = query['requestType'][0]
    name = query['name'][0]
    email = query['email'][0]
    try:
        country = query['country'][0]
    except:
        country = "not set"
    company = query['company'][0]
    if requestType == 'request':
        avid = query['avid'][0]
        legal_name = query['legal_name'][0]
        additional_info = query.get('additional_info', [''])[0]
        to = ['requestinformation.'+domainStem+'@avox.info', 'jnthnlstr@googlemail.com']
        subject = 'Request for more information'
        body = 'SPECIFIC REQUEST re: additional information request\n' \
            'for '+legal_name+' (AVID = '+avid+')\n'
        if additional_info != '':
            body += 'Additional info: '+additional_info+'\n'
        body += 'Name: '+name+'\n' \
            'Email address: '+email+'\n' \
            'Country: '+country+'\n' \
            'Company: '+company+'\n'
    elif requestType == 'challenge':
        avid = query['avid'][0]
        legal_name = query['legal_name'][0]
        original_legal_name = query['original_legal_name'][0]
        source = query['source'][0]
        to = ['foundanerror.'+domainStem+'@avox.info', 'jnthnlstr@googlemail.com']
        subject = 'Challenge record'
        body = 'SPECIFIC REQUEST re: correction\n' \
            'for '+original_legal_name+' (AVID = '+avid+')\n' \
            'Name: '+name+'\n' \
            'Email address: '+email+'\n' \
            'Country: '+country+'\n' \
            'Company: '+company+'\n' \
            'Source for challenge: '+source+'\n' \
            'Challenge details\n--------------\n'
        #for field, _ in recordFields.recordFields: # is this syntax valid?
        for field, label, tooltip in recordFields.recordFields:
            try:
                body += label+': '+query[field][0]+'\n'
            except KeyError:
                pass
    elif requestType == 'suggest_new':
        source = query['source'][0]
        to = ['registerentity.'+domainStem+'@avox.info', 'jnthnlstr@googlemail.com']
        subject = domain+' AVID Entity Registration'
        body = """Submittor info
--------------
Name: %s
Email address: %s
Country: %s
Company: %s

Sources:
%s

Record info
--------------
""" % (name, email, country, company, source)
        for field, label, tooltip in recordFields.recordFields:
            try:
                body += label + ': ' + query[field][0] + '\n'
            except KeyError:
                pass
    elif requestType == 'wdds':
        telephone = query['telephone'][0]
        comments = query['comments'][0]        
        to = ['wiki-data@avox.info', 'jnthnlstr@googlemail.com']
        subject = 'Wiki-Data File Download Service request'
        body = """Submittor info
--------------
Name: %s
Email address: %s
Company: %s
Telephone: %s

Comments:
%s
--------------
""" % (name, email, company, telephone, comments)
    else:
        to = 'jnthnlstr@googlemail.com'
        subject = 'Unknown contact type'
        body = 'Query: %s' % repr(query)
    logging.debug('to: %s , subject: %s body: %s', repr(to), subject, body)
    send(to, subject=subject, body=body, from_='avox@'+domain)
