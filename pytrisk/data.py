# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from pytrisk.locale  import _
from .logger import log

import csv
from pathlib import Path
import weakref
import yaml

maps_dir = Path(Path(__file__).parent, 'maps')

class Continent():
    def __init__(self, mapref:weakref, numid:int, name:str, bonus:int,
            color:str):
        self.mapref = mapref
        self.numid  = numid
        self.name   = name
        self.bonus  = bonus
        self.color  = color
        self.longid = f'{self.mapref().name}-{self.name}'

class Country():
    def __init__(self, mapref:weakref, numid:int, name:str,
            continentref:weakref, coordx:int, coordy:int):
        self.mapref       = mapref
        self.numid        = numid
        self.name         = name
        self.continentref = continentref
        self.coordx       = coordx
        self.coordy       = coordy
        self.longname     = f'{self.mapref().name}-{self.continentref().name}-{self.name}'
        self.connections  = set()

    def add_connection(self, countryref:weakref):
        self.connections.add(countryref)

class Map():
    def __init__(self, name):
        self.name   = name
        self.path   = Path(maps_dir, name)
        self._continents = set()
        self._countries  = set()
        #log.info(f'loading map {name}')
        self._load()
        self.background = next(self.path.glob('background.*'), None)
        self.background = self.background.as_posix()


    # -- finders

    def get_continent_by_numid(self, numid):
        return next(filter(lambda continent: continent.numid==numid,
            self._continents), None)

    def get_country_by_numid(self, numid):
        return next(filter(lambda country: country.numid==numid,
            self._countries), None)

    # -- map loading

    def _load(self):
        self._load_infos()
        self._load_continents()
        self._load_countries()
        self._load_connections()

    def _load_connections(self):
        log.info('- loading country connections')
        with open(Path(self.path, 'connections.csv'), newline='') as csvstream:
            csvreader = csv.reader(csvstream)
            next(csvreader, None)  # skip the headers
            for row in csvreader:
                cnumid1, cnumid2 = row
                country1 = self.get_country_by_numid(int(cnumid1))
                country2 = self.get_country_by_numid(int(cnumid2))
                country1.add_connection(weakref.ref(country2))
                country2.add_connection(weakref.ref(country1))
                log.debug(f'new connection: {country1.name} - {country2.name}')
        log.info('- loaded country connections')

    def _load_continents(self):
        log.info('- loading continents')
        with open(Path(self.path, 'continents.csv'), newline='') as csvstream:
            csvreader = csv.reader(csvstream)
            next(csvreader, None)  # skip the headers
            for row in csvreader:
                cnumid, cname, cbonus, ccolor = row
                cname = eval(cname)     # eval to localize
                newcont = Continent(weakref.ref(self), int(cnumid),
                        cname, int(cbonus), ccolor)
                self._continents.add(newcont)
        log.info(f'- loaded {len(self._continents)} continents')

    def _load_countries(self):
        log.info('- loading countries')
        with open(Path(self.path, 'countries.csv'), newline='') as csvstream:
            csvreader = csv.reader(csvstream)
            next(csvreader, None)  # skip the headers
            for row in csvreader:
                cnumid, cname, ccontinentnum, coordx, coordy = row
                cname = eval(cname)     # eval to localize
                ccontinent = self.get_continent_by_numid(int(ccontinentnum))
                newcountry = Country(weakref.ref(self), int(cnumid),
                        cname, weakref.ref(ccontinent), int(coordx),
                        int(coordy))
                self._countries.add(newcountry)
        log.info(f'- loaded {len(self._countries)} countries')

    def _load_infos(self):
        log.info('- loading general information')
        yfile = Path(self.path, 'info.yaml')
        with yfile.open() as ystream:
            try:
                info = yaml.safe_load(ystream)
            except yaml.YAMLError as e:
                log.error('error loading {yfile.as_posix()}: {e}')
        self.title = eval(info['title'])    # eval to localize
        self.author = info['author']
        log.info(f'- infos loaded: "{self.title}" by {self.author}')


def all_maps():
    subdirs = [d for d in maps_dir.glob('*')]
    log.info(f'found {len(subdirs)} map subdirs in {maps_dir.as_posix()}')
    maps = []
    for subdir in subdirs:
        mapname = subdir.name
        newmap  = Map(mapname)
        maps.append(newmap)
    return maps
