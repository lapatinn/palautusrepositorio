from tuomari import Tuomari

class KiviPaperiSakset:
    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto = self._ensimmaisen_siirto()
        tokan_siirto = self._toisen_siirto(ekan_siirto)

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = input("Ensimmäisen pelaajan siirto: ")
            tokan_siirto = self._toisen_siirto(ekan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self, ensimmaisen_siirto):
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
    
    @staticmethod
    def luo_peli(tyyppi):
        if tyyppi == 'a':
            from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
            return KPSPelaajaVsPelaaja()
        if tyyppi == 'b':
            from kps_tekoaly import KPSTekoaly
            return KPSTekoaly()
        if tyyppi == 'c':
            from kps_parempi_tekoaly import KPSParempiTekoaly
            return KPSParempiTekoaly()

        return None
