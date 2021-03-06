# Simple Kickstart Templater

[![Build Status](https://travis-ci.org/cdodd/simple-kickstart-templater.svg?branch=master)](https://travis-ci.org/cdodd/simple-kickstart-templater)

## So, what is it?
The Simple Kickstart Templater is a small script the runs a minimal web server
for serving kickstart files. It can serve different kickstart files to
different hosts (based on their MAC address), and supports basic variable
templating.

## Why would I want to use this?
* You need to quickly and easily debug a kickstart file you are working on,
without modifying production systems
* You want to set up a small build lab but don't need or want a bulkier system
(such as [cobbler](http://www.cobblerd.org/))

## What are the benefits?
Only python is required, which you probably already have, no external
dependencies. No need to install or configure a web server, just run the script
and you have a simple but flexible system for serving kickstart files with a
basic level of templating.

## Installation
This script is designed to run on Python 2.7, and has been tested on 2.7.5. It
won't run on Python 3 however as the `BaseHTTPServer` module is not available.

To download and start the script, run the following:
```
git clone https://github.com/cdodd/simple-kickstart-templater.git
simple-kickstart-templater/simple-kickstart-templater.py
```

Once the server is running point your kickstart installation at the server
(i.e. using the kernel parameter `linux ks=http://<your host>:8080/ kssendmac`)

Make sure to include the `kssendmac` option as this is required for the client
to send the `X_RHN_PROVISIONING_MAC_0` header, which the template system uses
to identify which kickstart file to serve.

## How it works
1. Get the clients MAC address from the `X_RHN_PROVISIONING_MAC_0` header.
1. Search through the files in the `hosts` directory to find a host with a
matching MAC address.
1. Read the file in the hosts directory and load the template specified.
1. Replace the placeholder variables in the template with the data from the
host file

Template variables are defined by wrapping a variable name with double percent
characters (e.g. `%%KEYBOARD%%`).

## Example host file
```
mac=de:ad:be:ef:ca:fe
template=default
%%KEYBOARD%%=uk
```

## Viewing a kickstart file

You can view the kickstart file that gets served to a host with `curl`:
```
curl -H 'X_RHN_PROVISIONING_MAC_0: eth0 de:ad:be:ef:ca:fe' <your host>:8080
```
