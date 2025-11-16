/**
 * Copyright (C) 2025 Aaron Toponce
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License version 3 for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
 */

/**
 * RFC 9562-compliant UUID generator
 */
class UUID {
  #hexBytes = []; // 8 bits
  #hexWords = []; // 16 bits
  #node = "";

  constructor() {
    for (let i = 0; i < 0x100; i++) {
      this.#hexBytes[i] = i.toString(16).padStart(2, "0");
    }

    for (let i = 0; i < 0x10000; i++) {
      this.#hexWords[i] = i.toString(16).padStart(4, "0");
    }

    // Generate a RFC 9542 MAC address from the reserved documentation range
    // 00-00-5E-00-53-00 through 00‑00‑5E‑00‑53‑FF for unicast and
    // 01‑00‑5E‑90‑10‑00 through 01‑00‑5E‑90‑10‑FF for multicast.
    this.#node = "00005e0053" + this.#hexBytes[Math.random() * 0x100 >>> 0];
  }

  /**
   * Generate the nil RFC 9562 UUID.
   * @returns {String} Returns the RFC 9562 nil UUID string.
   */
  nil() {
    return "00000000-0000-0000-0000-000000000000";
  }

  /**
   * Generate the maximum RFC 9562 UUID.
   * @returns {String} Returns the RFC 9562 max UUID string.
   */
  max() {
    return "ffffffff-ffff-ffff-ffff-ffffffffffff";
  }

  /**
   * Generate a version 1 UUID. JavaScript does not support nanosecond
   * resolution for security reasons. As such, the best this function can offer
   * is 1 millisecond precision while maintaining high performance.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 1 string.
   */
  v1() {
    const now = Date.now() * 10000 + 0x01b21dd213814000;

    return (
      this.#hexWords[now & 0xffff] + // time_low
      this.#hexWords[now >> 16 & 0xffff] + "-" +
      this.#hexWords[Math.floor(now / 2**32) & 0xffff] + "-" + // time_mid
      this.#hexWords[Math.floor(now / 2**48) & 0x0fff | 0x1000] + "-" + // ver & time_high
      this.#hexWords[Math.random() * 0x10000 & 0x3fff | 0x8000] + "-" + // var && clock_seq
      this.#node // node
    );
  }

  /**
   * UUIV2 is not defined in RFC 9562 but in a POSIX document for DEC.
   * @returns {String} Returns text that this class does not generate UUIDv2.
   */
  v2() {
    return "Not implemented as it's not defined in RFC 9562.";
  }

  /**
   * Generate a verison 3 UUID. Both RFC 4122 and 9562 mention that unless you
   * know you need backwards compatibility with MD5, you should use SHA-1
   * instead. Both UUIDv3 and UUIDv5 are identical except for the algorithm. So
   * MD5 is here, per the RFC, and SHA-1 is found in v5().
   * 
   * The following namespaces are predefined in the RFC and available for use:
   * - DNS: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
   * - URL: 6ba7b811-9dad-11d1-80b4-00c04fd430c8
   * - OID: 6ba7b812-9dad-11d1-80b4-00c04fd430c8
   * - X500: 6ba7b814-9dad-11d1-80b4-00c04fd430c8
   * @param {String} namespace The globally unique identifier for the namespace.
   * @param {String} name The corresponding name for the namespace.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 3 string.
   */
    v3(namespace, name) {
    const crypto = require("crypto");
    const hash = crypto.createHash("md5");

    namespace = namespace.replace(/-/g, "");
    namespace = Buffer.from(namespace, "hex");

    hash.update(namespace);
    hash.update(name);
    
    const digest = hash.digest();

    digest[6] = (digest[6] & 0x0f) | 0x30;
    digest[8] = (digest[8] & 0x3f) | 0x80;

    return (
      this.#hexBytes[digest[0]] + this.#hexBytes[digest[1]] +
      this.#hexBytes[digest[2]] + this.#hexBytes[digest[3]] + "-" +
      this.#hexBytes[digest[4]] + this.#hexBytes[digest[5]] + "-" +
      this.#hexBytes[digest[6]] + this.#hexBytes[digest[7]] + "-" +
      this.#hexBytes[digest[8]] + this.#hexBytes[digest[9]] + "-" +
      this.#hexBytes[digest[10]] + this.#hexBytes[digest[11]] +
      this.#hexBytes[digest[12]] + this.#hexBytes[digest[13]] +
      this.#hexBytes[digest[14]] + this.#hexBytes[digest[15]]
    );
  }

  /**
   * Generate a version 4 UUID. Do not use for security, privacy, or any type of
   * risk. Use crypto.randomUUID() instead.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 4 string.
   */
  v4() {
    const r1 = (Math.random() * 0x100000000) >>> 0;
    const r2 = (Math.random() * 0x100000000) >>> 0;
    const r3 = (Math.random() * 0x100000000) >>> 0;
    const r4 = (Math.random() * 0x100000000) >>> 0;

    return (
      this.#hexWords[r1 >>> 16] + // random_a
      this.#hexWords[r1 & 0xffff] + "-" +
      this.#hexWords[r2 >>> 16] + "-" +
      this.#hexWords[(r2 & 0x0fff) | 0x4000] + "-" + // ver && random_b
      this.#hexWords[((r3 >>> 16) & 0x3fff) | 0x8000] + "-" + // var & random_c
      this.#hexWords[r3 & 0xffff] +
      this.#hexWords[r4 >>> 16] +
      this.#hexWords[r4 & 0xffff]
    );
  }

