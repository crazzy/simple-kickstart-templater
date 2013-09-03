# Simple Kickstart Templater

## What is it?
The Simple Kickstart Templater is a small script the runs a minimal web server for serving kickstart files. It can serve different kickstart files to different hosts (based on their MAC address), and supports basic variable templating.

## Why would I want to use this?
* You need to quickly and easily debug a kickstart file you are working on, without modifying production systems
* You want to set up a small build lab but don't need or want a bulkier system (such as [cobbler](http://www.cobblerd.org/))

## What are the benefits?
Only python is required, which you probably already have. No need to install or configure a web server, just run the script and you have a simple but flexible system for serving kickstart files with a basic level of templating.

## Installation
```
git clone xxx
cd xxx
python skt.py
```

Once the server is running point your kickstart installation at the server (i.e. using the kernel parameter `ks=http://<your host>/`)

## How it works
1. Get the clients MAC address from the `X_RHN_PROVISIONING_MAC_0` header.
1. Search through the files in the `hosts` directory to find a host with a matching MAC address.
1. Read the file in the hosts directory and load the template specified.
1. Replace the placeholder variables in the template with the data from the host file

Template variables are defined by starting with %% in the host file.

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
