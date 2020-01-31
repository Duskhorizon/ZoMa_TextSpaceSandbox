from __future__ import print_function
import objects
import os
import random
from  terminaltables import DoubleTable
from terminaltables.terminal_io import terminal_size
from colorclass import Color, Windows
from textwrap import wrap



class My_Table(DoubleTable):
    def __init__(self, table_data, title):
        super().__init__(table_data, title)
        self.inner_row_border =True
        for x in range(0,len(table_data[0])):
            self.justify_columns[x] = 'center'
        self.wrap_long_strings(table_data)

    def wrap_long_strings(self,table_data):
        while self.table_width > terminal_size()[0]:
            longest = 0
            for rowindex,row in enumerate(table_data):
                for columnindex,column in enumerate(row):
                    if len(column) > longest:
                        longest = len(column)
                        longestrow = rowindex
                        longestcollumn = columnindex
            max_width = self.column_max_width(longestcollumn)
            longstring = self.table_data[longestrow][longestcollumn]
            wrapped_string = '\n'.join(wrap(longstring, max_width))
            self.table_data[longestrow][longestcollumn] = wrapped_string                        

def status_table():
    
    title = Color('{yellow}[{}]{/yellow}').format(playership.name)

    TABLE_DATA = (
    ('HP ',Color('{green}{}/{}{/green}').format(playership.max_hp,playership.current_hp)),
    ('ARMOR ','{}'.format(playership.armor)),
    ('FUEL ',Color('{green}{}/{}{/green}').format(playership.max_fuel,str(playership.current_fuel)[:4])),
    ('CURRENT SYSTEM','{}'.format(playership.currentsystem.name)),
    ('CURRENT LOCATION','{}'.format(playership.location.name))
    )
    table_status = My_Table(TABLE_DATA, title)
    return table_status

def action_table():
    title = Color('{yellow}[{}]{/yellow}').format(playership.name)
    TABLE_DATA = (
    ['Action','Hotkey'],
    ['Examine current solar system','1'],
    ['Examine planets in current solar system','2'],
    ['Examine structures in current solar system','3'],
    ['Fly to structures in current solar system','4'],
    )
    TABLE_DATA += playership.location.add_actions()
    table_action = My_Table(TABLE_DATA,title)
    return table_action

def menu_examine_planet(planet):
    table_top = My_Table(planet.create_description(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,None,0,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
        menu_examine_planets()

def menu_examine_station(station):
    table_top = My_Table(station.create_description(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,None,0,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
        menu_examine_stations()

def menu_examine_system():
    table_top = My_Table(playership.currentsystem.create_description(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_mid = My_Table(playership.currentsystem.create_planetlist(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['Select planet number to inspect it, input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,table_mid,1,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
         menu_main()
    else:
        try:
            menu_examine_planet(playership.currentsystem.planetlist[int(action)-1])
        except ValueError:
            input('Incorrect Value, press any key to try again')
            menu_examine_system()
        except IndexError:
            input('Incorrect Value, press any key to try again')
            menu_examine_system()                     

def menu_examine_planets():
    table_top = status_table()
    table_mid = My_Table(playership.currentsystem.create_planetlist(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['Select planet number to inspect it, input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,table_mid,1,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
         menu_main()
    else:
        try:
            menu_examine_planet(playership.currentsystem.planetlist[int(action)-1])
        except ValueError:
            input('Incorrect Value, press any key to try again')
            menu_examine_planets()
        except IndexError:
            input('Incorrect Value, press any key to try again')
            menu_examine_planets()                 

def menu_examine_stations():
    table_top = status_table()
    table_mid = My_Table(playership.currentsystem.create_structurelist(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['Select station number to inspect it, input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,table_mid,1,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
         menu_main()
    else:
        try:
            menu_examine_station(playership.currentsystem.structurelist[int(action)-1])
        except ValueError:
            input('Incorrect Value, press any key to try again')
            menu_examine_stations()
        except IndexError:
            input('Incorrect Value, press any key to try again')
            menu_examine_stations()                

def menu_flyto_stations():
    table_top = status_table()
    table_mid = My_Table(playership.currentsystem.create_structurelist(),Color('{yellow}[{}]{/yellow}').format(playership.name))
    table_bot = My_Table([['Select station number to fly to it, input z to go back']],Color('{yellow}[{}]{/yellow}').format(playership.name))
    refresh(table_top,1,table_mid,1,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == 'z':
         menu_main()
    else:
        try:
            playership.fly(playership.currentsystem.structurelist[int(action)-1])
            table_mid = My_Table(playership.createflylog(playership.currentsystem.structurelist[int(action)-1]),'FLIGHT LOG OF {} SHIP'.format(playership.name))
            refresh(None,0,table_mid,1,None,0)
            input('press any key to confirm')
            menu_flyto_stations()
        except ValueError:
            input('Incorrect Value, press any key to try again')
            menu_flyto_stations()
        except IndexError:
            input('Incorrect Value, press any key to try again')
            menu_flyto_stations()

def menu_jump_to_system():
            table_mid = My_Table(playership.jump(),'FLIGHT LOG OF {} SHIP'.format(playership.name))
            refresh(None,0,table_mid,1,None,0)
            input('press any key to confirm')
            menu_main()

def menu_main():    
    table_top = status_table()
    table_bot = action_table()
    refresh(table_top,1,None,0,table_bot,1)
    action = input('Awaiting orders commander: ')
    if action == "1":
        menu_examine_system()
    if action == "2":
        menu_examine_planets()
    if action == "3":
        menu_examine_stations()
    if action == "4":
        menu_flyto_stations()
    else:
       globals()[playership.location.add_choices(action)]()
    

def refresh(tt,tta,mt,mta,bt,bta):

    os.system('cls' if os.name == 'nt' else 'clear')

    #top table
    if tta == 1:
        print(tt.table)
        print('\n' * 1)

    #mid table
    if mta == 1:
        print(mt.table)
        print('\n' * 1)

    #bottom table
    if bta == 1:
        print(bt.table)
        print('\n' * 1)

if __name__ == "__main__":
    my_universe = objects.Universe()
    os.system('cls' if os.name == 'nt' else 'clear')
    shipname = input('Hello, please tell me how you want to name your ship:')
    playership = objects.Spaceship(shipname,100,100,5,100,100,my_universe.solarsystem_list[0],my_universe.solarsystem_list[0].structurelist[0])
    first_run = 1
    mid_table_active =0
    os.system('cls' if os.name == 'nt' else 'clear')
    menu_main()
    print('Im done')  