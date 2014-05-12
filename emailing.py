from mako.template import Template
from mako.lookup import TemplateLookup
import mandrill

mylookup = TemplateLookup(directories=[''],input_encoding='utf-8',output_encoding='utf-8',)
mytemplate = mylookup.get_template("template.html")


## TODO ##
# Contruire object avec les bons parametres de l'email
# mytemplate.render(TODO);
message = {'attachments': None,
            'auto_html': None,
            'auto_text': None,
            'from_email': 'jeremie@datarec.io',
 'from_name': 'Jeremie Cohen',
 'headers': {'Reply-To': 'jeremie@datarec.io'},
 'html': mytemplate.render(name='dsds'),
 'important': False,
 'metadata': {'website': 'www.datarec.io'},
 'preserve_recipients': None,
 'recipient_metadata': [{'rcpt': 'jeremcoh@gmail.com',
                         'values': {'user_id': 123456}}],
 'subject': 'Test Email',
 'tags': ['thebeautyst'],
 'to': [{'email': 'jeremcoh@gmail.com',
         'name': 'Jeremie Cohen',
         'type': 'to'}],
 'track_clicks': True,
 'track_opens': True,
 'tracking_domain': True}

mandrill_client = mandrill.Mandrill('QVQhU-pdRHiaPGWceEKZfg')
result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool', send_at='')


