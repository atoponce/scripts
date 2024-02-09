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

/**
 * Prints the options supported by the script. Grouped by concept.
 */
function print_usage() {
  console.log("Usage: " + process.argv[1] + " [OPTION [ARG]]")
  console.log("")
  console.log("  -h,   --help      Print this help and exit.")
  console.log("")
  console.log("  -c,   --coin      Get raw coin flips.")
  console.log("  -s,   --spins     Get raw coin flips and spins per flip.")
  console.log("  -f,   --fair      Get fair coin flips (von Neumann extracted).")
  console.log("")
  console.log("  -b,   --byte      Get raw bytes.")
  console.log("  -v,   --neumann   Get fair bytes (von Neumann extracted).")
  console.log("")
  console.log("  -2,   --sha256    Get 256 bits in hex (SHA-256 hashed). Default.")
  console.log("  -x,   --hex       Get 256 bits in hex (von Neumann extracted).")
  console.log("")
  console.log("  -n #, --num #     Print requested data a specific number of times.")

  process.exit(0)
}

/**
 * Returns a high resolution timestamp with sub-millisecond accuracy since script execution.
 * @returns {number} Floating point milliseconds.
 */
function now() {
  return performance.now()
}

/**
 * Sets a timer 100 microseconds in the future, flips a bit between 0/1 until the timer expires
 * while also counting bit flips.
 * @returns {Array} Result of the coin flip and number of cycles per flip.
 */
function flip_coin() {
  let coin = 0
  let cycles = 0
  const later = now() + 0.1

  while(now() <= later) {
    coin ^= 1
    cycles++
  }

  return [coin, cycles]
}

/**
 * John von Neumann randomness extractor. If two consecutive non-overlapping bits are different,
 * return the first bit.
 * @returns {number} 0 or 1.
 */
function fair_bit() {
  while(1) {
    const bit = flip_coin()[0]
    if(bit != flip_coin()[0]) return(bit)
  }
}

/**
 * Builds an 8-bit byte, either raw for SHA-256 hashing, or unbiased via von Neumann randomness
 * extraction.
 * @param {string} extractor Either "raw" or "neumann".
 * @returns {number} Decimal number 0-255.
 */
function get_byte(extractor) {
  let byte = 0
  let bits = 8

  while(bits--) {
    byte <<= 1

    if(extractor === "raw")
      // Raw bits are okay for SHA-256 hashing *after* the fact.
      byte |= flip_coin()[0]
    else if (extractor === "neumann")
      // Unbiased bits are required *before* returning to the user.
      byte |= fair_bit()
    else
      process.exit(1)
  }

  return byte
}

/**
 * Generates a 256-bit hexadecimal string from von Neumann debiased bits.
 * @returns {string} 64 hexadecimal characters, zero-padded.
 */
function fair_bytes() {
  let count = 32
  const results = new Uint8Array(count)

  while(count--) results[count] = get_byte("neumann")

  return Buffer.from(results).toString("hex");
}

/**
 * Generates a 256-bit hexadecimal string from SHA-256 hashing.
 * @returns {string} 64 hexadecimal characters, zero-padded.
 */
function hash_bytes() {
  let count = 32
  const results = new Uint8Array(count)

  while(count--) results[count] = get_byte("raw")

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
         if (args.includes("-h") || args.includes("--help"))    print_usage()
    else if (args.includes("-c") || args.includes("--coin"))    console.log(flip_coin()[0])
    else if (args.includes("-s") || args.includes("--spins"))   console.log(flip_coin()[1])
    else if (args.includes("-f") || args.includes("--fair"))    console.log(fair_bit())
    else if (args.includes("-b") || args.includes("--bytes"))   console.log(get_byte("raw"))
    else if (args.includes("-v") || args.includes("--neumann")) console.log(get_byte("neumann"))
    else if (args.includes("-2") || args.includes("--sha256"))  console.log(hash_bytes())
    else if (args.includes("-x") || args.includes("--hex"))     console.log(fair_bytes())
    else                                                        console.log(hash_bytes())
  }
}
