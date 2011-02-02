__author__    = 'Grzegorz Biesiadecki'
__email__     = 'gbiesiadecki@gmail.com'
__program__   = 'pyFuel'
__version__   = '0.9.4'
__date__      = 'Date: 30/03/2010'
__copyright__ = 'Copyright (c) 2006 Grzegorz Biesiadecki'
__license__   = 'Python s60 GPL' 


class Refueling:
    """Refueling - data structure.
    Set km != 0 only if full refueling"""
   
    def __init__(self, date, price, volume, km):
        self.date = date
        self.price = price
        self.volume = volume
        self.km = km

       
    def __cmp__(self, other):
        #print '%f - %f = ' % (self.date, other.date),
        if self.date > other.date:
            #print 1
            return 1
        if self.date < other.date: 
            #print -1
            return -1
        #print 0
        return 0
        
            
class Refuelings(list):
    """Refuelings list"""
     
    def save(self, path):
        """Saves list to file"""

        data = open(path, 'w')
        self.sort(reverse=True)
        for refuel in self:
            fu = '%s|%.2f|%.2f|%.2f\n' % (refuel.date, refuel.price, refuel.volume, refuel.km)
            data.write(fu)
        data.close()
    
    
    def load(path):
        """Loads list from file"""
        
        rflist = Refuelings()
        try:
            data = open(path)
        except IOError:
            return rflist
             
        for rf in data:
            date, price, vol, km = rf.rstrip('\n').split('|')
            rfobj = Refueling(float(date), float(price), float(vol), float(km))
            rflist.append(rfobj)
        data.close()
        return rflist
    load = staticmethod(load)


    def avg_kmcost(self, issum=False):
        """Gets average distance cost.
        If issum is True, the average is calculated from all full refuelings,
        otherwise only last full refueling is taken into account""" 

        if len(self) == 0:
            return 0

        full = False
        fullcost = float(0)
        fullkm = float(0)
        
        self.sort(reverse=True)       
        for rf in self:
            # exclude all not fulls from top
            if rf.km == 0 and not full:
                continue

            # is full?
            if rf.km != 0:
                # if not first full and calculate only from one full refueling
                if full and not issum:
                    break
                full = True

            #print '%f + %f = %f\n' % (rf.volume, rf.price, rf.volume*rf.price) 
            fullcost += rf.volume * rf.price
            fullkm += rf.km

        return fullkm and fullcost / fullkm or fullkm
        

    def avg_kmcons(self, issum=False):
        """Gets average fuel consumption per km.
        If issum is True, the average is calculated from all full refuelings,
        otherwise only last full refueling is taken into account""" 

        if len(self) == 0:
            return 0

        full = False
        vol = float(0)
        km = float(0)

        self.sort(reverse=True)
        for rf in self:
            # exclude all not fulls from top
            if rf.km == 0 and not full:
                continue

            # is full?
            if rf.km != 0:
                # if not first full and calculate only from one full refueling stop calc
                if full and not issum:
                    break
                full = True

            #print '%f, %f' % (rf.volume, rf.km)
            vol += rf.volume
            km += rf.km
        
        return km and vol / km or km

        
    def avg_fuelprice(self):
        """Gets average fuel price"""
        if len(self) == 0:
            return 0

        sum = 0
        for rf in self:
            sum += rf.price
        return sum / len(self)
