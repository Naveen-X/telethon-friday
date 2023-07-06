#    Copyright (C) @chsaiujwal 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests

from fridaybot import CMD_HELP
from fridaybot.utils import admin_cmd
from fridaybot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


@friday.on(friday_on_cmd(pattern="pokedex ?(.*)"))
@friday.on(sudo_cmd(pattern="pokedex ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = f"https://starkapi.herokuapp.com/pokedex/{input_str}"
    r = requests.get(url).json()
    pokemon = r
    if pokemon.get("error") is not None:
          kk = f"""
Error:   {pokemon.get("error")}"""
          ommhg = await edit_or_reply(event, kk)
          return
    name = str(pokemon.get("name"))
    number = str(pokemon.get("number"))
    species = str(pokemon.get("species"))
    typo = pokemon.get("types")
    types = "".join(f"{str(tu)},  " for tu in typo)
    lol = pokemon.get("abilities")
    lmao = lol.get("normal")
    ok = ""
    for ty in lmao:
        ok = f"{str(ty)},  "

    kk = lol.get("hidden")
    hm = "".join(f"{str(pq)},  " for pq in kk)
    hell = pokemon.get("eggGroups")
    uio = "".join(f"{str(x)},  " for x in hell)
    height = pokemon.get("height")
    weight = pokemon.get("weight")
    yes = pokemon.get("family")
    Id = str(yes.get("id"))
    evo = str(yes.get("evolutionStage"))
    pol = yes.get("evolutionLine")
    xy = "".join(f"{str(p)},  " for p in pol)
    start = pokemon.get("starter")
    if start == False:
        start = "No"
    elif start == True:
        start = "True"
    leg = pokemon.get("legendary")

    if leg == False:
        leg = "No"
    elif leg == True:
        leg = "True"
    myt = pokemon.get("mythical")
    if myt == False:
        myt = "No"
    elif myt == True:
        myt = "True"
    ultra = pokemon.get("ultraBeast")

    if ultra == False:
        ultra = "No"
    elif ultra == True:
        ultra = "True"
    megA = pokemon.get("mega")

    if megA == False:
        megA = "No"
    elif megA == True:
        megA = "True"
    gEn = pokemon.get("gen")
    link = pokemon.get("sprite")
    des = pokemon.get("description")

    # hope = await borg(event.chat_id, link)
    caption = f"<b><u>Pokemon Information Gathered Successfully</b></u>\n\n\n<b>Name:-   {name}\nNumber:-  {number}\nSpecies:- {species}\nType:- {types}\n\n<u>Abilities</u>\nNormal Abilities:- {ok}\nHidden Abilities:- {hm}\nEgg Group:-  {uio}\nHeight:- {height}\nWeight:- {weight}\n\n<u>Family</u>\nID:- {Id}\nEvolution Stage:- {evo}\nEvolution Line:- {xy}\nStarter:- {start}\nLegendary:- {leg}\nMythical:- {myt}\nUltra Beast:- {ultra}\nMega:- {megA}\nGen:-  {gEn}\nDescription:-  {des}</b>"

    await borg.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
        file=link,
        force_document=False,
        silent=True,
    )
    await event.delete()


CMD_HELP.update(
    {
        "pokedex": "**Pokedex**\
\n\n**Syntax : **`.pokedex <pokemon name>`\
\n**Usage :** Gives Information About Given Pokemon.\
\n\n**Example : **`.pokedex pikachu`\
\nThis above syntax gives Information about Pikachu"
    }
)
