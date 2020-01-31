import json
import os
import random
import string
import roman
from colorclass import Color, Windows


dir_path = os.path.dirname(os.path.realpath(__file__))

class Universe:
    def __init__(self):
        self.generate_new_universe()

    def generate_new_universe(self):
        self.solarsystem_list=[]
        for _ in range(100):
            self.solarsystem_list.append(Solarsystem())
        self.connect_solar_systems()

    def connect_solar_systems(self):
        for solar_system in self.solarsystem_list:
            counter = 0
            while len(solar_system.connected_systems) < solar_system.connections:
                counter += 1
                if counter > 1000:
                    break
                connector = self.solarsystem_list[random.randint(0,99)]
                if solar_system != connector:
                    if connector not in solar_system.connected_systems:
                        if len(connector.connected_systems) < connector.connections:
                            solar_system.connected_systems.append(connector)
                            connector.connected_systems.append(solar_system)                            
        failed_systems = 0
        for solar_system in self.solarsystem_list:
            solar_system.build_stargates()
            if len(solar_system.connected_systems) < solar_system.connections:
                failed_systems += 1
        with open('test.txt', 'w+') as f:
            f.write(str(failed_systems))     


                       


class Solarsystem:
    def __init__(self):
        self.generate_new_system() 

    def create_description(self):
        TABLE_DATA = [
            ['SYSTEM NAME :','{}'.format(self.name)],
            ['STAR CLASS :','{}'.format(self.starclass)],
            ['MAIN STAR TEMPERATURE  :','{}'.format(self.temp)],
            ['SYSTEM PLANETS :','{}'.format(self.planetcount)],
            ['MAIN STAR DESCRIPTION :','{}'.format(self.descr)]
        ]
        return TABLE_DATA

    def create_planetlist(self):
        TABLE_DATA = [['Number','Name','Type','Moons','AU from star','Station']]
        for planetindex,planet in enumerate(self.planetlist):
            TABLE_DATA.append([planetindex +1,planet.name,Color(planet.planetclass),planet.mooncount,planet.distancefromstar,planet.havestation])
        return TABLE_DATA    

    def create_structurelist(self):
        TABLE_DATA = [['Number','Name','Type','Owner','AU from star']]
        for structureindex,structure in enumerate(self.structurelist):
            TABLE_DATA.append([structureindex +1,structure.name,structure.type,Color(structure.owner),structure.distancefromstar])
        return TABLE_DATA               
    
    def generate_new_system(self):
        self.name = self.generaterandomname()
        self.connections = random.randint(1,4)
        self.connected_systems = []   
        with open(dir_path +'/data/data.json') as json_file:
            data = json.load(json_file)
        randomseed = random.randint(1,100)
        for star in data['stars']:
            if randomseed <= int(star['rarity']):
                self.starclass = star['class']    
                self.temp = star['temp']
                self.descr = star['descr']
                self.structurelist = []
                self.planetcount = random.randint(4,10)
                self.population = int(star['population'])
                self.populatewithplanets(self.planetcount)
    
                break

    def build_stargates(self):
        for connected_system in self.connected_systems:
            self.structurelist.append(Stargate(self,connected_system))


    def generaterandomname(self):
        with open(dir_path +'/data/words.txt') as longtxt:
            words = longtxt.read().splitlines()
        lastnamepart = random.choice(words).upper()
        secondnamepart = str(random.randint(100,999))
        firstnamepart = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
        return firstnamepart + secondnamepart + '-' + lastnamepart

    def populatewithplanets(self,planetcount):
        self.planetlist = []
        distancefromstar = 0
        for x in range(planetcount):
            distancefromstar += random.uniform(0,3)
            distancefromstar = str(distancefromstar)[:4]
            distancefromstar = float(distancefromstar)
            self.planetlist.append(Planet(self,x,distancefromstar))



class Planet:
    def __init__(self,mothersystem,planetindex,distancefromstar):
       self.generatenewplanet(mothersystem,planetindex,distancefromstar)

    def create_description(self):
        TABLE_DATA = [
            ['PLANET NAME :','{}'.format(self.name)],
            ['PLANET TYPE :','{}'.format(Color(self.planetclass))],
            ['PLANET DESCRIPTION  :','{}'.format(self.descr)],
            ['NUMBER OF MOONS  :','{}'.format(self.mooncount)],
            ['HAVE STATION?  :','{}'.format(self.havestation)],
            ['DISTANCE FROM STAR :','{} AU'.format(self.distancefromstar)],
        ]
        return TABLE_DATA       

    def generatenewplanet(self,mothersystem,planetindex,distancefromstar):
        self.name = self.generaterandomname(mothersystem,planetindex)
        self.distancefromstar = distancefromstar 
        self.mothersystem = mothersystem
        self.havestation = False
        with open(dir_path +'/data/data.json') as json_file:
            data = json.load(json_file)
        randomseed = random.randint(1,100)
        self.randomseed = randomseed
        randomseed2 = random.randint(1,100)
        if randomseed2 <= mothersystem.population:
            self.havestation = True
            self.station = Station(self)        
        

        for planet in data['planets']:
            if randomseed <= int(planet['rarity']):
                self.planetclass = planet['type']    
                self.descr = planet['descr']
                self.mooncount = random.randint(0,9)
                self.populatewitmoons(self.mooncount)
                break

    def generaterandomname(self,mothersystem,planetindex):
        secondnamepart = roman.toRoman(planetindex+1)
        firstnamepart = mothersystem.name
        return firstnamepart + ' - Planet ' + secondnamepart

    def populatewitmoons(self,mooncount):
        self.moonlist = []
        for x in range(mooncount):
            self.moonlist.append(Moon(self,x))

