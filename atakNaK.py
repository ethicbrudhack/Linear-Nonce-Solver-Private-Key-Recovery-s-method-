from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import generator_secp256k1

# Dane z transakcji
r1 = int("ab9467e44699c0ab5ee2da6389e1646725a03bd66433eb99e531e45d76476ee0", 16)
r2 = int("a674f3ced3e25621cde299d20a700ccab080eb8352db313c5e039473ae48df83", 16)
s1 = int("59098b9fe30776049508f91eea10e4a9972eec2c1afe79674379578447b7aa46", 16)
s2 = int("57d8156cb1f7d1b390a13bc008bb3f2478d5552d00cc75215f21bbef866bec55", 16)
z1 = int("726c33406e9d8ac5824b9ab64a252c27146c26907b23eb082ac72b324c2e1167", 16)
z2 = int("c7c58a952ca7b31ced67bfea57fd7571314f8d77a88c90f42e68bdd82c2adb4f", 16)

# Moduł porządkowy krzywej secp256k1
n = generator_secp256k1.order()

# Różnice
delta_s = (s1 - s2) % n
delta_z = (z1 - z2) % n

# Obliczanie k – tylko jeśli delta_s ≠ 0
if delta_s != 0:
    k = (delta_z * inverse_mod(delta_s, n)) % n
    print(f"✅ Wykryto liniową zależność k! k = {hex(k)}")

    # Teraz obliczamy prywatny klucz d na podstawie wzoru:
    # s = (z + r*d)/k  =>  d = (s*k - z) / r
    d = ((s1 * k - z1) * inverse_mod(r1, n)) % n
    print(f"🔑 Odzyskany klucz prywatny: d = {hex(d)}")
else:
    print("❌ Brak zależności liniowej w k – delta_s = 0")
