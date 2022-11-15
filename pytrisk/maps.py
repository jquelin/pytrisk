#
# This file is part of pytrisk.
#
# pytrisk is free software: you can redistribute it and/or modify it
# under the # terms of the GNU General Public License as published by
# the Free Software # Foundation, either version 3 of the License, or
# (at your option) any later # version.
#
# pytrisk is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytrisk. If not, see <https://www.gnu.org/licenses/>.
#

from pytrisk.locale  import _
from pytrisk.logging import log

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
        log.debug(f'new continent: {numid} - "{name}" bonus={bonus} color={color}')

    def __del__(self):
        log.debug(f'~{self.longid}')

class Country():
    def __init__(self, mapref:weakref, idgrey:int, name:str,
            continentref:weakref, coordx:int, coordy:int):
        self.mapref       = mapref
        self.idgrey       = idgrey
        self.name         = name
        self.continentref = continentref
        self.coordx       = coordx
        self.coordy       = coordy
        self.longname     = f'{self.mapref().name}-{self.continentref().name}-{self.name}'
        log.debug(f'new country: {idgrey} - {continentref().name} - {name} @{coordx},{coordy}')

    def __del__(self):
        log.debug(f'~{self.longname}')


class Map():
    def __init__(self, name):
        self.name   = name
        self.path   = Path(maps_dir, name)
        self._continents = set()
        self._countries  = set()
        log.info(f'loading map {name}')
        self._load()

    def __del__(self):
        log.debug(f'~{self.name}')


    # -- finders

    def get_continent_by_numid(self, numid):
        return next(filter(lambda continent: continent.numid==numid,
            self._continents), None)

    # -- map loading

    def _load(self):
        self._load_infos()
        self._load_continents()
        self._load_countries()
        self._load_connections()

    def _load_connections(self):
        log.info('- loading country connections')
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
                cidgrey, cname, ccontinentnum, coordx, coordy = row
                cname = eval(cname)     # eval to localize
                ccontinent = self.get_continent_by_numid(int(ccontinentnum))
                newcountry = Country(weakref.ref(self), int(cidgrey),
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
    maps = {}
    for subdir in subdirs:
        mapname      = subdir.name
        maps[mapname] = Map(mapname)
    return maps
