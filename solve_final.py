#!/usr/bin/env python3
"""
Riddler: Null Set - Final Solution

The challenge describes using the common factors (fractures) to decrypt the flag.
Let's use the factors p, q, s as keys for XOR decryption.
"""

from math import gcd

# The three "bombs" 
hospital = 17228885174970084276161970522097412605266394159971647740752267300221714788550197385293497867284890619874129427467673441688167088281496263523126626874873040420690149997429144654882986643604004320995801451651978549126665724326037323443693785147308295273804941176324595270160848031743691643352199091770561183390101638892864365971529361775777473322338259828117124021731569968581096105773133290818616623517239075045010723533051858606599891085860123293236498867687161911760308272069433482552999066140765265852927860548903142423166019118304640362315363826033542802010314992302177183041218307694787831493560402247717975058777
subway = 18599394198408159559032127206556973904470958589652384401139516143215782574096306554190666147629219501568720150220610776907290318953673688570966652188653414334135944107812388490123363711694776438197910528441090458287491320232545060818540405255660036329115175285563075067615115662971223964466609690121087345003072037826745412886843594744373925001833637904010490107159214131436719753440343088809862147325818389229992483097674780613975438662993160352072711897374040436210067117793225426902614028702255450993606803712362745736227617347976687372229897332444483782057154829741076097868855041890160420732593056490770604016963
financial = 21465018203265794097113095991538507070009934123584712754183836984749947784914875073029917205704709806063598091539183323502642805321030095506965670322592578944062438932372074147246983365306801187413681411691600283518148755726465920648688770335822658763606803297069673119665208343264880669287960265441639527802610566656299685318339460983357111370900461103556978263689008699830462732473301850828945035801211567525902267631084241059888222620103913512778392054697511670625304307246238730039519706049298726456456715325025195145205840264871637036819903723164701441937741275296892662198340153409014099281713703913671372908819
flag_encrypted = 2688799573415612194172688341985385655869767021669706325971969222982091539107082257386772222987306933827264001995669863266148641628566567467721627695226828529063310337313730890984773336370189319810197054705752635402192590291140330841505400796372134659065052651929114899378965182328524235056804062656407286061152078766613035623406173201907601732254045680536238007225975731741967059981506881028597601704173481437206652323544395617004541689706710800898777397919180336353911831098500922631432068656317452009839798641849451740369839351859125801709185337650226880544125158905221302154116578507914015625510759196575232097337

print("=== Riddler: Null Set - Solution ===\n")

# Find the common factors
p = gcd(hospital, subway)  # 122183...
q = gcd(hospital, financial)  # 141008...
s = gcd(subway, financial)  # 152225...

print("The three factors (fractures):")
print(f"p (Hospital ∩ Subway):  {p}")
print(f"q (Hospital ∩ Financial): {q}")
print(f"s (Subway ∩ Financial):   {s}")
print()

# Try various combinations of the factors as XOR keys
print("Attempting to decrypt the flag using the factors...\n")

keys_to_try = [
    ("p", p),
    ("q", q),
    ("s", s),
    ("p ⊕ q", p ^ q),
    ("p ⊕ s", p ^ s),
    ("q ⊕ s", q ^ s),
    ("p ⊕ q ⊕ s", p ^ q ^ s),
    ("p * q mod 2^2048", (p * q) % (2**2048)),
    ("p + q + s", p + q + s),
]

for name, key in keys_to_try:
    print(f"Trying key: {name}")
    try:
        result = flag_encrypted ^ key
        
        # Convert to hex and decode
        result_hex = hex(result)[2:]
        if len(result_hex) % 2:
            result_hex = '0' + result_hex
        
        result_bytes = bytes.fromhex(result_hex)
        result_str = result_bytes.decode('ascii')
        
        # Check if it's all printable ASCII
        if all(32 <= ord(c) < 127 for c in result_str):
            print(f"✓ SUCCESS!")
            print(f"Plaintext: {result_str}")
            print(f"\nFinal Flag: ctf{{{result_str}}}kernel\n")
            exit(0)
        elif sum(1 for c in result_str if 32 <= ord(c) < 127) > len(result_str) * 0.7:
            printable = ''.join(c if 32 <= ord(c) < 127 else '.' for c in result_str)
            print(f"  Partially readable ({sum(1 for c in result_str if 32 <= ord(c) < 127) * 100 // len(result_str)}%): {printable[:80]}")
    except Exception as e:
        print(f"  Error: {e}")
    print()

# Maybe we need to think about this differently
# The "whisper" might be decrypted by removing the noise from the factors
# Let's try: flag_decrypted = flag XOR (H XOR S) XOR (H XOR F) etc.

print("\n=== Alternative: Using XOR combinations of ciphertexts ===\n")

xor_hs = hospital ^ subway
xor_hf = hospital ^ financial
xor_sf = subway ^ financial

combos = [
    ("H ⊕ S", xor_hs),
    ("H ⊕ F", xor_hf),
    ("S ⊕ F", xor_sf),
    ("(H⊕S) ⊕ (H⊕F)", xor_hs ^ xor_hf),
    ("(H⊕S) ⊕ (S⊕F)", xor_hs ^ xor_sf),
    ("(H⊕F) ⊕ (S⊕F)", xor_hf ^ xor_sf),
]

for name, key in combos:
    print(f"Trying key: {name}")
    try:
        result = flag_encrypted ^ key
        
        # Convert to hex and decode
        result_hex = hex(result)[2:]
        if len(result_hex) % 2:
            result_hex = '0' + result_hex
        
        result_bytes = bytes.fromhex(result_hex)
        result_str = result_bytes.decode('ascii')
        
        # Check if it's all printable ASCII
        if all(32 <= ord(c) < 127 for c in result_str):
            print(f"✓ SUCCESS!")
            print(f"Plaintext: {result_str}")
            print(f"\nFinal Flag: ctf{{{result_str}}}kernel\n")
            exit(0)
    except:
        pass
    print()

print("No solution found with these approaches.")
