"use strict"

/** Class representing the Spritz CSPRNG. */
class Spritz {
  #a // Counts how many nibbles have been absorbed.
  #i // Increases by w % 256 when drip() is called.
  #j // Changes pseudorandomly.
  #k // Changes pseudorandomly.
  #w // Always relatively prime to 256, updated when whip(r) is called.
  #z // Records the last output byte produces.
  #S // Spritz state array.

  /** Initialize Spritz to its standard initial state. Hard-coded to N=256. */
  constructor(key, iv) {
    if (typeof key === "undefined") {
      key = new Uint8Array(Array(16).fill(0))
    }

    if (typeof iv === "undefined") {
      iv = new Uint8Array(Array(16).fill(0))
    }

    if (!(key instanceof Uint8Array) || key.length !== 16) {
      throw new Error("Key must be a 16-element Uint8Array.")
    }

    if (!(iv instanceof Uint8Array) || iv.length !== 16) {
      throw new Error("IV must be a 16-element Uint8Array.")
    }

    this.#a = 0
    this.#i = 0
    this.#j = 0
    this.#k = 0
    this.#w = 1
    this.#z = 0
    this.#S = Array.from(Array(256), (_, n) => n)

    this.#absorb(key)
    this.#absorbStop()
    this.#absorb(iv)
  }

