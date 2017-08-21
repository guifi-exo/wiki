# Orchestration and Configuration manager solutions

## Ansible

Does not require agent and uses ssh. Relieves on python, but you can use raw mode (the ssh you encounter) or other programming languages.

## TR-069

Used by most ISPs in the world for configuring home routers

"If an attacker compromises an ACS he could obtain information from the managed routers like wireless network names, hardware MAC addresses, voice-over-IP credentials, administration usernames and passwords. He could also configure the router to use a rogue DNS server, to pass the entire traffic Internet through a rogue tunnel, set up a hidden wireless network or remove the security password from the existing network. Even worse, he could upgrade the firmware on the devices with a rogue version that contains malware or a backdoor.
The TR-069 specification recommends the use of HTTPS (HTTP with SSL encryption) for connections between managed devices and the ACS, but tests performed by Tal and his colleagues revealed that around 80 percent of real-world deployments don’t use encrypted connections. Even when HTTPS is used, in some cases there are certificate validation issues, with the customer equipment accepting self-signed certificates presented by an ACS. This allows a man-in-the-middle attacker to impersonate the ACS server."

src: http://www.pcworld.com/article/2463480/many-home-routers-supplied-by-isps-can-be-compromised-en-masse-researchers-say.html
