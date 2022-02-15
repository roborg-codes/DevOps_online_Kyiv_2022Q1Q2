# Task 3.4

DHCP
----

For this task, I started with configuring DHCP server in Enterprise network:

![DHCP server configuration](./images/DHCP.png)

And then enabling DHCP on both clients on the network, allowing the service to freely assign these devices IP addresses within `/24` range:

![DHCP on client side](./images/DHCP-clients.png)

The same process applies for the home router, and can be seen in DNS enabling section.

DNS
---

I got on DNS server's configuration by assigning neighbouring servers their respective A record domain names:

![DNS server configuration](./images/DNS-configuration.png)

Then, I added this DNS server to both of my DHCP servers, and reenabled DHCP on all clients:

![Configuring DNS and DHCP on Home Router](./images/DNS-homerouter.png)

And like this, Web Servers were accessible via their domain names:

![Pinging domain1 from Enterprise](./images/DNS-in-action.png)


Port forwarding
---------------

For homeserver, I first configured the server with a static IP address and a custom index.html file.
Then plugged it into the router and configured the router to forward http traffic to `192.168.0.100`.
Then, added a DNS record, tried opening domain3 on Enterprise network and recorded all DNS and HTTP traffic:

![Accessing home server with port forwarding](./images/homeserver.png)
