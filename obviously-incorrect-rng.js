#!/usr/bin/env node

/**
  * Released to the public domain.
  *
  * This code primarily comes from Dan Kaminsky in 2012. It models coin flips by pitting the RTC
  * against the CPU. An expiration timer is set at some point in the future and a bit is flipped
  * between 0/1 as fast as possible on the CPU until the timer expires. At timer expiration, the
  * bit is returned. Because interrupts are not precise, a "true random" bit is generated, after
  * which it can be sent through a von Neumann randomness extractor or collect 256 bits & hashed
  * with SHA-256. This code is specific to Node.js. It will not work in the browser.
  */

const crypto = require("crypto")

function print_usage() {
  console.log("Usage: " + process.argv[1] + " [OPTION [ARG]]\n")
  console.log("\n")
  console.log("  -h,   --help      Print this help and exit.\n")
  console.log("\n")
  console.log("  -b,   --byte      Get raw bytes.\n")
  console.log("  -c,   --coin      Get raw coin flips.\n")
  console.log("\n")
  console.log("  -f,   --fair      Get fair coin flips (von Neumann extracted).\n")
  console.log("  -s,   --spins     Get number of spins per coin flip.\n")
  console.log("  -v,   --neumann   Get fair bytes (von Neumann extracted).\n")
  console.log("\n")
  console.log("  -2,   --sha256    Get 256 bits in hex (SHA-256 hashed).\n")
  console.log("  -x,   --hex       Get 256 bits in hex (von Neumann extracted).\n")
  console.log("\n")
  console.log("  -n #, --num #     Print requested data specific number of times.\n")
}

/**
 * Returns a high resolution timestamp with sub-millisecond accuracy.
 * @returns {number}
 */
function now() {
  return performance.now()
}

/**
 * Sets a timer in the future and flips a bit between 0/1 until the timer expires.
 * @returns {number}
 */
function flip_coin() {
  let coin = 0
  const later = now() + 0.1

  while(now() <= later) coin ^= 1

  return coin
}

/**
 * Counts the number of bit flips before the timer expires.
 * @returns {Array}
 */
function coin_spins() {
  let coin = 0
  let cycles = 0
  const later = performance.now() + 0.1

  while(performance.now() <= later) {
    coin ^= 1
    cycles++
  }

  return [coin, cycles]
}

/**
 * John von Neumann randomness extractor.
 * @returns {number}
 */
function fair_bit() {
  while(1) {
    const a = flip_coin()
    if(a != flip_coin()) return(a)
  }
}

/**
 * Builds a full byte, either raw (for SHA-256) or after von Neumann randomness extraction.
 * @param {string} extractor 
 * @returns {number}
 */
function get_byte(extractor) {
  let n = 0
  let bits = 8

  while(bits--) {
    n <<= 1

    if(extractor === "sha256")
      n |= flip_coin()
    else if (extractor === "neumann")
      n |= fair_bit()
    else
      process.exit(1)
  }

  return n
}

/**
 * Generates a 256-bit hexadecimal string from von Neumann debiased bits.
 * @returns {string}
 */
function fair_bytes() {
  let count = 32
  const results = new Uint8Array(count)

  while(count--) results[count] = get_byte("neumann")

  return Buffer.from(results).toString("hex");
}

/**
 * Generates a 256-bit hexadecimal string from SHA-256 hashing.
 * @returns {string}
 */
function hash_bytes() {
  let count = 32
  const results = new Uint8Array(count)

  while(count--) results[count] = get_byte("sha256")

  return crypto.createHash("sha256").update(results).digest("hex")
}

if (require.main === module) {
  let count = 1
  const args = process.argv.slice(2)
  
  if (args.includes("-n") || args.includes("--num")) {
    const option = args.findIndex((option) => option === "-n" || option === "--num")
    count = args[option + 1]
  }
  
  while(count--) {
    if (args.includes("-h") || args.includes("--help")) {
      print_usage()
      process.exit(0)
    }
    else if (args.includes("-2") || args.includes("--sha256"))
      console.log(hash_bytes())
    else if (args.includes("-b") || args.includes("--bytes"))
      console.log(get_byte("sha256"))
    else if (args.includes("-c") || args.includes("--coin"))
      console.log(flip_coin())
    else if (args.includes("-f") || args.includes("--fair"))
      console.log(fair_bit())
    else if (args.includes("-s") || args.includes("--spins")) {
      const result = coin_spins()
      console.log(result[0] + ", " + result[1])
    }
    else if (args.includes("-v") || args.includes("--neumann"))
      console.log(get_byte("neumann"))
    else if (args.includes("-x") || args.includes("--hex"))
      console.log(fair_bytes())
    else
      console.log(hash_bytes())
  }
}