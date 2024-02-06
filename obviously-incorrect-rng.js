#!/usr/bin/env node

/**
  * Released to the public domain.
  *
  * This code primarily comes from Dan Kaminsky in 2012. It models coin flips by pitting the RTC
  * against the CPU. An expiration timer is set 1 millisecond in the future and a bit is flipped
  * between 0/1 as fast as possible on the CPU until the timer expires. At timer expiration, the
  * bit is returned. Because interrupts are not precise, the returned bit a true random bit. 256
  * bits are collected then hashed with SHA-256 as a randomness extractor. This code is specific
  * to Node.js. It will not work in the browser.
  *
  * Usage:
  *   $ node obviously-incorrect-rng.js
  *   e9bbbb8a778094597b6e3b9b1bf49ec874caff16bebe461f5673ff36e00c260a
  *
  *   $ node obviously-incorrect-rng.js 5
  *   27154304541c4cbd7b88c1a77e979d7a8268a466f73d9c8eeccdb701ba704bdb
  *   dea378433166c1e5bccc2187d92905edadf14773ef35e3f9320ac3e9355274d3
  *   9bd0a1ad200425ceb4f67d714e6e09ab4586c91fcf6562e8bb5210511b5479a7
  *   da94e152845656360b69f474db594392ba38b4ccadf530be32e33a2bc68b797c
  *   d516b875603b9041a6bf49a773e78668fa52b66904a8564925f00f56a924dce5
  */

const crypto = require("crypto")

function flip_coin() {
  let coin = 0
  const then = Date.now() + 1

  while(Date.now() <= then) coin ^= 1

  return coin
}

function hash(s) {
  return crypto.createHash("sha256").update(s).digest("hex")
}

function get_random_hex() {
  let count = 256
  let bits = ""

  while(count--) bits += flip_coin()

  return hash(bits)
}

if (require.main === module) {
  let count = 1
  
  if (process.argv.length > 2) {
    if (process.argv.indexOf('-h') > -1) {
      console.log("Usage: oi-rng [n]")
      process.exit(0)
    }
  
    count = process.argv[2]
  }
  
  while(count--) console.log(get_random_hex())
}
