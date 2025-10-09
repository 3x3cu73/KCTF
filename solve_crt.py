#!/usr/bin/env python3
"""
Riddler: Null Set - CRT Attack

Since all three moduli share factors, maybe the flag was encrypted
multiple times with a small exponent (like e=3) and we can use CRT.
"""

from math import gcd

# The three "bombs" 
hospital = 17228885174970084276161970522097412605266394159971647740752267300221714788550197385293497867284890619874129427467673441688167088281496263523126626874873040420690149997429144654882986643604004320995801451651978549126665724326037323443693785147308295273804941176324595270160848031743691643352199091770561183390101638892864365971529361775777473322338259828117124021731569968581096105773133290818616623517239075045010723533051858606599891085860123293236498867687161911760308272069433482552999066140765265852927860548903142423166019118304640362315363826033542802010314992302177183041218307694787831493560402247717975058777
subway = 18599394198408159559032127206556973904470958589652384401139516143215782574096306554190666147629219501568720150220610776907290318953673688570966652188653414334135944107812388490123363711694776438197910528441090458287491320232545060818540405255660036329115175285563075067615115662971223964466609690121087345003072037826745412886843594744373925001833637904010490107159214131436719753440343088809862147325818389229992483097674780613975438662993160352072711897374040436210067117793225426902614028702255450993606803712362745736227617347976687372229897332444483782057154829741076097868855041890160420732593056490770604016963
financial = 21465018203265794097113095991538507070009934123584712754183836984749947784914875073029917205704709806063598091539183323502642805321030095506965670322592578944062438932372074147246983365306801187413681411691600283518148755726465920648688770335822658763606803297069673119665208343264880669287960265441639527802610566656299685318339460983357111370900461103556978263689008699830462732473301850828945035801211567525902267631084241059888222620103913512778392054697511670625304307246238730039519706049298726456456715325025195145205840264871637036819903723164701441937741275296892662198340153409014099281713703913671372908819
flag_encrypted = 2688799573415612194172688341985385655869767021669706325971969222982091539107082257386772222987306933827264001995669863266148641628566567467721627695226828529063310337313730890984773336370189319810197054705752635402192590291140330841505400796372134659065052651929114899378965182328524235056804062656407286061152078766613035623406173201907601732254045680536238007225975731741967059981506881028597601704173481437206652323544395617004541689706710800898777397919180336353911831098500922631432068656317452009839798641849451740369839351859125801709185337650226880544125158905221302154116578507914015625510759196575232097337

print("=== Riddler: Null Set - Trying different interpretations ===\n")

# Get the factors
p = gcd(hospital, subway)
q = gcd(hospital, financial)
s = gcd(subway, financial)

print(f"Factors found:")
print(f"  p = {p}")
print(f"  q = {q}")
print(f"  s = {s}")
print()

# Wait, let me think about this differently
# Maybe the flag_encrypted isn't actually RSA-encrypted at all
# Maybe it's just XORed with a key that can be derived from the factors

# Let me try simpler operations
print("=== Trying simple mathematical relationships ===\n")

# What if the key is just the sum or product of factors modulo something?
key_candidates = [
    ("p mod flag", p % flag_encrypted),
    ("q mod flag", q % flag_encrypted),
    ("s mod flag", s % flag_encrypted),
    ("flag mod p", flag_encrypted % p),
    ("flag mod q", flag_encrypted % q),
    ("flag mod s", flag_encrypted % s),
]

for name, value in key_candidates:
    print(f"{name} = {value}")
    # Try to decode
    value_hex = hex(value)[2:]
    if len(value_hex) % 2:
        value_hex = '0' + value_hex
    try:
        value_bytes = bytes.fromhex(value_hex)
        value_str = value_bytes.decode('ascii', errors='ignore')
        if len(value_str) > 0 and sum(1 for c in value_str if 32 <= ord(c) < 127) > len(value_str) * 0.8:
            printable = ''.join(c if 32 <= ord(c) < 127 else '.' for c in value_str)
            print(f"  Decoded: {printable}")
    except:
        pass
    print()

# What if these numbers are actually already the flag in different encodings?
# Let's check if any of them directly decode to text
print("\n=== Checking if numbers directly encode text ===\n")

numbers_to_check = [
    ("Hospital", hospital),
    ("Subway", subway),
    ("Financial", financial),
    ("Flag", flag_encrypted),
    ("p", p),
    ("q", q),
    ("s", s),
]

for name, num in numbers_to_check:
    num_hex = hex(num)[2:]
    if len(num_hex) % 2:
        num_hex = '0' + num_hex
    try:
        num_bytes = bytes.fromhex(num_hex)
        num_str = num_bytes.decode('ascii', errors='ignore')
        if len(num_str) > 10 and sum(1 for c in num_str if 32 <= ord(c) < 127) > len(num_str) * 0.5:
            printable = ''.join(c if 32 <= ord(c) < 127 else '.' for c in num_str)
            print(f"{name} might contain text: {printable[:100]}")
    except:
        pass

# What about using CRT with the remainders?
print("\n=== Trying CRT-based approach ===\n")

# If flag = c^3 was computed mod each of H, S, F
# We can use CRT to recover c^3 mod (H*S*F) / (common factors)
# But the moduli aren't coprime, so standard CRT won't work

# However, we can use CRT on pairwise coprime parts
# Actually, since H=p*q, S=p*s, F=q*s
# We need to be careful about overlapping factors

# Let's try: recover M mod p, M mod q, M mod s separately
m_mod_p = flag_encrypted % p
m_mod_q = flag_encrypted % q
m_mod_s = flag_encrypted % s

print(f"flag mod p = {m_mod_p}")
print(f"flag mod q = {m_mod_q}")
print(f"flag mod s = {m_mod_s}")
print()

# Now try to use CRT to combine these
def chinese_remainder_theorem(remainders, moduli):
    """Solve system of congruences using CRT"""
    from functools import reduce
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    def mod_inverse(a, m):
        gcd_val, x, _ = extended_gcd(a % m, m)
        if gcd_val != 1:
            return None
        return (x % m + m) % m
    
    total = 0
    prod = reduce(lambda a, b: a * b, moduli)
    
    for r_i, n_i in zip(remainders, moduli):
        p_i = prod // n_i
        inv = mod_inverse(p_i, n_i)
        if inv is None:
            return None
        total += r_i * p_i * inv
    
    return total % prod

# Try CRT
result = chinese_remainder_theorem([m_mod_p, m_mod_q, m_mod_s], [p, q, s])
if result:
    print(f"CRT result = {result}")
    
    # Try to decode
    result_hex = hex(result)[2:]
    if len(result_hex) % 2:
        result_hex = '0' + result_hex
    try:
        result_bytes = bytes.fromhex(result_hex)
        result_str = result_bytes.decode('ascii')
        if all(32 <= ord(c) < 127 for c in result_str):
            print(f"✓ SUCCESS!")
            print(f"Plaintext: {result_str}")
            print(f"\nFinal Flag: ctf{{{result_str}}}kernel\n")
            exit(0)
    except:
        pass
else:
    print("CRT failed (moduli not coprime)")