  /**
   * Generate a verison 5 UUID. Both RFC 4122 and 9562 mention that unless you
   * know you need backwards compatibility with MD5, you should use SHA-1
   * instead. Both UUIDv3 and UUIDv5 are identical except for the algorithm. So
   * SHA-1 is here, per the RFC, and MD5 is found in v3().
   * 
   * The following namespaces are predefined in the RFC and available for use:
   * - DNS: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
   * - URL: 6ba7b811-9dad-11d1-80b4-00c04fd430c8
   * - OID: 6ba7b812-9dad-11d1-80b4-00c04fd430c8
   * - X500: 6ba7b814-9dad-11d1-80b4-00c04fd430c8
   * @param {String} namespace The globally unique identifier for the namespace.
   * @param {String} name The corresponding name for the namespace.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 5 string.
   */
  v5(namespace, name) {
    const crypto = require('crypto');
    const hash = crypto.createHash('sha1');

    namespace = namespace.replace(/-/g, "");
    namespace = Buffer.from(namespace, "hex");

    hash.update(namespace);
    hash.update(name);
    
    const digest = hash.digest();

    digest[6] = (digest[6] & 0x0f) | 0x30;
    digest[8] = (digest[8] & 0x3f) | 0x80;

    return (
      this.#hexBytes[digest[0]] + this.#hexBytes[digest[1]] +
      this.#hexBytes[digest[2]] + this.#hexBytes[digest[3]] + "-" +
      this.#hexBytes[digest[4]] + this.#hexBytes[digest[5]] + "-" +
      this.#hexBytes[digest[6]] + this.#hexBytes[digest[7]] + "-" +
      this.#hexBytes[digest[8]] + this.#hexBytes[digest[9]] + "-" +
      this.#hexBytes[digest[10]] + this.#hexBytes[digest[11]] +
      this.#hexBytes[digest[12]] + this.#hexBytes[digest[13]] +
      this.#hexBytes[digest[14]] + this.#hexBytes[digest[15]]
    );
  }

  /**
   * Generate a version 6 UUID. JavaScript does not support nanosecond
   * resolution for security reasons. As such, the best this function can offer
   * is 1 millisecond precision while maintaining high performance.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 6 string.
   */
  v6() {
    const now = Date.now() * 10000 + 0x01b21dd213814000;

    return (
      this.#hexWords[Math.floor(now / 2**48)] +
      this.#hexWords[Math.floor(now / 2**32) & 0xffff] + "-" +
      this.#hexWords[now >>> 16 & 0xffff] + "-" +
      this.#hexWords[now & 0x0fff | 0x6000] + "-" +
      this.#hexWords[(Math.random() * 0x10000 >>> 0) & 0x3fff | 0x8000] + "-" +
      this.#node
    );
  }

  /**
   * Generate a version 7 UUID.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 7 string.
   */
  v7() {
    const now = Date.now();
    const r1 = (Math.random() * 0x3000) >>> 0;
    const r2 = (Math.random() * 0x40000000) >>> 0;
    const r3 = (Math.random() * 0x100000000) >>> 0;

    return (
      this.#hexWords[Math.floor(now / 2**32)] + // unix_ts_ms
      this.#hexWords[now >>> 16 & 0xffff] + "-" +
      this.#hexWords[now & 0xffff] + "-" +
      this.#hexWords[r1 & 0x0fff | 0x7000] + "-" + // ver & rand_a
      this.#hexWords[r2 >>> 16 & 0x3fff | 0x8000] + "-" + // var & rand_b
      this.#hexWords[r2 & 0xffff] + // rand_b
      this.#hexWords[r3 >>> 16] +
      this.#hexWords[r3 & 0xffff]
    );
  }

  /**
   * Generate a version 8 UUID that includes time and space by combining the
   * Unix epoch timestamp in milliseconds with latitude and longitude in decimal
   * degrees.
   * 
   * The specification is as follows:
   *   - 48 bits for Unix epoch timestamp
   *   - 10 bits random
   *   - 32 bits latitude (6 decimal degree precision)
   *   - 32 bits longitude (6 decimal degree precision)
   *
   * Latitude calculaton (-90° to 90°):
   *   - Add 90
   *   - Multiply by 2**24
   *   - Encode as hex
   *   - Storage: 32 bits
   *
   * Longitude calculation (-180° to 180°):
   *   - Add 180
   *   - Multiply by 2**23
   *   - Encode as hex
   *   - Storage: 32 bits
   *
   * The layouta is as follows:
   * 
   *     0                   1                   2                   3
   *     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   *     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   *     |                         unix_ts_ms                            |
   *     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   *     |          unix_ts_ms           |  ver  |       rand_a      |lat|
   *     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   *     |var|                          lat                              |
   *     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   *     |                              lon                              |
   *     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   * 
   * @param {Number} unix The number of milliseconds since the Unix epoch.
   * @param {Number} lat The latitude GPS coordinate in decimal degrees.
   * @param {Number} lon The longitude GPS coordinate in decimal degrees.
   * @returns {String} Returns an RFC 9562-compliant UUID Version 8 string.
   */
  v8(unix, lat, lon) {
    const r1 = (Math.random() * 0x10000) >>> 0;
    lat = ((lat + 90) * 2**24) >>> 0;
    lon = ((lon + 180) * 2**23) >>> 0;

    return (
      this.#hexWords[Math.floor(unix / 2**32)] +
      this.#hexWords[unix >>> 16 & 0xffff] + "-" +
      this.#hexWords[unix & 0xffff] + "-" +
      this.#hexWords[r1 & 0x0ffc | 0x8000 | lat >>> 30] + "-" +
      this.#hexWords[lat >>> 16 & 0x3fff | 0x8000] + "-" +
      this.#hexWords[lat & 0xffff] +
      this.#hexWords[lon & 0xffff] +
      this.#hexWords[lon & 0xffff]
    );
  }
}
