import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

  #  def test_kortille_ei_voi_ladata_negatiivista_summaa(self):
   #     kortti = Maksukortti(1000)
    #    kortti.lataa_rahaa(-100)
     #   self.assertEqual(str(kortti), "Kortilla on rahaa 10.00 euroa")

    def test_kortille_voi_ladata_rahaa(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.00 euroa")

    def test_saldo_vahenee_jos_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 9.00 euroa")

    def test_saldo_ei_vahene_jos_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_ota_rahaa_palauttaa_true_jos_rahaa_tarpeeksi(self):
        totuus = self.maksukortti.ota_rahaa(100)
        self.assertEqual(totuus, True)

    def test_ota_rahaa_palauttaa_false_jos_rahaa_ei_tarpeeksi(self):
        totuus = self.maksukortti.ota_rahaa(1100)
        self.assertEqual(totuus, False)