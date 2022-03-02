import requests, socket
from discord_webhook import DiscordWebhook,DiscordEmbed

# ----------VARIABLES TO MODIFY ---------

domain = 'subdomain.domain.com' # Reference domain for local / public IP check
reference_domain = 'subdomain.domain.com' # local domain to check
WEBHOOK_URL="your_webhook_url"
discord_username = '<@my_id>' # username to mention if record has been updated (keep <@ and >)
# ---------------------------------------
host= [['subdomain.domain.com','username','password'],
    ['subdomain2.domain.com','username2','password2']]
# ---------------------------------------

# -- CORE --
global discord_log2
discord_log2 = ""
discord_log = ""
system = 'dyndns'
different = False

webhook = DiscordWebhook(url=WEBHOOK_URL)
# ---------------------------------------
def log_string(message):
    global discord_log2
    discord_log2 += "\n" + message
# ---------------------------------------
check_ip_addr = socket.gethostbyname(domain) # check if ip of domain match ip of reference domain
ref_ip_addr = socket.gethostbyname(reference_domain)
# ---------------------------------------
length = len(host)
if ref_ip_addr != check_ip_addr: # domain record does not match the public ip  - i.e : need to update the record
    different = True
    discord_log = discord_username + " Reference domain IP and check domain IP are **different** - __need to update records__"
    discord_log += "\n" + "Domains will be updated with **" + ref_ip_addr + "** IP"
    for host in host:
        hostname = host[0]
        username = host[1]
        password = host[2]
        params = (('system', 'dyndns'),('hostname', hostname),('myip', ref_ip_addr),)
        response = requests.get('https://www.ovh.com/nic/update', params=params, auth=(username, password))
        log_string("*" + hostname + "* updated with status code : **" + str(response.status_code) + "**")
else:
    discord_log = "Both reference domain IP and check domain IP are **equal** - __no need to update records__"
# ---------------------------------------
# create embed object for webhook
embed = DiscordEmbed(title="Summary", color='f6ff00')
embed.add_embed_field(name='Reference domain', value=reference_domain, inline=True)
embed.add_embed_field(name='Check domain', value=domain, inline=True)
embed.add_embed_field(name='\u200b', value='\u200b') # empty field to get 2x2 display
embed.add_embed_field(name='Reference domain IP', value=ref_ip_addr, inline=True)
embed.add_embed_field(name='Check domain IP', value=check_ip_addr, inline=True)
embed.add_embed_field(name='\u200b', value='\u200b')
embed.add_embed_field(name='Domains', value=length, inline=False)
embed.add_embed_field(name='Execution', value=discord_log, inline=False)
webhook.add_embed(embed)
if different:
    embed2 = DiscordEmbed(title="Details", description=discord_log2, color='AC33FF')
    embed2.set_timestamp()
    webhook.add_embed(embed2)
else: 
    embed.set_timestamp()
response = webhook.execute()