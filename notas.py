import hashlib
TOTAL = 0
CONTADOR_NOTAS = 0

while CONTADOR_NOTAS <= 10:
    nota = float(input("Entre com a nota: "))
    TOTAL += nota
    CONTADOR_NOTAS += 1

media_disciplina = TOTAL / 10
print(f"A média da disciplina é: {media_disciplina}")

# Calculating md5sum of the script
script_path = "notas.py"
hash_md5 = hashlib.md5()
with open(script_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)

print(f"MD5sum of the script '{script_path}': {hash_md5.hexdigest()}")