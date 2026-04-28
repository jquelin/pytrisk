#!/usr/bin/env python
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

import argparse
from dataclasses import dataclass, field
import json
from pathlib import Path
from PIL import Image
import shutil
import sys
from typing import Dict, List, Tuple

# Add pytrisk to sys.path
curdir = Path(__file__).parent
sys.path.append(str(curdir.parent.parent))

from pytrisk.logger import log


# -- Internal model

@dataclass
class Continent:
    id: int
    name: str
    bonus: int
    color: str

@dataclass
class Country:
    id: int
    name: str
    continent: int
    x: int
    y: int
    connections: List[int] = field(default_factory=list)

@dataclass
class Card:
    type: str
    id: int

@dataclass
class Mission:
    target: int
    nbcountries: int
    nbarmies: int
    continent_1: str
    continent_2: str
    continent_3: str
    description: str

@dataclass
class ParseResult:
    info: Dict[str, str]
    files: Dict[str, str]
    continents: Dict[str, List[str]]
    countries: Dict[int, Country]
    cards: List[Card]
    missions: List[Mission]
    errors: List[str]


# -- Main parser

def parse_cards(parsed: ParseResult, content: str) -> ParseResult:
    log.info('Parsing card file')

    lines = content.splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()

        if not line or line.startswith(";"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue

        parts = line.split()
        try:
            # cards
            if section == 'cards':
                if parts[0] not in ['Cannon', 'Infantry', 'Cavalry', 'wildcard']:
                    raise ValueError(f"info: unknown key {parts[0]}")

                else:
                    cid = int(parts[1]) if len(parts) > 1 else None
                    card = Card(type=parts[0].lower(), id=cid)
                    parsed.cards.append(card)

            # missions
            elif section == "missions":
                mission = Mission(
                    target=int(parts[0]),
                    nbcountries=int(parts[1]),
                    nbarmies=int(parts[2]),
                    continent_1=int(parts[3]) if parts[3] != '*' else '"*"',
                    continent_2=int(parts[4]) if parts[4] != '*' else '"*"',
                    continent_3=int(parts[5]) if parts[5] != '*' else '"*"',
                    description=' '.join(parts[6:]),
                )
                parsed.missions.append(mission)

            else:
                raise ValueError(f"unknown section {section}")

        except Exception as e:
            log.error(f"Line {lineno}: {e} -> {raw}")

    return parsed


def parse_map(content: str) -> ParseResult:
    log.info('Parsing map')
    section    = 'info'
    info       = { "name": "unknown" }
    countries  = {}
    continents = {}
    cards      = []
    missions   = []
    files      = {}
    errors     = []
    continent_id = 1

    lines = content.splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()

        if not line or line.startswith(";"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip().lower()
            continue

        parts = line.split()

        try:
            # header
            if section == 'info':
                if parts[0] != "name":
                    raise ValueError(f"info: unknown key {parts[0]}")
                name = ' '.join(parts[1:]) if len(parts) > 1 else parts[1]
                info["name"] = name

            # files
            elif section == "files":
                if len(parts) != 2:
                    raise ValueError("files: expected 2 columns")
                files[parts[0]] = parts[1]

            # continents
            elif section == "continents":
                if len(parts) < 3:
                    raise ValueError("continents: not enough fields")
                name = parts[0]
                bonus = int(parts[1])
                color = parts[2]
                log.debug(f"continents: {continent_id} {name} {bonus} {color}")
                continents[continent_id] = Continent(
                    id=continent_id,
                    name=name,
                    bonus=bonus,
                    color=color
                )
                continent_id += 1

            # countries
            elif section == "countries":
                if len(parts) < 5:
                    raise ValueError("countries: not enough fields")

                cid = int(parts[0])
                name = parts[1]
                continent = int(parts[2])
                x = int(parts[3])
                y = int(parts[4])

                if continent not in continents:
                    log.error(f"countries: unknown continent {continent}")
                    raise ValueError(f"countries: unknown continent {continent}")

                if cid in countries:
                    raise ValueError(f"duplicate country id {cid}")

                countries[cid] = Country(
                    id=cid,
                    name=name,
                    continent=continent,
                    x=x,
                    y=y,
                    connections=[]
                )

            # borders
            elif section == "borders":
                cid = int(parts[0])

                if len(parts) < 2:
                    connections = []
                else:
                    connections = list(map(int, parts[1:]))

                # check if country exists
                if cid not in countries:
                    log.error(f"borders: country {cid} does not exist")
                    raise ValueError(f"borders: country {cid} does not exist")

                for conn in connections:
                    if conn == cid:
                        log.warning(f"borders: country {cid} has self-connection")
                        continue

                    if conn not in countries:
                        log.error(f"borders: country {conn} does not exist")
                        raise ValueError(f"borders: country {cid} does not exist")

                    # add connection without duplicate
                    if conn not in countries[cid].connections:
                        countries[cid].connections.append(conn)

            else:
                raise ValueError(f"unknown section {section}")

        except Exception as e:
            errors.append(f"Line {lineno}: {e} -> {raw}")

    return ParseResult(info, files, continents, countries, cards, missions, errors)


# -- Graph validation

def validate(result: ParseResult) -> List[str]:
    errors = []

    for c in result.countries.values():
        # check asymetric connections
        for conn in c.connections:
            if c.id not in result.countries[conn].connections:
                log.warning(f"Asymetrical connection: country {c.id} -> {conn}")


    return errors


# -- Export

def to_json(result: ParseResult) -> dict:
    # manual dump instead of json.dumps to allow pretty printing as we want.
    out = []
    out.append( '{')
    out.append(f'  "name": "{result.info["name"]}",')
    out.append( '  "category": "unknown",')

    out.append( '  "continents": [')
    continents = []
    for c in result.continents.values():
        continents.append(f'    {{ "id": {c.id}, "name": "{c.name}", "color": "{c.color}", "bonus": {c.bonus} }}')
    out.append( ',\n'.join(continents))
    out.append( '  ],')

    out.append( '  "countries": [')
    countries = []
    for c in result.countries.values():
        countries.append(f'    {{ "id": {c.id}, '
                         f'"x": {c.x}, "y": {c.y}, '
                         f'"continent": {c.continent}, '
                         f'"name": {json.dumps(c.name)}, '
                         f'"connections": {c.connections} }}')
    out.append( ',\n'.join(countries))
    out.append( '  ],')

    out.append( '  "cards": [')
    cards = []
    for c in result.cards:
        if c.id is None:
            cards.append(f'    {{ "type": "{c.type}" }} ')
        else:
            cards.append(f'    {{ "type": "{c.type}", "id": {c.id} }} ')
    out.append( ',\n'.join(cards))
    out.append( '  ],')

    out.append( '  "missions": [')
    missions = []
    for m in result.missions:
        curmission  = f'    {{ "target": {m.target}, '
        curmission += f'"countries": [{m.nbcountries}, {m.nbarmies}], '
        curmission += f'"continents": [{json.dumps(m.continent_1)}, {json.dumps(m.continent_2)}, {json.dumps(m.continent_3)}], '
        curmission += f'"description": {json.dumps(m.description)} }} '
        missions.append(curmission)
    out.append( ',\n'.join(missions))
    out.append( '  ]')

    out.append( '}')
    return '\n'.join(out)

def convert(mapfile: Path, force: bool = False):
    mapname = mapfile.stem
    srcdir = mapfile.parent
    dstdir = curdir / mapname
    log.info(f"Converting {mapname}")
    log.debug(f"source: {mapfile}")
    log.debug(f"dst: {dstdir}")

    # first check if mapdir is a directory
    if dstdir.is_dir():
        if not force:
            log.error(f"{dstdir} exists and --force is not set")
            return

        # force is in effect, delete the directory
        log.info(f"Deleting {dstdir.as_posix()}")
        shutil.rmtree(dstdir.as_posix())
        dstdir.mkdir()

    # check if mapdir contains a file with a .map extension
    if not mapfile.is_file():
        log.error(f"{mapfile} does not exist, skipping")
        return

    # parse the map file
    raw = mapfile.read_bytes()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            content = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    parsed = parse_map(content)
    parse_errors = parsed.errors

    # Parse cards if needed
    if "crd" in parsed.files:
        cardfile = srcdir / parsed.files["crd"]
        raw = cardfile.read_bytes()
        for enc in ("utf-8", "cp1252", "latin-1"):
            try:
                content = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        parsed = parse_cards(parsed, content)

    # validate the result
    validation_errors = validate(parsed)
    all_errors = parse_errors + validation_errors

    if all_errors:
        print("Errors found:")
        for e in all_errors:
            print(" -", e)


    # write the result
    dstdir.mkdir(exist_ok=True)

    outfile = dstdir / "map.json"
    log.info(f"Writing to {outfile.as_posix()}")
    data = to_json(parsed)

    with outfile.open("w", encoding="utf-8") as f:
        f.write(data)
    # try to load it, if it fails, it's not valid json
    try:
        json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid json: {e}")


    # copy files

    src = srcdir / parsed.files["pic"]
    dst = dstdir / "background.png"
    log.info(f"Copying/converting {src.as_posix()} to {dst.as_posix()}")
    img = Image.open(src.as_posix())
    img.save(dst.as_posix(), "PNG")

    shutil.copy(src.as_posix(), dst.as_posix())
    src = srcdir / parsed.files["map"]
    dst = dstdir / "overlay.png"
    log.info(f"Copying/converting {src.as_posix()} to {dst.as_posix()}")
    img = Image.open(src.as_posix())
    img.save(dst.as_posix(), "PNG")


def run():
    # Parse arguments
    parser = argparse.ArgumentParser(
        prog        = 'convert',
        description = 'Domination map converter',
    )
    parser.add_argument('-v', '--verbose', action='count', default=0,
                            help='Increase verbosity level')
    parser.add_argument('-q', '--quiet', action='count', default=0,
                            help='Decrease verbosity level')
    parser.add_argument('-f', '--force', default=False, action='store_true',
                        help='Force overwrite of existing files')
    parser.add_argument('-i', '--input', required=True, action='store',
                            help='Input directory')
    parser.add_argument('mapname', help='Name of the map to convert', nargs='*')
    args = parser.parse_args()

    # Adjust logging level based on verbosity flags
    for _ in range(args.quiet):
        log.decrease_verbosity()
    for _ in range(args.verbose):
        log.increase_verbosity()

    # Check which files to convert
    inputdir = Path(args.input)
    if args.mapname:
        mapfiles = [inputdir / f"{m}.map" for m in args.mapname]
    else:
        mapfiles = sorted(inputdir.glob('*.map'))

    # Do the conversion
    for mapfile in mapfiles:
        convert(mapfile, args.force)


if __name__ == "__main__":
    run()
