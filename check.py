import sys
import requests
import shodan

# https://kb.vmware.com/s/article/82374

# If 404/Not Found error is returned from the URL, then not vulnerable
# https://<VC-IP-or-FQDN>/ui/vropspluginui/rest/services/checkmobregister
# ptswarm's POC appears to show that as long as this page returns 200, then
# the server is vulnerable.  That's what I'm going with.

def main(argv):

    SHODAN_API_KEY = "----PUT API KEY HERE----"
    api = shodan.Shodan(SHODAN_API_KEY)

    protocol = 'https://'
    #server = sys.argv[1]
    endpoint = '/ui/vropspluginui/rest/services/checkmobregister'

    try:
        results = api.search("http.title:ID_VC_Welcome")
        print('Found: {}'.format(results['total']))
        for result in results['matches']:
            server = result['ip_str']
            url = protocol + server + endpoint
            try:
                r = requests.get(url, verify=False, timeout=(6.1))
            except:
                print(server + " did not respond")
                continue

            if r.status_code == 200:
                print(server + " is vulnerable!!!!!!!!!! - Status Code: " + str(r.status_code))
            else:
                print(server + " is not vulnerable - Status Code: " + str(r.status_code))
    except shodan.APIError:
        print('Error: Shodan API Error')

if __name__ == "__main__":
    main(sys.argv[1:])
