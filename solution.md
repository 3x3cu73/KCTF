# Riddler: Null Set - Solution

## Challenge Analysis

The challenge presents three "bombs" (large numbers called Hospital, Subway, and Financial) and one encrypted flag. The narrative suggests using common factors to decrypt the flag.

## Approach

### Step 1: Factor Analysis

Using GCD (Greatest Common Divisor), we can find that the three numbers share common factors:

- Hospital = p × q
- Subway = p × s  
- Financial = q × s

Where:
- p = gcd(Hospital, Subway) = 122183442526228731953182815023045032811760641141661308088520678955649064062357635272218472938229651021598797696131754354301040525107391560520108253036566924134837400335847090821724478470224866110330335262674294485751297641236816729570955497811910885631034043531847485919738535728854628486333189194994717750227

- q = gcd(Hospital, Financial) = 141008346292678847693211109971485931683376483617941118949092240999463197559734893690702307449031663443323766063716520540023109911559366978761374506789361004066114027060887311000811883546154901623686481506396894383350756664484173420109544252345580637032097215350762338479469120557560418878523470330452063743651

- s = gcd(Subway, Financial) = 152225160904395754090335168505270249561152851090575894380035344762096236492820738882140724210190267389734589225766717689548341276274191767075437304719182723577972859223543840725383977812419288667920039942288107694829272282812601945865530888647024455447250138187192300788503863748250526889352151363037252661969

### Step 2: RSA Common Factor Attack

This is a classic RSA vulnerability where multiple moduli share common prime factors. By finding these common factors through GCD operations, we can factor each modulus completely.

### Step 3: Decryption Attempts

We attempted several decryption methods:
1. Standard RSA decryption with individual moduli (Hospital, Subway, Financial)
2. RSA decryption with combined modulus n = p × q × s
3. XOR operations between ciphertexts and factors
4. Chinese Remainder Theorem (CRT) based approaches
5. Modular arithmetic with the flag encrypted number

## Solution

[TO BE DETERMINED - The exact decryption method is still being investigated]

## Flag Format

The flag should be wrapped as: `ctf{...}kernel`

## Tools Used

- Python 3
- math.gcd() for finding common factors
- Modular arithmetic operations
- RSA decryption algorithms

## References

- RSA Common Factor Attack
- GCD-based factorization
- Chinese Remainder Theorem
