#!/bin/sh
# Reseed the Linux kernel CSPRING with data from Steve Gibson Research Corp
results=$(curl -so - 'https://www.grc.com/passwords.htm')
echo -n "$results" | grep -Eo '[[:xdigit:]]{64}' | paste -sd '' | tr A-F a-f
