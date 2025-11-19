import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_ostos_oikealla_nimella(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, ANY)

    def test_kaksi_eri_tuotetta_pankin_metodia_kutsutaan_oikealla_asiakkaalla_tilinumerolla_ja_summalla(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 20
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 2)
                
            
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 7)

    def test_kaksi_samaa_tuotetta_pankin_metodia_kutsutaan_oikealla_asiakkaalla_summalla_tilinumerolla(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 20
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 2)
                
            
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 10)

    def test_loppunut_tuote_ja_tuote_pankin_metodia_kutsutaan_oikealla_asiakkaalla_tilinumerolla_summalla(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0
            
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 2)
                
            
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)

