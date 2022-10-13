#!/usr/bin/env python3

import argparse
from urllib.parse import urlparse
import sys
import socket
import ssl
import datetime

parser = argparse.ArgumentParser(description='Specify domain name to check. As example: https://example.com:443')
parser.add_argument('-d', dest='domain', required=True, type=str, help="Specify domain name to check. As example: https://example.com:443")
args = parser.parse_args()
# print (args.domain)
default_timeout= 10 # seconds

def checkInt(number_str):
    print (number_str)
    if number_str[0] in ('-', '+'):
        return number_str[1:].isdigit()
    return str.isdigit()

def validate_domain(domain):
    res = urlparse(''.join(args.domain.split()))
    # print (res)
    if res.scheme != 'https':
        print ('URL scheme must be httpS, please specify it rightly, exit...')
        return False
    else:
        pass
    if res.scheme != '' and res.netloc != '':
        return res.netloc
    else:
        print ('Wrong domain name and scheme, please specify domain. As example: https://example.com:443')
        return False

def get_cert_expiration_days(domain):
    port = 443
    domain_in_split = domain.split(':')
    if len(domain_in_split) > 2:
        try:
            int(domain_in_split[-1])
            if int(domain_in_split[-1]) >=1 and int(domain_in_split[-1]) <=65535:
                port = int(domain_in_split[-1])
            else:
                print ('Port number is outside of range 1..65535')
                sys.exit(1)
        except:
            print ('Wrong port number, exit...')
            sys.exit(1)
    else:
        pass
    dn = ''.join(domain.split()).split(':')[1].replace('/','')
    try:
        context = ssl.create_default_context()
        with socket.create_connection((dn, str(port)), timeout=default_timeout) as sock:
            with context.wrap_socket(sock, server_hostname=dn) as ssock:
                now = datetime.datetime.now()
                notAfter = ssl.cert_time_to_seconds(ssock.getpeercert()['notAfter'])
                delta_seconds = (datetime.datetime.fromtimestamp(notAfter)-now).total_seconds()
                return int(divmod(delta_seconds, 86400)[0])
    except:
        print (f'Something went wrong during connection up to host {domain}')
        sys.exit(1)


def mainfunc():
    netloc_domain = validate_domain(args.domain)
    if netloc_domain != False and type(netloc_domain) == str:
            expire_days = get_cert_expiration_days(args.domain)
            print (expire_days)
            return (expire_days)
    else:
        print ('Something has been wrong during domain validation, exit...')
        sys.exit(1)


if __name__ == '__main__':
    mainfunc()