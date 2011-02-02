__author__    = 'Grzegorz Biesiadecki'
__email__     = 'gbiesiadecki@gmail.com'
__program__   = 'pyFuel'
__version__   = '0.9.4'
__date__      = 'Date: 30/03/2010'
__copyright__ = 'Copyright (c) 2006 Grzegorz Biesiadecki'
__license__   = 'Python s60 GPL'


from copy import deepcopy
from refuel import *

class Refuelings_test:

    _refuels = []

    def __init__(self):
        self._refuels = Refuelings()
        # date, price, volume, dist
        r = Refueling(5, 5, 50, 100)
        self._refuels.append(r)
        r = Refueling(3, 3, 30, 0)
        self._refuels.append(r)
        r = Refueling(7, 7, 70, 0)
        self._refuels.append(r)
        r = Refueling(6, 6, 60, 100)
        self._refuels.append(r)
        r = Refueling(9, 9, 90, 0)
        self._refuels.append(r)
        r = Refueling(8, 8, 80, 100)
        self._refuels.append(r)


    def sort_test(self):
        self._refuels.sort(reverse=True)
        assert self._refuels[0].date == 9, self._refuels[0].date
        assert self._refuels[1].date == 8, self._refuels[1].date
        assert self._refuels[2].date == 7, self._refuels[2].date
        assert self._refuels[3].date == 6, self._refuels[3].date
        assert self._refuels[4].date == 5, self._refuels[4].date
        assert self._refuels[5].date == 3, self._refuels[5].date


    def avg_kmcost_test(self):
        r = Refueling(1, 1, 10, 0)
        zero_refuels = Refuelings()
        zero_refuels.append(r)
        assert zero_refuels.avg_kmcost() == 0, zero_refuels.avg_kmcost()
        
        assert self._refuels.avg_kmcost() == 11.3, self._refuels.avg_kmcost()
        assert self._refuels.avg_kmcost(issum=True) == 6.1, self._refuels.avg_kmcost(issum=True)


    def avg_kmcons_test(self):
        r = Refueling(1, 1, 10, 0)
        zero_refuels = Refuelings()
        zero_refuels.append(r)
        assert zero_refuels.avg_kmcons() == 0, zero_refuels.avg_kmcost()
        
        assert self._refuels.avg_kmcons() == 1.5, self._refuels.avg_kmcons()
        assert '%0.2f' % self._refuels.avg_kmcons(issum=True) == '0.97', '%0.2f' % self._refuels.avg_kmcons(issum=True)
