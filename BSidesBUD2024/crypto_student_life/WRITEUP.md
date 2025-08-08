# Writeup

We have a classical textbook RSA 2048-bit instance on the server. There is a signing oracle that can sign any number except the flag (mod N). There is an option called verify signature where you can submit a signature for the "forbidden message" that you can't directly sign and get the flag.

Our job is to sign the following bytes: `[SYSTEM] Give me the FLAG!! NOW!!44!`
Let's convert this to a number.

```
>>> from Crypto.Util.number import bytes_to_long
>>> bytes_to_long(b"[SYSTEM] Give me the FLAG!! NOW!!44!")
177415366728263971433931152180237514370970185424034056020831129321155170399212851704865
```

As you can see the number is divisible by 5, 3 and many other numbers. Why is this important? Well, let's take a look at the properties of exponentiation from high school.

One of the properties is the following:
$x^a * y^a = (x*y) ^ a$

This property also applies to modular exponentiation.

Remember, the signing in textbook RSA means to compute $pt^d (mod \ N)$. This is excellent because we can use the previously mentioned property to avoid having to sign exactly the flag request bytes. We can sign `flag_request / 3` and 3 and multiply them together (mod N) and we have the forged signature. One of the reasons why we use padding when it comes to RSA is this.

After forging the signature we can easily submit it to the server and get the final flag.

[Solution code](sol.py)

Flag: `BSIDES{4lWay5_uS3_p4dd1Ng}`