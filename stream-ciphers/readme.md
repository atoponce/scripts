# !!! PLEASE DON'T USE THESE SCRIPTS !!!

I implemented these stream ciphers strictly as a learning exercise. I don't plan on ever using them
in real code and I hope you won't also. Even though I've ensured they pass their respective test
vectors, cryptography development is full of sharp edges. Side channel attacks, key/nonce reuse,
buffer overflow errors, and so much more. I've made no attempt to mitigate any of these.

Even if I did go to great extent to make this code as safe as possible, JavaScript isn't exactly the
best language to develop cryptography with. I would prefer Rust if both correctness and safety were
my goals.

I hang out in a number of different cryptography and security communities, both online and offline.
These were developed to help deepen my understanding of the internals of different stream ciphers
and their designs. Thus, when I find myself in discussion about such things, I can have a more
meaningful conversation.

That's it. My intention for these scripts is strictly for personal enlightenment and nothing more.
