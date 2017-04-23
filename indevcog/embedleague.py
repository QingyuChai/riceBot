import discord
import aiohttp
import json
import aiohttp
import operator
import collections

try:
    from cassiopeia import riotapi
    isAvailable = True
except Exception as e:
    print(e)
    isAvailable = False

riotapi_key = 'RGAPI-63809742-ba2e-419e-b767-191d8be5ddca'
championgg_key = 'fd746fed9a1447ba5f337c892327c6aa'

riotapi.set_api_key(riotapi_key) #keycheck
#command to set key


from __main__ import send_cmd_help
from discord.ext import commands


class League:
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xCC9835
        riotapi.set_region("eune")

    @commands.group(pass_context = True)
    async def opgg(self, ctx):
        """Shows a summoners account on OPGG"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @commands.command(pass_context = True)
    async def currentgame(self, ctx, region, *, summoner):
        try:
            riotapi.set_region(region)
        except ValueError as e:
            print(e)
            await self.bot.say("Invalid region! Try again.")
            return
        except Exception as e:
            print(e)
            await self.bot.say("Check your console for logs.")
            return
        try:
            summoner = riotapi.get_summoner_by_name(summoner)
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid summoner. Either wrong "
                               "summoner name or region. Check your console.")
            return
        try:
            cur = summoner.current_game()
            cur = cur.to_json()
            cur = json.loads(cur)
        except Exception as e:
            await self.bot.say("Summoner isn't in a game right now.")
            print(e)
            return

        #If champions are banned
        banned_champions_id = cur['bannedChampions']
        banned_champions = []

        for champ_bans in banned_champions_id:
            champ_name = riotapi.get_champion_by_id(champ_bans['championId'])
            banned_champions.append(champ_name)

        participants = cur['participants']
        players = []
        chosen_one = summoner.name
        #get players
        i = 0
        for participant in participants:
            i += 1
            player = {}
            summoner = riotapi.get_summoner_by_name(participant['summonerName'])
            player['teamId'] = participant['teamId']
            player['championId'] = participant['championId']
            player['championName'] = riotapi.get_champion_by_id(participant['championId'])
            player['summonerId'] = participant['summonerId']
            player['summonerName'] = participant['summonerName']
            players.append(player)
            try:#To get user tier and division and lp
                leagues = summoner.leagues()
                name = summoner.name
                tier = leagues[0].tier.name.title()
                tier_info = leagues[0].to_json()
                tier_info_dict = json.loads(tier_info)
                tier_users = tier_info_dict['entries']
                user_stats = [s for s in tier_users if s['playerOrTeamName'] == name]
                div = user_stats[0]['division']
                lp = user_stats[0]['leaguePoints']
                if div == "V":
                    div = "5"
                elif div == "IV":
                    div = "4"
                elif div == "III":
                    div = "3"
                elif div == "II":
                    div = "2"
                elif div == "I":
                    div = "1"
                losses = user_stats[0]['losses']
                wins = user_stats[0]['wins']
                total_games = wins + losses
                winrate = wins / total_games
                winrate = str(winrate)
                winrate = winrate[2:4]
                player['winrate'] = winrate
                player['division'] = div
                player['tier'] = tier
                player['rank'] = "{}{}".format(tier[0], div)
            except Exception as e:
                print(e)
                pass

        #get what team you're on
        for player in players:
            if player['summonerName'] == chosen_one:
                your_team_id = player['teamId']

        your_team = []
        enemy_team = []
        i = 0
        bans = ""
        for banned_champion in banned_champions:
            if i == 0:
                bans += "{}".format(banned_champion)
            else:
                bans += ", {}".format(banned_champion)
            i += 1

        #seperate teams
        for player in players:
            if player['teamId'] == your_team_id:
                your_team.append(player)
            else:
                enemy_team.append(player)

        #List teammates and their champs
        your_team_str = ""
        your_team_champs = ""
        your_team_stats = ""
        for player in your_team:
            try:
                your_team_str += "{}\n".format(player['summonerName'])
                your_team_champs += "{}\n".format(player['championName'])
                your_team_stats += "{}% - {}\n".format(player['winrate'], player['rank'])
            except:
                your_team_str += "{}\n".format(player['summonerName'])
                your_team_champs += "{}\n".format(player['championName'])
                your_team_stats += "   \n"

        enemy_team_str = ""
        enemy_team_champs = ""
        enemy_team_stats = ""
        for player in enemy_team:
            try:
                enemy_team_str += "{}\n".format(player['summonerName'])
                enemy_team_champs += "{}\n".format(player['championName'])
                enemy_team_stats += "{}% - {}\n".format(player['winrate'], player['rank'])
            except:
                enemy_team_str += "{}\n".format(player['summonerName'])
                enemy_team_champs += "{}\n".format(player['championName'])
                enemy_team_stats += "Unranked\n"

        region = region.upper()


        #start embedding
        embed = discord.Embed(description="{}".format(cur['gameId']), color=self.color)
        embed.add_field(name="Region", value=region.upper())
        embed.add_field(name="Type", value=cur['gameMode'].lower().title())
        if bans != "":
            embed.add_field(name="Bans", value=bans, inline=False)
        else:
            embed.add_field(name="Bans", value="None", inline=False)

        embed.add_field(name="Your Team",value=your_team_str)
        embed.add_field(name="Stats", value=your_team_stats)
        embed.add_field(name="Champions", value=your_team_champs)

        embed.add_field(name="Enemy Team",value=enemy_team_str)
        embed.add_field(name="Stats", value=enemy_team_stats)
        embed.add_field(name="Champions", value=enemy_team_champs)


        embed.set_author(name="{}'s current match".format(chosen_one))
        #embed.set_thumbnail(url='http://vignette1.wikia.nocookie.net/leagueoflegends/images/1/12/League_of_Legends_Icon.png/revision/latest?cb=20150402234343')

        await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def lastmatch(self, ctx, region, *, summoner):
        try:
            riotapi.set_region(region)
        except ValueError as e:
            print(e)
            await self.bot.say("Invalid region! Try again.")
            return
        except Exception as e:
            print(e)
            await self.bot.say("Check your console for logs.")
            return
        try:
            summoner = riotapi.get_summoner_by_name(summoner)
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid summoner. Either wrong "
                               "summoner name or region. Check your console.")
            return
        #asd = me.top_champion_masteries()
        player_stats = {}
        name = summoner.name
        _id = summoner.id
        region = region
        level = summoner.level
        matches = summoner.recent_games()
        last_match = matches[0].to_json()
        last_match = json.loads(last_match)
        match_type = last_match['subType'].title()
        deaths = last_match['stats']["numDeaths"]
        kills = last_match['stats']['championsKilled']
        assists = last_match['stats']['assists']
        last_champion_id = last_match['championId']
        last_champion_name = riotapi.get_champion_by_id(last_champion_id).name
        creeps = last_match['stats']["minionsKilled"]
        poop = True
        try:
            triple_kills = last_match['tripleKills']
            triple = True
        except:
            triple = False
        try:
            quadra_kills = last_match['quadraKills']
            quadra = True
        except:
            quadra = False
        try:
            penta_kills = last_match['pentaKills']
            penta = True
        except:
            penta = False
        msg =  "```ruby\n"
        msg += "Last Match of {}:\n\n".format(name)
        msg += "Match Type     -   {}\n".format(match_type)
        msg += "Region         -   {}\n".format(region.upper())
        msg += "Champion       -   {}\n".format(last_champion_name)
        msg += "Score K/D/A    -   {}/{}/{}\n".format(kills, deaths, assists)
        msg += "Creep Score    -   {}".format(creeps)
        if triple:
            msg += "Triple Kills   -   {}".format(triple_kills)
        if quadra:
            msg += "Quadra Kills   -   {}".format(quadra_kills)
        if penta:
            msg += "Penta Kills    -   {}".format(penta_kills)

        msg += "```"
        await self.bot.say(msg)

    @commands.command(pass_context = True)
    async def summoner(self, ctx, region, *, summoner):
        try:
            riotapi.set_region(region)
        except ValueError as e:
            print(e)
            await self.bot.say("Invalid region! Try again.")
            return
        except Exception as e:
            print(e)
            await self.bot.say("Check your console for logs.")
            return
        try:
            summoner = riotapi.get_summoner_by_name(summoner)
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid summoner. Either wrong "
                               "summoner name or region. Check your console.")
            return

        #Get basic user info
        name = summoner.name
        _id = summoner.id
        region = region
        level = summoner.level
        ma_pages = len(summoner.mastery_pages())
        ru_pages = len(summoner.rune_pages())
        if int(summoner.level) == 30:#To get user tier and division and lp
            leagues = summoner.leagues()
            tier = leagues[0].tier.name.title()
            tier_info = leagues[0].to_json()
            tier_info_dict = json.loads(tier_info)
            tier_users = tier_info_dict['entries']
            user_stats = [s for s in tier_users if s['playerOrTeamName'] == name]
            div = user_stats[0]['division']
            lp = user_stats[0]['leaguePoints']
            losses = user_stats[0]['losses']
            wins = user_stats[0]['wins']
            total_games = wins + losses
            winrate = wins / total_games
            winrate = str(winrate)
            winrate = winrate[2:4]
        try:
            top_champs = summoner.top_champion_masteries()
        except:
            pass

        #The message that is sent
        embed = discord.Embed(description = "{}".format(_id), color = self.color)
        embed.add_field(name="Region", value = region.upper())
        embed.set_thumbnail(url='http://vignette1.wikia.nocookie.net/leagueoflegends/images/1/12/League_of_Legends_Icon.png/revision/latest?cb=20150402234343')

        embed.set_author(name="{}".format(name))
        embed.add_field(name="Level", value = "{}".format(level))
        if int(summoner.level) == 30:
            embed.add_field(name="Rank", value= "{} {}, {} LP".format(tier, div, lp))
            embed.add_field(name="Ranked W/L", value= "{}/{} - {}%".format(wins, losses, winrate))
        embed.add_field(name="Mastery Pages", value = str(ma_pages))
        embed.add_field(name="Rune Pages", value = str(ru_pages))
        try:
            title = "Top Champion Masteries:"
            i = 0
            msg = ""
            for champ in top_champs:
                if i == 0:
                    msg += "{}".format(champ)
                    i += 1
                else:
                    msg += " - {}".format(champ)
            embed.add_field(name=title, value=msg, inline=False)
        except:
            pass
        await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def champion(self, ctx, *, champion):
        champion = champion.title()
        try:
            champ = riotapi.get_champion_by_name(champion)
            champ.name
        except Exception as e:
            print(e)
            await self.bot.say("Probably an invalid champion. Either wrong "
                               "name or error. Check your console.")
            return
        image_link = "http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/" + champ.image.link
        name = champ.name
        _id = champ.id
        champggname = champ.name.replace(" ", "").replace("'", "")
        champgg = 'http://api.champion.gg'
        matchup_url = '{}/champion/{}/matchup?api_key={}'.format(champgg, champggname, championgg_key)
        #get json from champion.gg api
        async with aiohttp.get(matchup_url) as response:
            matchups = await response.json()
        matchup_list = matchups[0]["matchups"]
        #get matchups
        matchup_champion = {}

        for matchup in matchup_list:
            enemy_champ = matchup['key']
            your_winrate = matchup['winRate']
            matchup_champion[enemy_champ] = your_winrate

        sorted_matchup_lose = collections.OrderedDict(sorted(matchup_champion.items(), key = lambda t: t[1]))
        sorted_matchup_win = collections.OrderedDict(sorted(matchup_champion.items(), key = lambda t: t[1], reverse=True))
        general_winrate_url = '{}/champion/{}/general?api_key={}'.format(champgg, champggname, championgg_key)

        async with aiohttp.get(general_winrate_url) as response:
            general_winrate_list = await response.json()

        general_winrate_dic = general_winrate_list[0]
        general_winrate = general_winrate_dic['winPercent']['val']
        q = ""
        w = ""
        e = ""
        r = ""

        embed = discord.Embed(description="{}".format(_id), color = self.color)
        embed.set_thumbnail(url=image_link)
        embed.set_author(name="{}".format(champ.name), url=image_link)

        p = champ.passive.name
        roles = champ.tags
        abilities = [q, w, e ,r]
        spells = ["Q", "W", "E", "R"]
        i = 0
        while i <= 3:
            abilities[i] = champ.spells[i].name
            i += 1

        embed.add_field(name="Passive", value=p)
        embed.add_field(name="Winrate", value = "{}%".format(general_winrate))

        i = 0

        #Get skill order
        ability_url = '{}/champion/{}/skills/mostPopular?api_key={}'.format(champgg, champggname, championgg_key)
        async with aiohttp.get(ability_url) as response:
            skill_order_dic = await response.json()
        skill_order_info = skill_order_dic[0]
        skill_order = skill_order_info["order"]

        #Get item set
        items_url = '{}/champion/{}/items/finished/mostPopular?api_key={}'.format(champgg, champggname, championgg_key)
        async with aiohttp.get(items_url) as response:
            items_lists = await response.json()
        for items_dic in items_lists:
            if 'item' not in items_dic:
                continue
            elif items_dic['item'] != []:
                items_dic = items_dic
        items_list = items_dic["items"]
        items_set_role = items_dic['role']
        msg = ""
        cd = ""
        #Get abilities
        while i <= 3:
            ability = abilities[i]
            spell = spells[i]
            msg += "{}/{}".format(spell, ability)
            d = 0
            for cooldown in champ.spells[i].cooldowns:
                cooldown = str(cooldown).replace(".0", "")
                if d == 0:
                    cd += "{}".format(cooldown)
                    d += 1
                else:
                    cd += "/{}".format(cooldown)
            i += 1
            msg += "\n"
            cd += "\n"

        embed.add_field(name="Abilities", value=msg)
        embed.add_field(name="Cooldowns", value=cd)

        #say skill order
        msg = ""
        i = 0
        for skill in skill_order:
            if skill == None:
                skill = "R"
            if i == 0:
                msg += "{}".format(skill)
                i += 1
            else:
                msg += "/{}".format(skill)

        embed.add_field(name="Maxing order", value=msg)

        #get roles
        msg = ""
        i = 0
        for item in items_list:
            if i == 0:
                msg += "{}".format(riotapi.get_item(item).name.replace("'", "").replace('"', ""))
                i += 1
            else:
                msg += "\n{}".format(riotapi.get_item(item).name.replace("'", "").replace('"', ""))

        embed.add_field(name="Build path/{}".format(items_set_role), value=msg)

        try:
            msg = ""
            i = 0
            for role in roles:
                if i == 0:
                    msg += "{}".format(role)
                    i += 1
                else:
                    msg += " - {}".format(role)

            embed.add_field(name="Roles", value=msg)

        except:
            pass
        i = 0
        #Get counters
        msg = ""
        for champ in sorted_matchup_win:
            if i == 3:
                break
            elif i == 0:
                msg += "{} ({}%)".format(champ, sorted_matchup_win[champ])
            else:
                msg += "\n{} ({}%)".format(champ, sorted_matchup_win[champ])
            i += 1

        embed.add_field(name="Counters", value=msg)

        msg = ""
        i = 0
        for champ in sorted_matchup_lose:
            if i == 3:
                break
            elif i == 0:
                msg += "{} ({}%)".format(champ, sorted_matchup_win[champ])
            else:
                msg += "\n{} ({}%)".format(champ, sorted_matchup_win[champ])
            i += 1

        embed.add_field(name="Countered", value=msg)

        await self.bot.say(embed=embed)

    @opgg.command()
    async def na(self, *, summoner):
        await self.bot.say("http://na.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def eune(self, *, summoner):
        await self.bot.say("http://eune.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def euw(self, *, summoner):
        await self.bot.say("http://euw.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["kr"])
    async def korea(self, *, summoner):
        await self.bot.say("http://www.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["jp"])
    async def japan(self, *, summoner):
        await self.bot.say("http://jp.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["br"])
    async def brazil(self, *, summoner):
        await self.bot.say("http://br.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["tr"])
    async def turkey(self, *, summoner):
        await self.bot.say("http://tr.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["oce"])
    async def oceania(self, *, summoner):
        await self.bot.say("http://oce.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def las(self, *, summoner):
        await self.bot.say("http://las.op.gg/summoner/userName=" + summoner)

    @opgg.command()
    async def lan(self, *, summoner):
        await self.bot.say("http://lan.op.gg/summoner/userName=" + summoner)

    @opgg.command(aliases = ["ru"])
    async def russia(self, *, summoner):
        await self.bot.say("http://ru.op.gg/summoner/userName=" + summoner)



def setup(bot):
    if isAvailable:
        bot.add_cog(League(bot))
    else:
        raise RuntimeError("You need to run `pip3 install cassiopeia`")
