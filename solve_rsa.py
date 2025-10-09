#!/usr/bin/env python3
"""
Riddler: Null Set - RSA Attack using Common Factors

The three "bombs" share common factors, which means we can factor them
and potentially decrypt the flag using RSA mathematics.
"""

from math import gcd

# The three "bombs" (likely RSA moduli that share factors)
hospital = 17228885174970084276161970522097412605266394159971647740752267300221714788550197385293497867284890619874129427467673441688167088281496263523126626874873040420690149997429144654882986643604004320995801451651978549126665724326037323443693785147308295273804941176324595270160848031743691643352199091770561183390101638892864365971529361775777473322338259828117124021731569968581096105773133290818616623517239075045010723533051858606599891085860123293236498867687161911760308272069433482552999066140765265852927860548903142423166019118304640362315363826033542802010314992302177183041218307694787831493560402247717975058777
subway = 18599394198408159559032127206556973904470958589652384401139516143215782574096306554190666147629219501568720150220610776907290318953673688570966652188653414334135944107812388490123363711694776438197910528441090458287491320232545060818540405255660036329115175285563075067615115662971223964466609690121087345003072037826745412886843594744373925001833637904010490107159214131436719753440343088809862147325818389229992483097674780613975438662993160352072711897374040436210067117793225426902614028702255450993606803712362745736227617347976687372229897332444483782057154829741076097868855041890160420732593056490770604016963
financial = 21465018203265794097113095991538507070009934123584712754183836984749947784914875073029917205704709806063598091539183323502642805321030095506965670322592578944062438932372074147246983365306801187413681411691600283518148755726465920648688770335822658763606803297069673119665208343264880669287960265441639527802610566656299685318339460983357111370900461103556978263689008699830462732473301850828945035801211567525902267631084241059888222620103913512778392054697511670625304307246238730039519706049298726456456715325025195145205840264871637036819903723164701441937741275296892662198340153409014099281713703913671372908819
flag_encrypted = 2688799573415612194172688341985385655869767021669706325971969222982091539107082257386772222987306933827264001995669863266148641628566567467721627695226828529063310337313730890984773336370189319810197054705752635402192590291140330841505400796372134659065052651929114899378965182328524235056804062656407286061152078766613035623406173201907601732254045680536238007225975731741967059981506881028597601704173481437206652323544395617004541689706710800898777397919180336353911831098500922631432068656317452009839798641849451740369839351859125801709185337650226880544125158905221302154116578507914015625510759196575232097337

print("=== Riddler: Null Set - RSA Attack ===\n")

# Step 1: Find the common factors using GCD
print("Step 1: Finding common factors using GCD")
gcd_hs = gcd(hospital, subway)
gcd_hf = gcd(hospital, financial)
gcd_sf = gcd(subway, financial)

print(f"gcd(Hospital, Subway) = {gcd_hs}")
print(f"gcd(Hospital, Financial) = {gcd_hf}")
print(f"gcd(Subway, Financial) = {gcd_sf}")
print()

# Step 2: Factor each modulus
# For hospital: we have two GCDs with other numbers, we can find all factors
print("Step 2: Factoring the moduli")

# Hospital shares a factor with subway (gcd_hs) and with financial (gcd_hf)
# Let's find the other factors
p_h1 = gcd_hs
p_h2 = gcd_hf
# Hospital = p_h1 * p_h2 * something_else OR Hospital might just be p_h1 * something

# Try to find the third factor of hospital
hospital_partial = hospital // gcd(gcd_hs, gcd_hf)  # Remove common part
print(f"Hospital partial factorization...")

# Actually, let's be more systematic
# If H = p * q * r and S = p * r * s and F = q * r * t
# Then gcd(H,S) = p * r, gcd(H,F) = q * r, gcd(S,F) = r * s or similar

# Let's find r (the common factor of all three)
r = gcd(gcd_hs, gcd_hf)
print(f"Common factor r (gcd of all gcds) = {r}")

# Now find p and q
p = gcd_hs // r  # Factor shared by H and S only
q = gcd_hf // r  # Factor shared by H and F only  
s = gcd_sf // r  # Factor shared by S and F only

print(f"p (H,S factor) = {p}")
print(f"q (H,F factor) = {q}")
print(f"s (S,F factor) = {s}")
print()

# Now we can factor each modulus
# Hospital should be p * q * r (or some combination)
print("Step 3: Verifying factorization")
print(f"p * q * r = {p * q * r}")
print(f"Hospital = {hospital}")
print(f"Match: {p * q * r == hospital}")
print()

print(f"p * r * s = {p * r * s}")
print(f"Subway = {subway}")
print(f"Match: {p * r * s == subway}")
print()

print(f"q * r * s = {q * r * s}")
print(f"Financial = {financial}")
print(f"Match: {q * r * s == financial}")
print()

# Step 4: Now we need to figure out how to decrypt the flag
# The flag might be encrypted with RSA using one of these moduli
# Or it might be encrypted with a key derived from p, q, r, s

# Common RSA attack: if we know the factorization, we can compute phi(n) and find d
# Let's try each modulus

