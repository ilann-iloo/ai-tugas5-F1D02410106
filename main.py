import json


# Membaca file basis pengetahuan
def baca_pengetahuan():
    with open("knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Mengumpulkan fakta berdasarkan jawaban pengguna
def kumpulkan_fakta(pengetahuan):
    fakta = set()

    print("\n======================================")
    print(" SISTEM PAKAR IDENTIFIKASI HAMA PADI")
    print("======================================")
    print("Jawab pertanyaan dengan y (ya) atau t (tidak).\n")

    for key, pertanyaan in pengetahuan["pertanyaan"].items():

        while True:
            jawaban = input(pertanyaan + " (y/t): ").lower().strip()

            if jawaban == "y":
                fakta.add(key)
                break

            elif jawaban == "t":
                break

            else:
                print("Jawaban tidak valid. Masukkan y atau t.")

    return fakta


# Mesin inferensi Forward Chaining
def forward_chaining(aturan, fakta):
    memori = set(fakta)
    riwayat = []
    nomor = 1

    while True:
        aturan_ditemukan = False

        for rule in aturan:

            hasil = rule["maka"]

            # Jika hasil sudah ada, aturan dilewati
            if hasil in memori:
                continue

            kondisi = rule["jika"]
            mode = rule["mode"]

            # Memeriksa kondisi aturan
            if mode == "dan":
                cocok = all(item in memori for item in kondisi)

            elif mode == "atau":
                cocok = any(item in memori for item in kondisi)

            else:
                cocok = False

            # Jika aturan terpenuhi
            if cocok:
                memori.add(hasil)

                riwayat.append({
                    "nomor": nomor,
                    "id": rule["id"],
                    "kondisi": kondisi,
                    "hasil": hasil,
                    "sumber": rule["sumber"]
                })

                print(
                    f"Langkah {nomor}: "
                    f"{rule['id']} -> {hasil}"
                )

                nomor += 1
                aturan_ditemukan = True

        # Berhenti jika tidak ada aturan baru
        if not aturan_ditemukan:
            break

    return memori, riwayat


# Menampilkan hasil identifikasi
def tampilkan_hasil(pengetahuan, fakta, memori, riwayat):

    print("\n======================================")
    print("             HASIL IDENTIFIKASI")
    print("======================================")

    print("\nFakta awal:")
    for item in sorted(fakta):
        print("-", item)

    # Mengambil kesimpulan yang ditemukan
    hasil = [
        item for item in pengetahuan["kesimpulan"]
        if item in memori
    ]

    if hasil:
        print("\nKesimpulan:")

        for item in hasil:
            print("-", item)

        print("\nAlasan:")
        for rule in riwayat:
            print(
                f"{rule['hasil']} <- {rule['id']} "
                f"({', '.join(rule['kondisi'])})"
            )
            print("Sumber:", rule["sumber"])

    else:
        print("\nKesimpulan:")
        print("Tidak ditemukan kesimpulan berdasarkan aturan.")

    print("\nBatas Keberlakuan:")
    print(pengetahuan["batas"])

    print("\n======================================")


# Program utama
def main():

    pengetahuan = baca_pengetahuan()

    fakta = kumpulkan_fakta(pengetahuan)

    print("\n=== PROSES FORWARD CHAINING ===")

    memori, riwayat = forward_chaining(
        pengetahuan["aturan"],
        fakta
    )

    tampilkan_hasil(
        pengetahuan,
        fakta,
        memori,
        riwayat
    )


if __name__ == "__main__":
    main()
