#!/bin/bash

# Author: Aaron Toponce
# Date: Apr 11, 2013
# License: Released to the public domain

# Find a random starting point on my password card
# See https://passwordcard.org for more details

COLS=( '■' '□' '▲' '△' '○' '●' '★' '☂' '☀' '☁' '☹' '☺' '♠' '♣' '♥' '♦' '♫' '€' '¥' '£' '$' '!' '?' '¡' '¿' '⊙' '◐' '◩' '�' )
ROWS=( 1 2 3 4 5 6 7 8)

echo ${COLS[$(($RANDOM%29+1))]}${ROWS[$(($RANDOM%8+1))]}