class Moon:
    def __init__(self,motherplanet,moonindex):
       self.generatenewmoon(motherplanet,moonindex)

    def generatenewmoon(self,motherplanet,moonindex):
        self.name = motherplanet.name + ' - Moon ' + roman.toRoman(moonindex+1)        

class Structure:
    def __init__(self):
        self.type = None
        self.name = None
        self.owner = None
        self.descr = None
        self.distancefromstar = None 


    def create_description(self):
        TABLE_DATA = [
            ['STRUCTURE TYPE :','{}'.format(self.type)],
            ['STRUCTURE NAME :','{}'.format(self.name)],
            ['STATION OWNER :','{}'.format(Color(self.owner))],
            ['STATION DESCRIPTION  :','{}'.format(self.descr)],
            ['DISTANCE FROM STAR :','{} AU'.format(self.distancefromstar)],
            ['']
        ]
        return TABLE_DATA           



class Station(Structure):
    def __init__(self,motherplanet):
        self.motherplanet = motherplanet
        self.generate_new_station(motherplanet)
        self.type = "Station"

    def generate_new_station(self,motherplanet):
        with open(dir_path +'/data/data.json') as json_file:
            data = json.load(json_file)
        randomseed = random.randint(1,100)
        for station in data['stations']:
            if randomseed <= int(station['rarity']):
                self.name = '{} Station on '.format(Color(station['owner'])) + motherplanet.name
                self.owner = station['owner']
                self.descr = station['descr']
                self.distancefromstar = self.motherplanet.distancefromstar
                self.motherplanet.mothersystem.structurelist.append(self)
                break
    def add_actions(self):
        ADDITIONAL_DATA = (
        ['Dock to {}'.format(self.name),'5'],
        ['Quit game','6'],
        )
        return ADDITIONAL_DATA

    def add_choices(self,action):
        if action == "5":
            quit()
        if action == "6":
            quit()                    

class Stargate(Structure):
    def __init__(self,mothersystem,connectedsystem):
        self.type = "Stargate"
        self.mothersystem = mothersystem
        self.connectedsystem = connectedsystem
        self.generate_new_stargate(mothersystem,connectedsystem)

    def generate_new_stargate(self,mothersystem,connectedsystem):
        with open(dir_path +'/data/data.json') as json_file:
            data = json.load(json_file)
        randomseed = random.randint(1,100)
        for stargate in data['stargates']:
            if randomseed <= int(stargate['rarity']):
                self.name = '{} Stargate from {} system to {} system'.format(Color(stargate['owner']),mothersystem.name,connectedsystem.name)
                self.owner = stargate['owner']
                self.descr = stargate['descr']
                self.distancefromstar = 100
                break
    
    def add_actions(self):
        ADDITIONAL_DATA = (
        ['Jump to {}'.format(self.connectedsystem.name),'5'],
        ['Quit game','6'],
        )
        return ADDITIONAL_DATA

    def add_choices(self,action):
        if action == "5":
            return "menu_jump_to_system"
        if action == "6":
            quit()



            



class Spaceship:
    def __init__(self,name,max_hp,current_hp,armor,max_fuel,current_fuel,currentsystem,location):
        self.name = name
        self.current_hp = current_hp
        self.max_hp = max_hp
        self.armor = armor
        self.max_fuel = max_fuel
        self.current_fuel = current_fuel
        self.currentsystem = currentsystem
        self.location = location

    def fly(self,destination):
        distance = abs(self.location.distancefromstar - destination.distancefromstar)
        self.current_fuel -= distance
    def createflylog(self,destination):
        distance = abs(self.location.distancefromstar - destination.distancefromstar)
        TABLE_DATA = [
            ['LOCATION:','{}'.format(Color(self.location.name))],
            ['DESTINATION :','{}'.format(Color(destination.name))],
            ['DISTANCE TRAVELED :','{}'.format(distance)[:4]],
            ['FUEL LEFT :','{} AU'.format(self.current_fuel)[:4]],
        ]
        self.location = destination
        return TABLE_DATA
    
    def jump(self):
        TABLE_DATA = [
            ['FROM SYSTEM:','{}'.format(Color(self.location.mothersystem.name))],
            ['TO SYSTEM :','{}'.format(Color(self.location.connectedsystem.name))],
        ]

        for structure in self.location.connectedsystem.structurelist:
            if structure.type == "Stargate":
                if structure.connectedsystem == self.currentsystem:
                    self.location = structure

        self.currentsystem = self.location.mothersystem

        return TABLE_DATA
        


