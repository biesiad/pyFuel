__author__    = 'Grzegorz Biesiadecki'
__email__     = 'gbiesiadecki@gmail.com'
__program__   = 'pyFuel'
__version__   = '0.9.4'
__date__      = 'Date: 30/03/2010'
__copyright__ = 'Copyright (c) 2006 Grzegorz Biesiadecki'
__license__   = 'Python s60 GPL'


import sys
import os
from time import *
import e32
import appuifw

localpath = str(os.path.split(appuifw.app.full_name())[0])
sys.path = [localpath] + sys.path

from refuel import Refuelings, Refueling

class Application:
    """pyFuel application user interface"""
    _refuels = Refuelings().load('data.dat')
    _mainmenu_current = 0
    
    def run(self):
        appuifw.app.screen = 'normal'
        appuifw.app.title = u"pyFuel"
        self.mainmenu_reset();
        
        self.lock = e32.Ao_lock()
        self.lock.wait()


    def mainmenu_reset(self):
        appuifw.app.body = appuifw.Listbox([u'Refuelings', u'Trip',  u'Statistics'], self.mainmenu_obs)
        appuifw.app.body.set_list([u'Refuelings', u'Trip',  u'Statistics'], self._mainmenu_current)
        appuifw.app.menu = []
        appuifw.app.exit_key_handler = self.exit
     

    def mainmenu_obs(self):
        # Refuelings
        if appuifw.app.body.current() == 0:
            self._mainmenu_current = 0
            self.mainmenu_refuels()
            appuifw.app.exit_key_handler = self.mainmenu_reset

        # Trip
        elif appuifw.app.body.current() == 1:
            self._mainmenu_current = 1
            self.mainmenu_trip()
            appuifw.app.exit_key_handler = self.exit
            
        # Statistics
        elif appuifw.app.body.current() == 2:
            self._mainmenu_current = 2
            self.mainmenu_stat()
            appuifw.app.exit_key_handler = self.mainmenu_reset


    def mainmenu_refuels(self):
        appuifw.app.menu = [(u'Add refueling', self.add_refuel)]
        appuifw.app.menu.append((u'Remove refueling', self.del_refuel))
        
        rflist = self._getlistbox()
            
        if len(rflist) == 0:
            appuifw.note(u'No refuelings', 'info')
            self.add_refuel()
            rflist = self._getlistbox()
            if len(rflist) == 0:
                self.mainmenu_reset()
                return

        appuifw.app.body = appuifw.Listbox(rflist, self.mainmenu_reset)


    def _getlistbox(self):
        rflist = []
        for rf in self._refuels:
            date = strftime('%Y-%m-%d', localtime(rf.date))
            isfull = ''
            if rf.km != 0:
                isfull = ', %.2fkm (full)' % rf.km
            rflist.append((unicode('%s' %date), unicode('price: %.2f, %.2fl%s' %(rf.price, rf.volume, isfull))))
        return rflist
        

    def mainmenu_trip(self):
        appuifw.app.menu = []
        if len(self._refuels) == 0:
            appuifw.note(u'No refuelings', 'error')
            return

        km = appuifw.query(u'Trip length', 'number', 0)
        count = appuifw.query(u'Person count', 'number', 0)
        avg_kmcost = float(self._refuels.avg_kmcost())

        if km == None or count == 0 or km == 0 or count == 0 or avg_kmcost == 0:
            appuifw.note(u'Cannot calculate cost', 'error')
        else:            
            cost = '%.2f' % (avg_kmcost * km / count)
            appuifw.note(u'Cost per person: %s' % unicode(cost), 'conf')


    def mainmenu_stat(self):
        appuifw.app.menu = []
        if len(self._refuels) == 0:
            appuifw.note(u'No refuelings', 'error')
            return

        avg_cons = self._refuels.avg_kmcons()
        avg_kmcost = self._refuels.avg_kmcost()
        text =  'Last\n'
        text += '  Average cons: %.2f l/100km\n' % (avg_cons * 100)
        text += '  Cost:         %.2f $/km\n' % avg_kmcost
        text += '\n'
   
        avg_cons = self._refuels.avg_kmcons(True)
        avg_kmcost = self._refuels.avg_kmcost(True)
        avg_lcost = self._refuels.avg_fuelprice()
        text += 'All\n'
        text += '  Average cons: %.2f l/100km\n' % (avg_cons * 100)
        text += '  Fuel price:   %.2f $\n' % avg_lcost 
        text += '  Cost:         %.2f $/km\n' % avg_kmcost
        appuifw.app.body = appuifw.Text(unicode(text))
        appuifw.app.menu = []


    def add_refuel(self):
        fields = [(u'Date','date', time()), \
                (u'Fuel price', 'float', 0.0), \
                (u'Fuel volume', 'float', 0.0), \
                (u'Km count', 'float', 0.0)]

        flags = appuifw.FFormEditModeOnly
        f = appuifw.Form(fields, flags)
        f.save_hook = self.save_refuel           
        f.execute()
        
    
    def del_refuel(self):
        index = appuifw.app.body.current()
        del self._refuels[index]        
        self._refuels.save('data.dat')
        self.mainmenu_refuels()   

        
    def save_refuel(self, arg):
        date = arg[0][2]
        price = arg[1][2]
        volume = arg[2][2]
        km = arg[3][2]
        
        if km != 0:
            appuifw.note(u'Full refueling saved. Don\'t forget to reset odometer.', 'info')
        else:
            appuifw.note(u'Refueling saved.', 'info')

        rf = Refueling(float(date), float(price), float(volume), float(km))
        self._refuels.append(rf) 
        self._refuels.save('data.dat') 
        self.mainmenu_refuels()

    
    def exit(self):
        self.lock.signal()


if __name__ == '__main__':
    Application().run()
