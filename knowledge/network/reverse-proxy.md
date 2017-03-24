Why reverse proxy:
- Use less IPs
- Facilitates managing different HTTPS certificates
- Centralizes logs and troubleshooting


I went crazy configuring `haproxy` as a HTTPS reverse proxy for `wordpress`. **Lesson learned**: [use a network analyzer tool](https://github.com/guifi-exo/doc/blob/master/knowledge/network/analysis.md).

The core concept of a HTTPS reverse proxy is to add this two options in the HTTP header:

```
X-Forwarded-For: x.x.x.x
X-Forwarded-Proto: https
```

In the network captures

To add it in nginx:

```
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Note: nginx folks also usually add `X-Real-IP` but this is doing the same as X-Forwarded-For, so (?). [A reference](http://distinctplace.com/infrastructure/2014/04/23/story-behind-x-forwarded-for-and-x-real-ip-headers/)

To add it in haproxy:

```
option forwardfor
http-request set-header X-Forwarded-Proto https

```
