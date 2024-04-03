"use strict"

/** Class representing the Trivium stream cipher. */
class Trivium {
  #state      
  #keystream  // Trivium keystream.

  /**
   * Initialize Trivium with key and IV.
   * @param {Uint8Array} key - An 8-bit array of 10 unsigned integers.
   * @param {Uint8Array} iv - An 8-bit array of 10 unsigned integers.
   * @throws {Error}
   */
  constructor(key, iv) {
    if (typeof key === "undefined") {
      key = new Uint8Array([
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0
      ])
    }

    if (typeof iv === "undefined") {
      iv = new Uint8Array([
        0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0
      ])
    }

    if (!(key instanceof Uint8Array)) {
      "Key should be a 10-element Uint8Array."
    }

    if (!(iv instanceof Uint8Array)) {
      "IV should be a 10-element Uint8Array."
    }

    // (s1, .............., s93) | (s94, ..............., s177) | (s178, ......, s288)
    // (k1, ..., k80, 0, ..., 0) | (iv1, ..., iv80, 0, 0, 0, 0) | (0, ..., 0, 1, 1, 1)
    this.#state = Array.from(Array(288), (_, i) => 0)
    for (let i = 0; i < 80; i += 8) {
      this.#state[i + 0] = (key[i >> 3] >> 7) & 0x1
      this.#state[i + 1] = (key[i >> 3] >> 6) & 0x1
      this.#state[i + 2] = (key[i >> 3] >> 5) & 0x1
      this.#state[i + 3] = (key[i >> 3] >> 4) & 0x1
      this.#state[i + 4] = (key[i >> 3] >> 3) & 0x1
      this.#state[i + 5] = (key[i >> 3] >> 2) & 0x1
      this.#state[i + 6] = (key[i >> 3] >> 1) & 0x1
      this.#state[i + 7] = (key[i >> 3] >> 0) & 0x1

      this.#state[i +  93] = (iv[i >> 3] >> 7) & 0x1
      this.#state[i +  94] = (iv[i >> 3] >> 6) & 0x1
      this.#state[i +  95] = (iv[i >> 3] >> 5) & 0x1
      this.#state[i +  96] = (iv[i >> 3] >> 4) & 0x1
      this.#state[i +  97] = (iv[i >> 3] >> 3) & 0x1
      this.#state[i +  98] = (iv[i >> 3] >> 2) & 0x1
      this.#state[i +  99] = (iv[i >> 3] >> 1) & 0x1
      this.#state[i + 100] = (iv[i >> 3] >> 0) & 0x1
    }

    this.#state[285] = 1
    this.#state[286] = 1
    this.#state[287] = 1

    for (let i = 0; i < 4 * 288; i++) {
      this.#genKeyStream()
    }
  }

  /**
   * Generates a keystream bit and manipulates the Trivium state. The Trivium
   * state is defined with three non-linear feedback shift registers: s1 (93
   * bits), s2 (84 bits), and s3 (111 bits). Each state is modified
   * independently and each state depends on a single bit from the other,
   * creating a circular dependency on itself.
   * @returns {number} z - A single keystream bit.
   */
  #genKeyStream() {
    let t1 = this.#state[65] ^ this.#state[92]
    let t2 = this.#state[161] ^ this.#state[176]
    let t3 = this.#state[242] ^ this.#state[287]

    let z = t1 ^ t2 ^ t3