def mod_inverse(e, phi):
    """Extended Euclidean Algorithm to find modular inverse"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    gcd_val, x, _ = extended_gcd(e % phi, phi)
    if gcd_val != 1:
        return None
    return (x % phi + phi) % phi

# Standard RSA: c = m^e mod n, m = c^d mod n where d*e ≡ 1 (mod phi(n))
# phi(n) = (p-1)(q-1)(r-1) for n = p*q*r

print("Step 4: Attempting RSA decryption")

# Since r=1, we have:
# Hospital = p * q
# Subway = p * s
# Financial = q * s

# Try with hospital's phi
phi_h = (p - 1) * (q - 1)
print(f"phi(Hospital) = (p-1)*(q-1)")

# Common RSA public exponents
for e in [3, 5, 17, 65537]:
    try:
        d = mod_inverse(e, phi_h)
        if d:
            print(f"Trying Hospital with e={e}...")
            plaintext = pow(flag_encrypted, d, hospital)
            
            # Convert to hex and try to decode
            pt_hex = hex(plaintext)[2:]
            if len(pt_hex) % 2:
                pt_hex = '0' + pt_hex
            
            try:
                pt_bytes = bytes.fromhex(pt_hex)
                pt_str = pt_bytes.decode('ascii')
                if all(32 <= ord(c) < 127 for c in pt_str):
                    print(f"SUCCESS!")
                    print(f"Plaintext: {pt_str}")
                    print(f"Flag: ctf{{{pt_str}}}kernel")
                    print()
                    exit(0)
                elif sum(1 for c in pt_str if 32 <= ord(c) < 127) > len(pt_str) * 0.8:
                    print(f"Partially readable: {pt_str}")
            except:
                pass
    except Exception as ex:
        print(f"Error with e={e}: {ex}")

# Try with subway's phi
phi_s = (p - 1) * (s - 1)
print(f"\nphi(Subway) = (p-1)*(s-1)")

for e in [3, 5, 17, 65537]:
    try:
        d = mod_inverse(e, phi_s)
        if d:
            print(f"Trying Subway with e={e}...")
            plaintext = pow(flag_encrypted, d, subway)
            
            # Convert to hex and try to decode
            pt_hex = hex(plaintext)[2:]
            if len(pt_hex) % 2:
                pt_hex = '0' + pt_hex
            
            try:
                pt_bytes = bytes.fromhex(pt_hex)
                pt_str = pt_bytes.decode('ascii')
                if all(32 <= ord(c) < 127 for c in pt_str):
                    print(f"SUCCESS!")
                    print(f"Plaintext: {pt_str}")
                    print(f"Flag: ctf{{{pt_str}}}kernel")
                    print()
                    exit(0)
                elif sum(1 for c in pt_str if 32 <= ord(c) < 127) > len(pt_str) * 0.8:
                    print(f"Partially readable: {pt_str}")
            except:
                pass
    except Exception as ex:
        print(f"Error with e={e}: {ex}")

# Try with financial's phi
phi_f = (q - 1) * (s - 1)
print(f"\nphi(Financial) = (q-1)*(s-1)")

for e in [3, 5, 17, 65537]:
    try:
        d = mod_inverse(e, phi_f)
        if d:
            print(f"Trying Financial with e={e}...")
            plaintext = pow(flag_encrypted, d, financial)
            
            # Convert to hex and try to decode
            pt_hex = hex(plaintext)[2:]
            if len(pt_hex) % 2:
                pt_hex = '0' + pt_hex
            
            try:
                pt_bytes = bytes.fromhex(pt_hex)
                pt_str = pt_bytes.decode('ascii')
                if all(32 <= ord(c) < 127 for c in pt_str):
                    print(f"SUCCESS!")
                    print(f"Plaintext: {pt_str}")
                    print(f"Flag: ctf{{{pt_str}}}kernel")
                    print()
                    exit(0)
                elif sum(1 for c in pt_str if 32 <= ord(c) < 127) > len(pt_str) * 0.8:
                    print(f"Partially readable: {pt_str}")
            except:
                pass
    except Exception as ex:
        print(f"Error with e={e}: {ex}")

print("\nNo success with standard RSA decryption. Trying other approaches...")

# Maybe the flag uses a different modulus - let's try p*q*s
print("\nTrying combined moduli...")
n_pqs = p * q * s
phi_pqs = (p - 1) * (q - 1) * (s - 1)
print(f"Trying n = p*q*s")

for e in [3, 5, 17, 65537]:
    try:
        d = mod_inverse(e, phi_pqs)
        if d:
            print(f"Trying e={e}...")
            plaintext = pow(flag_encrypted, d, n_pqs)
            
            # Convert to hex and try to decode
            pt_hex = hex(plaintext)[2:]
            if len(pt_hex) % 2:
                pt_hex = '0' + pt_hex
            
            try:
                pt_bytes = bytes.fromhex(pt_hex)
                pt_str = pt_bytes.decode('ascii')
                if all(32 <= ord(c) < 127 for c in pt_str):
                    print(f"SUCCESS!")
                    print(f"Plaintext: {pt_str}")
                    print(f"Flag: ctf{{{pt_str}}}kernel")
                    print()
                    exit(0)
            except:
                pass
    except Exception as ex:
        pass
