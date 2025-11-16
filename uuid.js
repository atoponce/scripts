/**
 * RFC 9562-compliant UUID generator
 */
class UUID {
  #hexNibbles = []; // 4 bits
  #hexBytes = []; // 8 bits
  #hexWords = []; // 16 bits
  #clockSeq;
  #node = "";

  constructor() {
    this.#hexNibbles = "0123456789abcdef".split("");

    for (let i = 0; i < 0x100; i++) {
      this.#hexBytes[i] = i.toString(16).padStart(2, "0");
    }

    for (let i = 0; i < 0x10000; i++) {
      this.#hexWords[i] = i.toString(16).padStart(4, "0");
    }

    this.#clockSeq = Math.random() * 0x4000 >>> 0;
    this.#node = "00005e0053" + this.#hexBytes[Math.random() * 0x100 >>> 0];
  }

  max() {
    return "ffffffff-ffff-ffff-ffff-ffffffffffff";
  }

  nill() {
    return "00000000-0000-0000-0000-000000000000";
  }

  /**
   * Generate a version 1 UUID. JavaScript does not support high resolution,
   * nanosecond-precise timestamps for security reasons. As such, the best this
   * function can offer is 1-ms precision.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 1 string.
   */
  v1() {
    const now = Date.now() * 10000 + 0x01b21dd213814000;
    this.#clockSeq += 1;

    return (
      this.#hexWords[now & 0xffff] +
      this.#hexWords[now >> 16 & 0xffff] + "-" +
      this.#hexWords[Math.floor(now / 2**32) & 0xffff] + "-" +
      this.#hexWords[Math.floor(now / 2**48) & 0x0fff | 0x1000] + "-" +
      this.#hexWords[this.#clockSeq & 0x3fff | 0x8000] + "-" +
      this.#node
    );
  }

  v2() {
    return "Not implemented as it's not defined in RFC 9562.";
  }

  v3() { } // md5(namespace id)

  /**
   * Generate a version 4 UUID. Do not use for security, privacy, or any type of
   * risk. Use crypto.randomUUID() instead.
   * @returns 
   */
  v4() {
    const r1 = (Math.random() * 0x100000000) >>> 0;
    const r2 = (Math.random() * 0x100000000) >>> 0;
    const r3 = (Math.random() * 0x100000000) >>> 0;
    const r4 = (Math.random() * 0x100000000) >>> 0;

    return (
      this.#hexWords[r1 >>> 16] +
      this.#hexWords[r1 & 0xffff] + "-" +
      this.#hexWords[r2 >>> 16] + "-" +
      this.#hexWords[(r2 & 0x0fff) | 0x4000] + "-" +
      this.#hexWords[((r3 >>> 16) & 0x3fff) | 0x8000] + "-" +
      this.#hexWords[r3 & 0xffff] +
      this.#hexWords[r4 >>> 16] +
      this.#hexWords[r4 & 0xffff]
    );
  }

  v5() { } // sha-1(namespace id)
  v6() { } // field-compatible version of v1
  v7() { } // unix epoch timestamp ms
  v8() { } // custom vendor-specific uses

  ops() {
    let ctr = 0;
    const stop = Date.now() + 1000;

    do {
      ctr++;
      this.v1();
    } while (Date.now() <= stop);

    console.log(this.v1());
    return ctr;
  }

  cpb() {
    const results = [];

    for (let i = 10; i > 0; i--) {
      results[i] = uuid.ops();
    }

    const average = array => array.reduce((a, b) => a + b) / array.length;
    const avg = average(results);
    const cpb = 1.9 * 1000 ** 3 / (36 * avg);

    return cpb;
  }
}

const uuid = new UUID();
console.log(uuid.ops());