    t1 ^= (this.#state[90] & this.#state[91]) ^ this.#state[170]
    t2 ^= (this.#state[174] & this.#state[175]) ^ this.#state[263]
    t3 ^= (this.#state[285] & this.#state[286]) ^ this.#state[68]

    this.#state.pop()

    this.#state.unshift(t3)
    this.#state[93] = t1
    this.#state[177] = t2

    return z
  }

  /**
   * Generates a large enough keystream to encrypt/decrypt data.
   * @param {number} len - The length of the requested keystream in bits.
   */
  #keyStream(len) {
    this.#keystream = new Uint8Array(len)

    for (let i = 0; i < len; i++) {
      this.#keystream[i] = this.#genKeyStream()
    }
  }

  /**
   * Encrypt and decrypt data.
   * @param {Uint8Array} data - Array of data to XOR with the keystream.
   * @return {Uint8Array} output - Array of plaintext or ciphertext bytes.
   * @throws {Error}
   */
  #update(data) {
    if (!(data instanceof Uint8Array)) {
      throw new Error("Data should be a Uint8Array.")
    }

    const output = new Uint8Array(data.length)
    const keybytes = new Uint8Array(data.length)

    this.#keyStream(data.length << 3)

    for (let i = 0; i < data.length << 3; i += 8) {
      keybytes[i >> 3] = 
        (this.#keystream[i + 0] << 0) |
        (this.#keystream[i + 1] << 1) |
        (this.#keystream[i + 2] << 2) |
        (this.#keystream[i + 3] << 3) |
        (this.#keystream[i + 4] << 4) |
        (this.#keystream[i + 5] << 5) |
        (this.#keystream[i + 6] << 6) |
        (this.#keystream[i + 7] << 7)
    }

    for (let i = 0; i < data.length; i++) {
      output[i] = data[i] ^ keybytes[i]
    }

    return output
  }

  /**
   * Encryption
   * @param {Uint8Array} data - Array of data to encrypt.
   * @returns {Uint8Array} - Array of ciphertext bytes.
   */
  encrypt(data) {
    return this.#update(data)
  }

  /**
   * Decryption
   * @param {Uint8Array} data - Array of data to decrypt.
   * @returns {Uint8Array} - Array of plaintext bytes.
   */
  decrypt(data) {
    return this.#update(data)
  }
}

const key = new Uint8Array([
  0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A, 
])
const iv = new Uint8Array([
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
])
// I can only get the all-zero key and iv test vector to work.
// https://github.com/cantora/avr-crypto-lib/blob/master/testvectors/trivium-80.80.test-vectors#L232
const testVector = new Uint8Array([
  0x2C, 0x7F, 0x53, 0xF2, 0xFD, 0x7C, 0xC9, 0x34, 0x2E, 0xBD, 0xB2, 0x6E, 0x82, 0x45, 0xBB, 0x9F, 
  0x29, 0x8D, 0x54, 0xB7, 0x4A, 0x7E, 0x7C, 0x60, 0x8E, 0x4E, 0xE6, 0xFD, 0x7A, 0x66, 0x08, 0xB6, 
  0x9E, 0xE7, 0x1B, 0x83, 0xD9, 0x63, 0x5C, 0x45, 0x7D, 0xD9, 0xD0, 0x5F, 0xE9, 0x09, 0x0F, 0xBA, 
  0x05, 0xE2, 0x49, 0xD4, 0x42, 0x18, 0xE9, 0x7D, 0x1B, 0x90, 0x5E, 0x4F, 0x08, 0x10, 0xA9, 0x12, 
  //0xFB, 0xE0, 0xBF, 0x26, 0x58, 0x59, 0x05, 0x1B, 0x51, 0x7A, 0x2E, 0x4E, 0x23, 0x9F, 0xC9, 0x7F, 
  //0x56, 0x32, 0x03, 0x16, 0x19, 0x07, 0xCF, 0x2D, 0xE7, 0xA8, 0x79, 0x0F, 0xA1, 0xB2, 0xE9, 0xCD, 
  //0xF7, 0x52, 0x92, 0x03, 0x02, 0x68, 0xB7, 0x38, 0x2B, 0x4C, 0x1A, 0x75, 0x9A, 0xA2, 0x59, 0x9A, 
  //0x28, 0x55, 0x49, 0x98, 0x6E, 0x74, 0x80, 0x59, 0x03, 0x80, 0x1A, 0x4C, 0xB5, 0xA5, 0xD4, 0xF2, 
])
let ptData = new Uint8Array([
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
])

let trivium = new Trivium(key, iv)
let ctData = trivium.encrypt(ptData)

console.log(ctData, testVector)
console.log("Test vector validated?", JSON.stringify(ctData) === JSON.stringify(testVector))