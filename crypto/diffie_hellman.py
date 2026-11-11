# Diffie-Hellman Key-agreement (Key-exchange)
import hashlib
import random
import secrets
# Библиотека pycryptodome-4.3.0 (Crypto)
from Crypto.Util.number import getPrime, isPrime


# 'CLASSIC DIFFIE-HELLMAN' MODULE

# RFC 3526: More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE)
RFC_groups = ['1536-bit MODP Group', '2048-bit MODP Group', '3072-bit MODP Group', '4096-bit MODP Group', '6144-bit MODP Group']
RFC_3526_primes = {
    '1536-bit MODP Group': '''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF''',
    '2048-bit MODP Group': '''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AACAA68 FFFFFFFF FFFFFFFF''',
    '3072-bit MODP Group': '''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC E0FD108E 4B82D120 A93AD2CA FFFFFFFF FFFFFFFF''',
    '4096-bit MODP Group': '''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34063199 FFFFFFFF FFFFFFFF''',
    '6144-bit MODP Group': '''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492 36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD F8FF9406 AD9E530E E5DB382F 413001AE B06A53ED 9027D831 179727B0 865A8918 DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B DB7F1447 E6CC254B 33205151 2BD7AF42 6FB8F401 378CD2BF 5983CA01 C64B92EC F032EA15 D1721D03 F482D7CE 6E74FEF6 D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F BEC7E8F3 23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328 06A1D58B B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C DA56C9EC 2EF29632 387FE8D7 6E3C0468 043E8F66 3F4860EE 12BF2D5B 0B7474D6 E694F91E 6DCC4024 FFFFFFFF FFFFFFFF'''
}

# Creating the main public parameters for Diffie-Hellman algorithm (GENERATOR and PRIME)
def generate_diffie_hellman_params(RFC_flag: bool, bit_length=1024) -> tuple[int, int]:
    # Standardized strong generator
    generator = 2

    # RFC_flag determines using the RFC MODP groups
    if RFC_flag:
        RFC_3526_primes_index = secrets.randbelow(len(RFC_3526_primes))
        prime = RFC_3526_primes[RFC_groups[RFC_3526_primes_index]].replace(' ', '')
        return int(prime, 16), generator

    else:
        prime = getPrime(bit_length)
        if prime.bit_length() < 1024:
            raise ValueError('Введенное количество бит в кодировке простого числа недостаточно')
    return prime, generator


# Creating the public key that will be shared with another user
def generate_public_key(prime: int, generator: int) -> tuple[int, int]:
    own_exp = secrets.randbits(256)
    public_key = pow(generator, own_exp, prime)
    return own_exp, public_key


# Creating the private key that will become the key for AES cipher
def generate_shared_key(prime: int, own_exp: int, shared_public_key: int) -> int:
    shared_key = pow(shared_public_key, own_exp, prime)
    return shared_key


# 'ELLIPTIC CURVE DIFFIE-HELLMAN' MATH MODULE


def inverse_mod(inverse_coef, prime):
    if inverse_coef == 0:
        raise ZeroDivisionError('Обратное число не может равняться нулю.')
    if inverse_coef < 0:
        inverse_coef %= prime
    s, old_s = 0, 1
    rem, old_rem = prime, inverse_coef
    while rem != 0:
        quotient = old_rem // rem
        old_rem, rem = rem, old_rem - quotient * rem
        old_s, s = s, old_s - quotient * s
    return old_s % prime


def point_add(point_1, point_2, a, prime):
    if point_1 is None:
        return point_2
    if point_2 is None:
        return point_1
    x1, y1 = point_1
    x2, y2 = point_2
    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None
    if x1 == x2 and y1 == y2:
        slope = (3 * x1 * x1 + a) * inverse_mod(2 * y1, prime) % prime
    else:
        slope = (y2 - y1) * inverse_mod(x2 - x1, prime) % prime
    x3 = (slope * slope - x1 - x2) % prime
    y3 = (slope * (x1 - x3) - y1) % prime
    return x3, y3


def point_mult(mult, point, a, prime):
    if mult == 0 or point is None:
        return None
    result = None
    addend = point
    while mult > 0:
        if mult & 1:
            result = point_add(result, addend, a, prime)
        addend = point_add(addend, addend, a, prime)
        mult >>= 1
    return result


def is_on_curve(point, a, b, prime):
    if point is None:
        return False
    x, y = point
    return (y ** 2) % prime == (x ** 3 + a * x + b) % prime


# 'ECDH PROTOCOL' MODULE


