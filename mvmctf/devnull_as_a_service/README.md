# /dev/null as a service
A few months ago, I came across [this](https://devnull-as-a-service.com/) website. Inspired by it, I decided to recreate the service in C to self-host it.

To avoid any exploitable vulnerabilities, I decided to use a very strict seccomp filter. Even if my code were vulnerable, good luck exploiting it.

PS: You can find the flag at `/home/ctf/flag.txt` on the remote server.