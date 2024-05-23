class Chaocipher {
    #left
    #right

    constructor(l,  r) {
        if (typeof l === "undefined") {
            throw new Error("Left disk is not defined.")
        }

        if (typeof r === "undefined") {
            throw new Error("Right disk is not defined.")
        }

        if ((/^[^A-Z]{26}$/).test(l)) {
            throw new Error("Left disk must contain all 26 uppercase characters.")
        }

        if ((/^[^A-Z]{26}$/).test(r)) {
            throw new Error("Right disk must contain all 26 uppercase characters.")
        }

        this.#left = l
        this.#right = r
    }

    #rotate(n) {
        this.#left = this.#left.substring(n, 26) + this.#left.substring(0, n)
        this.#right = this.#right.substring(n, 26) + this.#right.substring(0, n)
    }

    #permute() {
        this.#left = this.#left[0] + this.#left.substring(2, 14) + this.#left[1] + this.#left.substring(14, 26)
        this.#right = this.#right.substring(1, 26) + this.#right[0]
        this.#right = this.#right[0] + this.#right[1] + this.#right.substring(3, 14) + this.#right[2] + this.#right.substring(14, 26)
    }

    output(msg, enc) {
        let txt = ""
        for (let i = 0; i < msg.length; i++) {
            let n
            if (enc) {
                n = this.#right.indexOf(msg[i])
                txt += this.#left[n]
            } else {
                n = this.#left.indexOf(msg[i])
                txt += this.#right[n]
            }
            this.#rotate(n)
            this.#permute()
        }
        return txt
    }
}

const left = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
const right = "PTLNBQDEOYSFAVZKGJRIHWXUMC"
const chaocipher = new Chaocipher(left, right)
const pt = "WELLDONEISBETTERTHANWELLSAID"
const ct = chaocipher.output(pt, 1)
console.log(ct)