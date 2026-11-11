import pytest

# MATH MODULE TESTS





# DIFFIE-HELLMAN MODULE TESTS
from diffie_hellman import generate_diffie_hellman_params
from diffie_hellman import generate_public_key
from diffie_hellman import generate_shared_key

#  GENERAL Diffie-Hellman test
def test_dh_key_exchange():
    p, g = generate_diffie_hellman_params(False)
    
    # Sender
    exp_1, public_key_1 = generate_public_key(p, g)
    # Recipient
    exp_2, public_key_2 = generate_public_key(p, g)
    
    # Exchanging
    senders_secret = generate_shared_key(p, exp_1, public_key_2)
    recipients_secret = generate_shared_key(p, exp_2, public_key_1)
    
    assert senders_secret == recipients_secret


# POSITIVE Diffie-Hellman tests
def test_generate_diffie_hellman_params():
    prime, generator = generate_diffie_hellman_params(False)
    assert 1024 <= prime.bit_length() <= 4096
    assert generator == 2


def test_generate_public_key():
    own_exp, public_key = generate_public_key(7, 2)
    assert own_exp.bit_length() <= 256
    assert public_key == pow(2, own_exp, 7)
    assert 1 <= public_key < 7


def test_generate_shared_key():
    assert generate_shared_key(7, 5, 3) == pow(3, 5, 7) == 5


# NEGATIVE Diffie-Hellman test

def test_negative_generate_diffie_hellman_params():
    with pytest.raises(ValueError):
        generate_diffie_hellman_params(False, 256)
    