# 🔍 Linear Nonce Solver & Private Key Recovery (Δs method)

This snippet checks whether two ECDSA signatures reveal a **linear relation** between their nonces and — if so — directly recovers the private key.  
It implements the classic algebraic attack: when two signatures share the same deterministic linear model such that

s1 = k⁻¹ (z1 + r1·d)
s2 = k⁻¹ (z2 + r2·d)


then (assuming `r1 == r2` or working from the difference of the `s` and `z` values) we can compute `k` from the differences and recover `d` algebraically.

---

## ✅ What this code does (step-by-step)

1. **Load signature values** (`r1, s1, z1`, `r2, s2, z2`) as integers (hex → int).  
2. **Compute modular differences** over the curve order `n`:


delta_s = (s1 - s2) mod n
delta_z = (z1 - z2) mod n

3. **If** `delta_s != 0` (invertible modulo `n`) compute:


k = delta_z * delta_s⁻¹ mod n

— interpreted as the nonce (or its difference) implied by the signatures.
4. **Recover private key** using:


d = (s1 * k - z1) * r1⁻¹ mod n

5. **Print** recovered `k` and `d`. If `delta_s == 0`, prints that no linear relation was found.

---

## ⚙️ Math rationale (concise)

From ECDSA:


s_i ≡ k⁻¹ (z_i + r_i·d) (mod n)
⇒ s_i * k ≡ z_i + r_i·d

Subtracting two equations (i = 1,2):


(s1 - s2) * k ≡ (z1 - z2) (mod n)
⇒ k ≡ (z1 - z2) * (s1 - s2)⁻¹ (mod n)

Substitute `k` back to solve for `d`:


d ≡ (s1 * k - z1) * r1⁻¹ (mod n)


All inverses are computed modulo the curve order `n` (here `secp256k1`).

---

## 🧪 When this works

- `delta_s` must be invertible (i.e., `(s1 - s2) % n != 0`).  
- The two signatures must be related by the same `k` (or follow a deterministic linear relation that reduces to the above).  
- The code assumes the curve order `n` equals `generator_secp256k1.order()`.

---

## ⚠️ Limitations & caveats

- This attack assumes a **strong algebraic relation** between the two signatures. It does **not** apply to arbitrary unrelated signatures.  
- If `r1 != r2` and nonces are unrelated, the derived `k` will be meaningless and `d` incorrect.  
- Always verify the recovered `d` by deriving the public key and checking addresses / signatures before trusting it.  
- Numeric operations must be done modulo `n` and use a cryptographically correct inverse (the code uses `inverse_mod`).

---

## 🧾 Example output (if successful)


✅ Wykryto liniową zależność k! k = 0x1a2b3c...
🔑 Odzyskany klucz prywatny: d = 0x4f5e6d...


---

## ⚖️ Ethical reminder

Use this only on data you own or have explicit authorization to analyze. Recovering private keys without permission is illegal and unethical. This snippet is for **research, auditing, and education** only.

© 2025 — Author: [ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