  /**
   * Swaps two elements in an array.
   * @param {Array} arr - An array of integer elements.
   * @param {number} x - An array index.
   * @param {number} y - An array index.
   * @return {Array} - The updated array with swapped elements.
   */
  #swap(arr, x, y) {
    return ([arr[x], arr[y]] = [arr[y], arr[x]])
  }

  /**
   * Adds two numbers modulo 256.
   * @param {number} x - An integer.
   * @param {number} y - An integer.
   * @return {number} - The sum of x and y modulo 256.
   */
  #add(x, y) {
    return (x + y) & 0xff
  }

  /**
   * Take a variable-length input sequence and updates the Spritz state. Can be
   * called for additional input even after it has produced some output, since
   * absorb() merely updates the current state without re-initializing it. This
   * corresponds to "duplex mode" in sponge function terminology. An input "I"
   * may be supplied in pieces, each of non-negative length, using absorb(x) on
   * each piece. It doesn't matter how the input is divided into pieces since
   * "absorb(x); absorb(y);" is equivalent to "absorb(xy)".
   * @param {Uint8Array} I - An array of unsigned 8-bit integers.
   */
  #absorb(I) {
    if (!(I instanceof Uint8Array)) {
      throw new Error("Data must be a Uint8Array.")
    }

    const l = I.length

    for (let v = 0; v < l; v++) {
      this.#absorbByte(I[v])
    }
  }

  /**
   * Updates the current Spritz state based on a given byte by splitting the
   * byte into two nibbles and updating the state based on each nibble,
   * low-order first.
   * @param {number} b - An unsigned 8-bit integer.
   */
  #absorbByte(b) {
    this.#absorbNibble(b & 0xf) // low
    this.#absorbNibble(b >> 4) // high
  }

  /**
   * First test whether Spritz is "full" of absorbed data. If so, calls
   * shuffle() to mix the absorbed data and reset a to 0. Then updates the state
   * based on the value of the supplied nibble.
   * @param {number} x - An unsigned 4-bit integer.
   */
  #absorbNibble(x) {
    if (this.#a >= 128) {
      this.#shuffle()
    }

    this.#swap(this.#S, this.#a, this.#add(128, x))

    this.#a += 1
  }

  /**
   * Same as absorbNibble(x), except no swapping is done. May be used to ensure
   * that the input from the preceding absorb(I) and that of a following
   * absorb(I) are cleanly separated. More precisely, "absorb(x); absorb(y);" is
   * fully equivalent to "absorb(xy)"". Putting absorbStop() between the two
   * calls to absorb(I) ensures this is not true.
   */
  #absorbStop() {
    if (this.#a >= 128) {
      this.#shuffle()
    }

    this.#a += 1
  }

  /**
   * Whips, crushes, whips, crushes, and then whips again. Each whip(r)
   * randomizes the state. Because crush() is called between each pair of calls
   * to whip(r), the effects of crush() are not easily determined by
   * manipulating the input, and any biases introduced by crush() are smoothed
   * out before shuffle() returns. The parameter "2 * N" on the size of each
   * whip(r) is chosen to produce a strong isolation of shuffle() inputs/outputs
   * and crush() inputs/outputs from each other.
   */
  #shuffle() {
    this.#whip(512)
    this.#crush()
    this.#whip(512)
    this.#crush()
    this.#whip(512)

    this.#a = 0
  }

  /**
   * Calls update() a specified number of r-times. The Spritz system is "being
   * whipped" without producing output. The registers and permutation state are
   * given new values that is a complex function of their initial values, with
   * larger values of "r" resulting in more complexity. The use of whip(r)
   * reflect a common recommendation for improving RC4. Every whip(r) call also
   * updates "w" to the next larger value that is relatively prime to "N", so
   * that the repeated execution of "i += w" in the first line of update()
   * causes "i" to cycle between all values modulo 256.
   * @param {number} r - How many times to call update() without output.
   */
  #whip(r) {
    for (let v = 0; v < r; v++) {
      this.#update()
    }

    this.#w += 2 // Always odd, thus relatively prime to 256.
  }

  /**
   * Provides a non-invertible transformation from states to states.
   * Intentionally "loses information" about the current state. More precisely,
   * it maps 2^(N/2) states to one, since each 256/2 pairs of compared values in
   * the state are sorted into increasing order.
   */
  #crush() {
    for (let v = 0; v < 128; v++) {
      const i = 255 - v

      if (this.#S[v] > this.#S[i]) {
        this.#swap(this.#S, v, i)
      }
    }
  }

  /**
   * The main output function for Spritz. The name derives from the terminology
   * of sponge functions (think squeezing water from a sponge). Equivalent to
   * calling drip() r-times.
   * @param {number} r - How many output bytes (N-values) to produce.
   * @return {Uint8Array} - An r-length array of unsigned random integers.
   */
  #squeeze(r) {
    if (this.#a > 0) {
      this.#shuffle()
    }

    const p = []

    for (let v = 0; v < r; v++) {
      p.push(this.#drip())
    }

    return new Uint8Array(p)
  }

  /**
   * The basic pseudorandom output routine designed to ensure that Spritz is in
   * "squeezing mode", updates the Spritz state using update(), and produces one
   * output byte using output(). The test for a > 0 and call to shuffle() are
   * placed both here and in squeeze(r) so that drip() may be safely called
   * directly by applications, ensuring that absorbed data is always shuffled
   * before any output is produced.
   * @return {number} - An unsigned random integer.
   */
  #drip() {
    if (this.#a > 0) {
      this.#shuffle()
    }

    this.#update()

    return this.#output()
  }

  /**
   * Advances the system to the next state by adding "w" to "i", giving "j" and
   * "k" their next values, and swapping "Spritz.i" and "Spritz.j". Since "w" is
   * relatively prime to "N", the value of "i" cycles modulo 256 as repeated
   * updates are performed.
   */
  #update() {
    this.#i = this.#add(this.#i, this.#w)
    this.#j = this.#add(this.#k, this.#S[this.#add(this.#j, this.#S[this.#i])])
    this.#k = this.#add(this.#i + this.#k, this.#S[this.#j])

    this.#swap(this.#S, this.#i, this.#j)
  }

  /**
   * Computes a single byte (N-value) to output, saves this value in register
   * "z", and returns this value.
   * @return {number} - An unsigned random integer.
   */
  #output() {
    this.#z =
      this.#S[
          this.#add(
              this.#j,
              this.#S[this.#add(this.#i, this.#S[this.#add(this.#z, this.#k)])]
          )
      ]

    // This countermeasure removes distinguishers from the Spritz key stream.
    // See https://www.jstage.jst.go.jp/article/transfun/E100.A/6/E100.A_1296/_article
    this.#z ^= this.#S[255 - this.#i]

    return this.#z
  }

  /**
   * Encrypt and decrypt data
   * @param {Uint8Array} data - An array of data to XOR against the keystream
   * @returns - Array of plaintext or ciphertext
   */
  #process(data) {
    const ks = this.#squeeze(data.length)
    const output = new Uint8Array(data.length)

    for (let i = 0; i < data.length; i++) {
      output[i] = data[i] ^ ks[i]
    }

    return output
  }

  /**
   * Encrypt data.
   * @param {Uint8Array} data An array of plaintext data.
   * @returns - An array of ciphertext data.
   */
  encrypt(data) {
    return this.#process(data)
  }

  /**
   * Decrypt data.
   * @param {Uint8Array} data An array of ciphertext data.
   * @returns - An array of plaintext data.
   */
  decrypt(data) {
    return this.#process(data)
  }
}