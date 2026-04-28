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
from pathlib import Path
from PIL import Image
import shutil
import sys
from tomlkit import document, table, aot, dumps
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
    cardtype: str
    connections: List[int] = field(default_factory=list)


@dataclass
class ParseResult:
    info: Dict[str, str]
    files: Dict[str, str]
    continents: Dict[str, List[str]]
    countries: Dict[int, Country]
    errors: List[str]


# -- Main parser

def parse_cards(parsed: ParseResult, content: str) -> ParseResult:
    log.info('Parsing card file')

    nb_wildcards = 0
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
                if parts[0] == 'wildcard':
                    nb_wildcards += 1

                else:
                    cid = int(parts[1])
                    parsed.countries[cid].cardtype = parts[0]

            # missions
            elif section == "missions":
                pass

            else:
                raise ValueError(f"unknown section {section}")

        except Exception as e:
            errors.append(f"Line {lineno}: {e} -> {raw}")

    parsed.info['nb_wildcards'] = nb_wildcards

    return parsed


def parse_map(content: str) -> ParseResult:
    log.info('Parsing map')
    section    = 'info'
    info       = { "name": "unknown" }
    countries  = {}
    continents = {}
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
                    cardtype="",
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

    return ParseResult(info, files, continents, countries, errors)


# -- Graph validation

def validate(result: ParseResult) -> List[str]:
    errors = []

    for c in result.countries.values():
        # check if missing card types
        if c.cardtype == "":
            log.warning(f"country {c.id} has no card type")

        # check asymetric connections
        for conn in c.connections:
            if c.id not in result.countries[conn].connections:
                log.warning(f"Asymetrical connection: country {c.id} -> {conn}")


    return errors


# -- Export TOML

def to_toml(result: ParseResult) -> dict:
    doc = document()

    # info
    t_info = table()
    for k, v in result.info.items():
        t_info[k] = result.info[k]
    doc["info"] = t_info

    # files
#    t_files = table()
#    for k, v in result.files.items():
#        t_files[k] = v
#    doc["files"] = t_files

    # continents
    continents_aot = aot()
    for c in sorted(result.continents.values(), key=lambda x: x.id):
        t = table()
        t["id"] = c.id
        t["name"] = c.name
        t["bonus"] = c.bonus
        t["color"] = c.color
        continents_aot.append(t)

    doc["continents"] = continents_aot

    # countries
    countries_aot = aot()
    for c in sorted(result.countries.values(), key=lambda x: x.id):
        t = table()

        t["id"] = c.id
        t["name"] = c.name
        t["continent"] = c.continent
        t["x"] = c.x
        t["y"] = c.y
        t["cardtype"] = c.cardtype
        t["connections"] = c.connections

        countries_aot.append(t)

    doc["countries"] = countries_aot

    return doc


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

    outfile = dstdir / "map.toml"
    log.info(f"Writing to {outfile.as_posix()}")
    toml_data = to_toml(parsed)

    with outfile.open("w", encoding="utf-8") as f:
        f.write(dumps(toml_data))

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