def generate_curve_parameters(bits=12):
    prime = getPrime(bits)
    while True:
        a = secrets.randbelow(prime - 1)
        b = secrets.randbelow(prime - 1)
        # Non-singularity check: 4A^3 + 27B^2 != 0
        discriminant = (4 * pow(a, 3, prime) + 27 * pow(b, 2, prime)) % prime
        if discriminant != 0:
            break

    all_points = []
    y_squares = {pow(y, 2, prime): y for y in range(prime)}

    for x in range(prime):
        rhs = (pow(x, 3, prime) + a * x + b) % prime
        if rhs in y_squares:
            y = y_squares[rhs]
            all_points.append((x, y))

    # Total ordering of a group (including the point at infinity)
    total_group_order = len(all_points) * 2 + 1

    # Shuffle the points to select a random generator
    random.shuffle(all_points)

    while True:
        for candidate_G in all_points:
            G_order = None
            for potential_n in range(total_group_order, 1, -1):
                if total_group_order % potential_n == 0:
                    if isPrime(potential_n):
                        if point_mult(potential_n, candidate_G, a, prime) is None:
                            G_order = potential_n
                            break

            if G_order and isPrime(G_order) and G_order >= 100:
                G_X, G_Y = candidate_G
                N_ORDER = G_order
                return prime, a, b, G_X, G_Y, N_ORDER


def generate_keypair(g_x, g_y, n_order, a, prime):
    private_key = secrets.randbelow(n_order - 1) + 1  # Приватный ключ от 1 до N_ORDER - 1
    public_key = point_mult(private_key, (g_x, g_y), a, prime)
    return private_key, public_key


def generate_shared_secret(private_key, side_public_key, a, b, prime):
    if not is_on_curve(side_public_key, a, b, prime):
        raise ValueError("Критическая ошибка: Публичный ключ не лежит на кривой!")

    shared_point = point_mult(private_key, side_public_key, a, prime)

    if shared_point is None:
        raise ValueError("Критическая ошибка: Получена точка на бесконечности!")
    return shared_point


# 'DERIVE TO AES' SHA256 MODULE


def derive_aes_key(shared_key: int) -> bytes:
    length = (shared_key.bit_length() + 7) // 8
    key_bytes = shared_key.to_bytes(length, byteorder='big')
    aes_key = hashlib.sha256(key_bytes).digest()
    return aes_key


# DEMONSTRATION


if __name__ == "__main__":
    print("Шаг 1: Генерация параметров эллиптической кривой...")
    P_MOD, A, B, G_X, G_Y, N_ORDER = generate_curve_parameters()

    print("\n" + "=" * 50)
    print("ГЕНЕРАЦИЯ ЗАВЕРШЕНА! ВАЛИДНЫЕ ПАРАМЕТРЫ КРИВОЙ:")
    print("=" * 50)
    print(f"P_MOD   = {P_MOD} ({hex(P_MOD)})")
    print(f"A       = {A}")
    print(f"B       = {B}")
    print(f"G_X     = {G_X} ({hex(G_X)})")
    print(f"G_Y     = {G_Y} ({hex(G_Y)})")
    print(f"N_ORDER = {N_ORDER} ({hex(N_ORDER)})")
    print("=" * 50)

    # Базовые математические проверки
    print("\n[Проверка параметров кривой]")
    is_g_valid = is_on_curve((G_X, G_Y), A, B, P_MOD)
    print(f"Проверка 1 (Базовая точка G лежит на кривой): {is_g_valid}")

    is_zero = point_mult(N_ORDER, (G_X, G_Y), A, P_MOD) is None
    print(f"Проверка 2 (Порядок точки верный: N_ORDER * G == None): {is_zero}")

    # Симуляция обмена ключами ECDH
    print("\n[Симуляция протокола Диффи-Хеллмана (ECDH)]")

    # 1. Алиса генерирует свои ключи
    alice_private, alice_public = generate_keypair(G_X, G_Y, N_ORDER, A, P_MOD)
    print(f"\n Ключи Алисы:")
    print(f" -> Приватный (a): {alice_private}")
    print(f" -> Публичный  (A): {alice_public}")

    # 2. Боб генерирует свои ключи
    bob_private, bob_public = generate_keypair(G_X, G_Y, N_ORDER, A, P_MOD)
    print(f"\n Ключи Боба:")
    print(f" -> Приватный (b): {bob_private}")
    print(f" -> Публичный  (B): {bob_public}")

    # 3. Перекрестное вычисление Общего Секрета (Shared Secret)
    # Алиса берет публичный ключ Боба и свой приватный ключ
    alice_shared_secret = generate_shared_secret(alice_private, bob_public, A, B, P_MOD)

    # Боб берет публичный ключ Алисы и свой приватный ключ
    bob_shared_secret = generate_shared_secret(bob_private, alice_public, A, B, P_MOD)

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ ОБМЕНА СЕКРЕТАМИ:")
    print("=" * 50)
    print(f"Секрет, вычисленный Алисой (a * B): {alice_shared_secret}")
    print(f"Секрет, вычисленный Бобом  (b * A): {bob_shared_secret}")

    # Финальный вердикт
    success = alice_shared_secret == bob_shared_secret
    print(f"Совпадение секретов: {success}")
    print("=" * 50)

    if success:
        print("🎉 УСПЕХ! Протокол ECDH работает корректно. Общий секрет успешно установлен.")
    else:
        print("❌ ОШИБКА! Математические секреты не совпали.")

    aes_key = derive_aes_key(bob_shared_secret).decode('latin-1')

    print(aes_key, f"Длина ключа: {len(aes_key) * 8} бит")
