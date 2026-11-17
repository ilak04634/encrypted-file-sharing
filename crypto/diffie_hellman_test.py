import pytest

# MATH MODULE TESTS
from diffie_hellman import inverse_mod
from diffie_hellman import point_add
from diffie_hellman import point_mult
from diffie_hellman import is_on_curve

a = 2
b = 3
prime = 97
G_point = (3, 6)
G2_point = (80, 10)   # 2 * G
G3_point = (80, 87)   # 3 * G
G4_point = (3, 91)    # 4 * G

def test_inverse_mod():
    assert inverse_mod(2, 3) == 2
    assert inverse_mod(3, 7) == 5
    assert inverse_mod(7, 3) == 1

def test_point_add():
    assert point_add(None, (3, 6), 2, 97) == (3, 6)
    assert point_add(None, None, 2, 97) is None
    assert point_add((1, 2), (1, -2), 2, 97) is None
    assert point_add(G_point, G_point, a, prime) == G2_point
    assert point_add(G_point, G2_point, a, prime) == G3_point
    assert point_add(G_point, G4_point, a, prime) is None
    assert point_add(G_point, G4_point, a, prime) is None

def test_point_mult():
    assert point_mult(0, G_point, a, prime) is None
    assert point_mult(5, None, a, prime) is None
    assert point_mult(2, G_point, a, prime) == G2_point
    assert point_mult(3, G_point, a, prime) == G3_point
    assert point_mult(4, G_point, a, prime) == G4_point


#  GENERAL DIFFIE-HELLMAN MODULE TEST


from diffie_hellman import generate_diffie_hellman_params
from diffie_hellman import generate_public_key
from diffie_hellman import generate_shared_key


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


#  GENERAL ELLIPTIC CURVE DIFFIE-HELLMAN MODULE TEST
from diffie_hellman import generate_curve_parameters
from diffie_hellman import generate_keypair
from diffie_hellman import generate_shared_secret


def test_ecdh_key_exchange():
    P_MOD, A, B, G_X, G_Y, N_ORDER = generate_curve_parameters()

    is_g_valid = is_on_curve((G_X, G_Y), A, B, P_MOD)
    is_zero = point_mult(N_ORDER, (G_X, G_Y), A, P_MOD) is None

    if is_g_valid and is_zero:
        sender_private, sender_public = generate_keypair(G_X, G_Y, N_ORDER, A, P_MOD)
        recipient_private, recipient_public = generate_keypair(G_X, G_Y, N_ORDER, A, P_MOD)


        sender_shared_secret = generate_shared_secret(sender_private, recipient_public, A, B, P_MOD)
        recipient_shared_secret = generate_shared_secret(recipient_private, sender_public, A, B, P_MOD)

        assert sender_shared_secret == recipient_shared_secret

    