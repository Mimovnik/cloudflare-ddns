# update_dns.py
import os
import requests
import json
import time
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

def get_public_ip():
    """Try multiple IP detection services with fallback"""
    services = [
        {
            'url': 'https://1.1.1.1/cdn-cgi/trace',
            'parser': lambda r: [line.split('=')[1] for line in r.text.split('\n') if 'ip=' in line][0]
        },
        {
            'url': 'https://api.ipify.org?format=json',
            'parser': lambda r: r.json()['ip']
        },
        {
            'url': 'https://ifconfig.me/ip',
            'parser': lambda r: r.text.strip()
        },
        {
            'url': 'https://ipecho.net/plain',
            'parser': lambda r: r.text.strip()
        }
    ]

    for service in services:
        try:
            response = requests.get(service['url'], timeout=5)
            response.raise_for_status()
            return service['parser'](response)
        except Exception as e:
            logging.warning(f"Failed {service['url']}: {str(e)}")
            continue

    logging.error("All IP detection services failed")
    return None

def update_dns_record(new_ip):
    config = {
        'api_token': os.getenv('CF_API_TOKEN'),
        'zone_id': os.getenv('CF_ZONE_ID'),
        'record_id': os.getenv('CF_DNS_RECORD_ID'),
        'record_name': os.getenv('CF_DNS_RECORD_NAME'),
        'record_type': os.getenv('CF_RECORD_TYPE', 'A'),
        'proxied': os.getenv('CF_PROXIED', 'false').lower() == 'true'
    }

    url = f"https://api.cloudflare.com/client/v4/zones/{config['zone_id']}/dns_records/{config['record_id']}"
    headers = {
        'Authorization': f'Bearer {config["api_token"]}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'type': config['record_type'],
        'name': config['record_name'],
        'content': new_ip,
        'ttl': int(os.getenv('CF_TTL', '120')),
        'proxied': config['proxied']
    }

    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        if response.json().get('success', False):
            logging.info(f"Successfully updated {config['record_name']} to {new_ip}")
            return True
        logging.error(f"API Error: {response.text}")
    except Exception as e:
        logging.error(f"Update failed: {str(e)}")
    
    return False

if __name__ == '__main__':
    check_interval = int(os.getenv('CF_UPDATE_INTERVAL', '300'))
    last_ip = None
    
    while True:
        current_ip = get_public_ip()
        if current_ip and current_ip != last_ip:
            if update_dns_record(current_ip):
                last_ip = current_ip
            else:
                logging.error("Failed to update DNS record")
        
        time.sleep(check_interval)
