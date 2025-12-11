from kps import KiviPaperiSakset

def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()
        if vastaus in ["a", "b", "c"]:
            print(
                "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
            )

            peli = KiviPaperiSakset()
            peli = peli.luo_peli(vastaus)
            peli.pelaa()
        else:
            break

if __name__ == "__main__":
    main()
