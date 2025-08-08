# Bluetrap

Bluetooth is all about convenient communication. But what happens when "plug and play" becomes "plug and pwn"?

Inspired by a real Bluetooth vulnerability from 2018, this device attempts to use ECC to establish a shared key—except the implementation is a little... forgetful.

You can still send your public key though. Surely you can guess the shared secret from there, right?

`nc challs.ctf.bsidesbud.com 4141`

By: [ahornyai](https://github.com/ahornyai)