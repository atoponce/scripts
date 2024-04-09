"use strict"

/** Class representing the HC-128 stream cipher */
modules.exports = class HC128 {
  #P        // S-box of 512 32-bit unsigned integers
  #Q        // S-box of 512 32-bit unsigned integers
  #W        // Intermediat table to build P and Q s-boxes
  #counter  // Global counter for the keystream

  /**
   * Initialize HC-128 to its standard initial state.
   * @param {Uint32Array} key A 4-element array of 32-bit unsigned integers.
   * @param {Uint32Array} iv A 4-element array of 32-bit unsigned integers.
   */
  constructor(key, iv) {
    if (typeof key === "undefined") {
      key = new Uint32Array([0, 0, 0, 0])
    }

    if (typeof iv === "undefined") {
      iv = new Uint32Array([0, 0, 0, 0])
    }

    if (!(key instanceof Uint32Array) || key.length !== 4) {
      throw new Error("Key must be a 4-element Uint32Array")
    }

    if (!(iv instanceof Uint32Array) || iv.length !== 4) {
      throw new Error("IV must be a 4-element Uint32Array")
    }

    this.#P = new Array(512)
    this.#Q = new Array(512) 
    this.#W = new Array(1280)
    this.#counter = 0

    // Step 1. Expand key and IV into table W.
    for (let i = 0; i < 4; i++) {
      this.#W[i] = key[i]
      this.#W[i + 4] = key[i]
      this.#W[i + 8] = iv[i]
      this.#W[i + 12] = iv[i]
    }

    for (let i = 16; i < 1280; i++) {
      this.#W[i] =
        this.#add(this.#f2(this.#W[i - 2]),
        this.#add(this.#W[i - 7],
        this.#add(this.#f1(this.#W[i - 15]),
        this.#add(this.#W[i - 16], i)
      )))
    }

    // Step 2. Update the tables P and Q with the array W.
    for (let i = 0; i < 512; i++) {
      this.#P[i] = this.#W[i + 256]
      this.#Q[i] = this.#W[i + 768]
    }

    // Step 3. Run the cipher 1024 steps and use the outputs to replace the P and Q table elements.
    for (let i = 0; i < 512; i++) {
      this.#P[i] =
        this.#add(
          this.#P[i], this.#g1(this.#P.at(i - 3), this.#P.at(i - 10), this.#P.at(i - 511))) ^
          this.#h1(this.#P.at(i - 12)
        )
      this.#Q[i] =
        this.#add(
          this.#Q[i], this.#g2(this.#Q.at(i - 3), this.#Q.at(i - 10), this.#Q.at(i - 511))) ^
          this.#h2(this.#Q.at(i - 12)
        )
    }
  }

  /**
   * Add two numbers modulo 4294967296
   * @param {number} x An unsigned 32-bit integer.
   * @param {number} y An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #add(x, y) {
    return ((x + y) & 0xffff_ffff) >>> 0
  }

  /**
   * Right rotation operator.
   * @param {number} x An unsigned 32-bit integer.
   * @param {number} n An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #rotr32(x, n) {
    return ((x >>> n) | (x << (32 - n))) >>> 0
  }

  /**
   * Left rotation operator.
   * @param {number} x An unsigned 32-bit integer.
   * @param {number} n An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #rotl32(x, n) {
    return ((x << n) | (x >>> (32 - n))) >>> 0
  }

  /**
   * Key/IV expansion function in the table W. Also the SHA-256 σ0(x) function.
   * @param {number} x An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #f1(x) {
    return (this.#rotr32(x, 7) ^ this.#rotr32(x, 18) ^ (x >>> 3)) >>> 0
  }

  /**
   * Key/IV expansion function in the table W. Also the SHA-256 σ1(x) function.
   * @param {number} x An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #f2(x) {
    return (this.#rotr32(x, 17) ^ this.#rotr32(x, 19) ^ (x >>> 10)) >>> 0
  }

  /**
   * Non-linear diffusion function for the table P.
   * @param {number} x An unsigned 32-bit integer.
   * @param {number} y An unsigned 32-bit integer.
   * @param {number} z An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #g1(x, y, z) {
    return this.#add(this.#rotr32(x, 10) ^ this.#rotr32(z, 23), this.#rotr32(y, 8))
  }

  /**
   * Non-linear diffusion function for the table Q.
   * @param {number} x An unsigned 32-bit integer.
   * @param {number} y An unsigned 32-bit integer.
   * @param {number} z An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #g2(x, y, z) {
    return this.#add(this.#rotl32(x, 10) ^ this.#rotl32(z, 23), this.#rotl32(y, 8))
  }

  /**
   * S-box diffusion function for table P, operating on table Q.
   * @param {number} x An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #h1(x) {
    const x0 = x & 0xff
    const x2 = (x >>> 16) & 0xff
    return this.#add(this.#Q[x0], this.#Q[256 + x2])
  }

  /**
   * S-box diffusion function for table Q, operating on table P.
   * @param {number} x An unsigned 32-bit integer.
   * @returns An unsigned 32-bit integer.
   */
  #h2(x) {
    const x0 = x & 0xff
    const x2 = (x >>> 16) & 0xff
    return this.#add(this.#P[x0], this.#P[256 + x2])
  }

  /**
   * Keystream generator. Tracks a global counter modulo 1024. If the counter is
   * less than 512, keystream output comes from table P, otherwise keystream
   * output comes from table Q.
   * @returns An unsigned 32-bit integer.
   */
  #genKeystream() {
    let s
    const i = (this.#counter & 0x1ff)

    if (this.#counter < 512) {
      this.#P[i] = this.#add(this.#P[i], this.#g1(this.#P.at(i - 3), this.#P.at(i - 10), this.#P.at(i - 511)))
      s = (this.#h1(this.#P.at(i - 12)) ^ this.#P[i]) >>> 0
    } else {
      this.#Q[i] = this.#add(this.#Q[i], this.#g2(this.#Q.at(i - 3), this.#Q.at(i - 10), this.#Q.at(i - 511)))
      s = (this.#h2(this.#Q.at(i - 12)) ^ this.#Q[i]) >>> 0
    }

    this.#counter = (this.#counter + 1) & 0x3ff
    return s
  }

  /**
   * Encrypt and decrypt data. Must be a multiple of 32 bits.
   * TODO: Remove 32-bit multiple restriction. This *IS* a stream cipher after
   * all, not a block cipher.
   * @param {Uint32Array} data An array of data to XOR against the keystream.
   * @returns Array of plaintext or ciphertext.
   */
  #update(data) {
    if (!(data instanceof Uint32Array)) {
      throw new Error("Data must be a Uint32Array")
    }

    if ((data.length % 4) !== 0) {
      throw new Error("For the time being, data must be a multiple of 32 bits.")
    }

    const output = new Uint32Array(data.length)

    for (let i = 0; i < data.length; i++) {
      output[i] = data[i] ^ this.#genKeystream()
    }

    return output
  }

  /**
   * Encrypt data.
   * @param {Uint32Array} data An array of plaintext data.
   * @returns Array of ciphertext.
   */
  encrypt(data) {
    return this.#update(data)
  }

  /**
   * Decrypt data.
   * @param {Uint32Array} data An array of ciphertext data.
   * @returns Array of plaintext.
   */
  decrypt(data) {
    return this.#update(data)
  }
}