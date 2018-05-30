#!/usr/bin/python

import click
from passlib import hash as ph

def _get_password():
    return raw_input("Enter password: ")

def _apr_md5_crypt(password):
    print(ph.apr_md5_crypt.hash(password))

def _mysql41_crypt(password):
    print(ph.mysql41.hash(password))

def _des_crypt(password):
    print(ph.des_crypt.hash(password))

def _md5_crypt(password):
    print(ph.md5_crypt.hash(password))

def _bcrypt(password, cost=5):
    print(ph.bcrypt.using(rounds=cost).hash(password))

def _bcrypt_sha256(password, cost=5):
    print(ph.bcrypt_sha256.using(rounds=cost).hash(password))

def _sha256_crypt(password, cost=5000):
    print(ph.sha256_crypt.using(rounds=cost).hash(password))

def _sha512_crypt(password, cost=5000):
    print(ph.sha512_crypt.using(rounds=cost).hash(password))

@click.command()
@click.option("--apache", is_flag=1, help="Apache md5crypt password variant.")
@click.option("--mysql", is_flag=1, help="MySQL 4.1 hashing algorithm.")
@click.option("--des", is_flag=1, help="Unix 3DES crypt, truncated to 8 characters.")
@click.option("--md5", is_flag=1, help="FreeBSD md5crypt hash, limited to 1,000 rounds.")
@click.option("--bcrypt", is_flag=1, help="OpenBSD bcrypt hash, truncated to 72 bytes.")
@click.option("--bcrypt_sha256", is_flag=1, help="bcrypt prehashed with SHA-256 and base64, unlimited length.")
@click.option("--sha256", is_flag=1, help="GNU libc sha256crypt hash.")
@click.option("--sha512", is_flag=1, help="GNU libc sha512crypt hash.")
@click.option("--cost", type=int, help="Password hashing cost, if applicable.")
def main(apache, mysql, des, md5, bcrypt, bcrypt_sha256, sha256, sha512, cost):
    if apache:
        _apr_md5_crypt(_get_password())
    if mysql:
        _mysql41_crypt(_get_password())
    if des:
        _des_crypt(_get_password())
    if md5:
        _md5_crypt(_get_password())
    if bcrypt:
        if cost:
            _bcrypt(_get_password(), cost)
        else:
            _bcrypt(_get_password())
    if bcrypt_sha256:
        if cost:
            _bcrypt_sha256(_get_password(), cost)
        else:
            _bcrypt_sha256(_get_password())
    if sha256:
        if cost:
            _sha256_crypt(_get_password(), cost)
        else:
            _sha256_crypt(_get_password())
    if sha512:
        if cost:
            _sha512_crypt(_get_password(), cost)
        else:
            _sha512_crypt(_get_password())
        
if __name__ == '__main__':
    main()
