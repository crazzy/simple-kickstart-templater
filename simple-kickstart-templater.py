#!/usr/bin/python
import BaseHTTPServer
import os
import socket
import sys

# Define a HTTP request handler class for BaseHTTPServer
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def simple_message(self, return_code, message):
        self.send_response(return_code)
        self.send_header('Content-Type','text/plain')
        self.end_headers()
        self.wfile.write(message + '\n')

    def do_GET(self):
        # Get the client MAC address from the "X_RHN_PROVISIONING_MAC_0" request header
        try:
            kssendmac_header = self.headers.dict['x_rhn_provisioning_mac_0']
        except KeyError:
            self.simple_message(400, 'ERROR: The "X_RHN_PROVISIONING_MAC_0" header was not found, did you use the "kssendmac" kernel parameter when booting?')
            return

        try:
            mac_addr = kssendmac_header.split()[1]
        except IndexError:
            self.simple_message(400, 'ERROR: The "X_RHN_PROVISIONING_MAC_0" header was not in the expected format')
            return

        # Find the host file that contains the given MAC address
        host_file = None
        for file in os.listdir('hosts'):
            try:
                if mac_addr in open(os.path.join('hosts', file)).read():
                    host_file = file
            except IOError:
                pass

        if host_file is None:
            self.simple_message(404, 'ERROR: No host entry found for MAC address "%s"' % mac_addr)
            return

        # Get the template filename and variable data from the host file
        template_file = None
        variables = {}
        try:
            host_data = open(os.path.join('hosts', host_file)).readlines()
        except IOError:
            self.simple_message(503, 'ERROR: Could not open host file "%s"' % host_file)
            return

        # Parse the template name and template variables
        for line in host_data:
            if line.startswith('template'):
                template_file = line.split('=')[1].strip()
            if line.startswith('%%'):
                variables[line.split('=')[0].strip()] = line.split('=')[1].strip()

        # Check if the template filename was found in the host file
        if template_file is None:
            self.simple_message(503, 'ERROR: Template filename not found in host file')
            return

        # Read the kickstart template
        try:
            template_data = open(os.path.join('templates', template_file)).read()
        except IOError:
            self.simple_message(503, 'ERROR: Could not open template file "templates/%s"' % template_file)
            return

        # Replace the variable placeholders in the template data
        for k, v in variables.items():
            template_data = template_data.replace(k, v)

        self.simple_message(200, template_data)

def main():
    HTTP_PORT = 8080
    sys.stdout.write('Starting HTTP server... ')
    try:
        httpd = BaseHTTPServer.HTTPServer(('', HTTP_PORT), RequestHandler)
    except socket.error, e:
        sys.stdout.write('\033[91m[FAILED]\033[0m (%s)\n' % e.strerror)
    else:
        sys.stdout.write('\033[92m[OK]\033[0m\n')
        httpd.serve_forever()

if __name__ == '__main__':
    main()
