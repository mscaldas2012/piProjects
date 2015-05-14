__author__ = 'marcelo'
import unittest
import time

from Gyro.gyro_l3g4200D import L3G4200D


class TestGyro(unittest.TestCase):
    gyro = None

    #    def setUp(self):
    #        self.tc = temp.TemperatureConverter()

    def test_gyroRead(self):
        gyro = L3G4200D(105)
        while (1):
            gyro.getAxes()
            time.sleep(500)


# def test_CelciusToFarenheight(self):
#        self.assertEqual(self.tc.convertTemp(32, "c"), 0, "Cjheck your calculations")

#    @unittest.expectedFailure
#    def test_fail(self):
#        self.assertEqual(1, 0, "Broken")
