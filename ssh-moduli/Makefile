# - makefile -
# vim: set noexpandtab sw=2 ts=2 cc=80 tw=78
#
# Run in parallel:
#		$ make -j $(nproc)
#
# Based on https://github.com/j0ju/ssh-moduli-generator/
# LICENSE: GPLv2
# Author: Joerg Jungermann, Aaron Toponce
#
# OpenSSH only ships 2048, 3072, 4096, 6144, 7680, and 8192-bit DH group
# moduli. This is because they are hard-coded in OpenSSH dh.c source code:
#
#	u_int dh_estimate(int bits) {
#		if (bits <= 112)
#			return 2048;
#		if (bits <= 128)
#			return 3072;
#		if (bits <= 192)
#			return 7680;
#		return 8192;
#	}
#
# The DH KEX modulus size is determined from the symmetric cipher key size in
# bits. This comes from NIST SP 800-57 Part 1 rev. 5 (May 2020):
#
#	| Symmetric |  DH Group  |
#	|:---------:|:----------:|
#	|   80 bits |  1024 bits |
#	|  112 bits |  2048 bits |
#	|  128 bits |  3072 bits |
#	|  192 bits |  7680 bits |
#	|  256 bits | 15360 bits |
#
# This means the 4096-bit and 6144-bit modulus shipped by default are for
# backward-compatability with older clients. There's no benefit no building
# moduli with other sizes unless you know you need 1024-bit or 1536-bit. The
# 8192-bit modulus is likely an upper cap for performance & disk space
# reasons.
#
# See https://fosstodon.org/@atoponce/114071816298119775 for more context.

TARGET =
TARGET += 2048
TARGET += 3072
TARGET += 4096
TARGET += 6144
TARGET += 7680
TARGET += 8192

all: $(addsuffix .moduli,$(TARGET))

%.candidates:
	rm -f $@
	ssh-keygen -M generate -O bits=$(@:.candidates=) $@

%.moduli: %.candidates
	ssh-keygen -M screen -f $< $@ && rm -f $<

.SUFFIXES:

# This allows to generate moduli candidates in advance and resume
# the calculation of modulis after candidates have been generated
# On the other hand we need to handle (un)successful creation and deletion
# of intermediate files ourselves
.PRECIOUS: %.candidates
