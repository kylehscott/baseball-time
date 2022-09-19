# -*- coding: utf-8 -*-
import urllib, json
from flask import Flask, render_template, url_for, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from sqlalchemy import desc
from sqlalchemy import func
from random import randint
from datetime import date
from datetime import datetime
from calendar import monthrange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///final.db'
app.jinja_env.add_extension('jinja2.ext.do')
db = SQLAlchemy(app)

#app.debug = True

from models import *

teams = ["ANA", "ARI", "ATL", "BAL", "BOS", "CHA", "CHN", "CIN", "CLE", "COL", "DET", "HOU",
         "KCA", "LAN", "MIA", "MIL", "MIN", "NYA", "NYN", "PHI", "PIT", "SDN", "SEA", "SFN",
         "SLN", "TBA", "TEX", "TOR", "WAS"]

month_list = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

positions = ["", "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]

def format_date(date, date_format):
    strp_date = datetime.strptime(str(date), "%Y%m%d")
    return datetime.strftime(strp_date, date_format)

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def ballpark_string(bp_code):
    ballpark = db.session.query(Parkcode).filter((Parkcode.parkId == bp_code)).first()
    return ballpark

app.jinja_env.globals.update(format_date=format_date)
app.jinja_env.globals.update(ord=ord)
app.jinja_env.globals.update(ballpark_string=ballpark_string)

@app.route("/")
def home():
    #total_games = len(Games.query.all())
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam)
    total_games = len(games)
    recent_games = games.order_by(desc(Games.date)).limit(5)
    recent_added = games.order_by(desc(Games.id)).limit(5)
    return render_template('main.html', games=games, recent_games=recent_games, recent_added=recent_added, total_games=total_games)

@app.route("/random/")
@app.route("/random", methods=['GET'])
def random():
    if request.args.get('date') and request.args.get('team'):
        date = request.args.get('date')
        team = request.args.get('team')
        games = Games.query.filter(Games.date.contains(str(date))).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper()))
        num = randint(0, games.count() - 1)
    elif request.args.get('date'):
        date = request.args.get('date')
        games = Games.query.filter(Games.date.contains(str(date)))
        num = randint(0, games.count() - 1)
    elif request.args.get('team'):
        team = request.args.get('team')
        games = Games.query.filter((Games.homeTeam == team.upper()))
        num = randint(0, games.count() - 1)
    else:
        games = Games.query.all()
        num = randint(0, len(games) - 1)
    random_game = games[num]
    year = random_game.date[:4]
    month = random_game.date[4:6]
    day = random_game.date[6:]
    db_header = str(random_game.gameNo)
    return redirect("/games/" + random_game.homeTeam + "/" + year + "/" + month + "/" + day + "/" + db_header)

@app.route("/years/<int:year>/")
def yearsPage(year):
    header = str(year) + " Season"
    games = Games.query.filter(Games.date.contains(str(year))).order_by(Games.date)
    return render_template('month_view.html', games=games, year=year, month_list=month_list, header=header)

@app.route("/years/<int:year>/<int:month>/")
def monthsPage(year, month):
    header = str(month_list[month - 1]) + " " + str(year)
    month_range = monthrange(year, month)
    month = '{0}'.format(str(month).zfill(2))
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter(Games.date.contains(str(year) + str(month))).order_by(Games.date)
    unlisted_games = Games.query.filter(Games.date.contains(str(year) + str(month))).order_by(Games.date)
    game_list = []
    games_len = 0
    return render_template('month_games.html', games=games, year=year, month=month,
                                month_list=month_list, games_len=games_len, month_range=month_range, game_list=game_list,
                                unlisted_games=unlisted_games, header=header)

@app.route("/years/<int:year>/<int:month>/<int:day>/")
def daysPage(year, month, day):
    month = '{0}'.format(str(month).zfill(2))
    day = '{0}'.format(str(day).zfill(2))
    games = Games.query.filter(Games.date.contains(str(year) + str(month) + str(day))).order_by(Games.date)
    gamelog = db.session.query(Gamelogs).filter(Gamelogs.date.contains(str(year) + str(month) + str(day))).all()
    return render_template('game_view.html', games=games, year=year, month=month, month_list=month_list, gamelog=gamelog)

@app.route("/teams/ALS/<year>/")
@app.route("/teams/NLS/<year>/")
def allStarRedirect(year):
    return redirect("/games/all-star-games/")

@app.route("/teams/<team>/")
def teamPages(team):
    header = team + " Games By Year"
    team = team
    if team == "BRO":
        return redirect("/teams/LAN/")
    elif team == "FLO":
        return redirect("/teams/MIA/")
    elif team == "MON":
        return redirect("/teams/WAS/")
    elif team == "CAL":
        return redirect("/teams/ANA/")
    elif team == "MIA":
        games = db.session.query(Games).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper()) | (Games.homeTeam == "FLO") | (Games.awayTeam == "FLO")).order_by(Games.date)
    elif team == "WAS":
        games = db.session.query(Games).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper()) | (Games.homeTeam == "MON") | (Games.awayTeam == "MON")).order_by(Games.date)
    elif team == "LAN":
        games = db.session.query(Games).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper()) | (Games.homeTeam == "BRO") | (Games.awayTeam == "BRO")).order_by(Games.date)
    elif team == "ANA":
        games = db.session.query(Games).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper()) | (Games.homeTeam == "CAL") | (Games.awayTeam == "CAL")).order_by(Games.date)
    else:
        games = db.session.query(Games).filter((Games.homeTeam == team.upper()) | (Games.awayTeam == team.upper())).order_by(Games.date)
    return render_template('years.html', games=games, team=team, header=header)

@app.route("/games/all-star-games/")
def allStarGames():
    header = "All-Star Games"
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Games.homeTeam == "ALS") | (Games.awayTeam == "ALS")).order_by(Games.date)
    return render_template('asg.html', games=games, header=header)

@app.route("/teams/<team>/<int:year>/")
def teamYears(team, year):
    con_state = Games.date.contains(str(year))
    old_games = Games.query.filter(((Games.homeTeam == team.upper()) & con_state) | ((Games.awayTeam == team.upper()) & con_state)).order_by(Games.date)
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter(((Games.homeTeam == team.upper()) & con_state) | ((Games.awayTeam == team.upper()) & con_state)).order_by(Games.date)
    team_code = db.session.query(Teamcode).filter((Teamcode.franId == team)).order_by(Teamcode.end).first()
    header = str(year) + " " + team + " Season"
    game_list = []
    return render_template('team_games.html', games=games, team=team, year=year, month_list=month_list, old_games=old_games, game_list=game_list, team_code=team_code, header=header)

@app.route("/pitchers/<pitcher_id>/")
def pitchers(pitcher_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Gamelogs.homPitchId == pitcher_id) | (Gamelogs.visPitchId == pitcher_id)).order_by(Games.date)
    return render_template('player_games.html', games=games, pitcher_id=pitcher_id)

@app.route("/pitchers/<pitcher_id>/random/")
def random_pitchers(pitcher_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Gamelogs.homPitchId == pitcher_id) | (Gamelogs.visPitchId == pitcher_id))
    num = randint(0, games.count() - 1)
    random_game = games[num][0]
    year = random_game.date[:4]
    month = random_game.date[4:6]
    day = random_game.date[6:]
    db_header = str(random_game.gameNo)
    return redirect("/games/" + random_game.homeTeam + "/" + year + "/" + month + "/" + day + "/" + db_header)


@app.route("/managers/<manager_id>/")
def managers(manager_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Gamelogs.homManId == manager_id) | (Gamelogs.visManId == manager_id)).order_by(Games.date)
    return render_template('manager_games.html', games=games, manager_id=manager_id)

@app.route("/managers/<manager_id>/random/")
def random_managers(manager_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Gamelogs.homManId == manager_id) | (Gamelogs.visManId == manager_id)).order_by(Games.date)
    num = randint(0, games.count() - 1)
    random_game = games[num][0]
    year = random_game.date[:4]
    month = random_game.date[4:6]
    day = random_game.date[6:]
    db_header = str(random_game.gameNo)
    return redirect("/games/" + random_game.homeTeam + "/" + year + "/" + month + "/" + day + "/" + db_header)

@app.route("/batters/<batter_id>/")
def batters(batter_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo) \
    .filter((Gamelogs.visBatOneID == batter_id) | \
    (Gamelogs.visBatTwoID == batter_id) | \
    (Gamelogs.visBatThreeID == batter_id) | \
    (Gamelogs.visBatFourID == batter_id) | \
    (Gamelogs.visBatFiveID == batter_id) | \
    (Gamelogs.visBatSixID == batter_id) | \
    (Gamelogs.visBatSevenID == batter_id) | \
    (Gamelogs.visBatEightID == batter_id) | \
    (Gamelogs.visBatNineID == batter_id) | \
    (Gamelogs.homBatOneID == batter_id) | \
    (Gamelogs.homBatTwoID == batter_id) | \
    (Gamelogs.homBatThreeID == batter_id) | \
    (Gamelogs.homBatFourID == batter_id) | \
    (Gamelogs.homBatFiveID == batter_id) | \
    (Gamelogs.homBatSixID == batter_id) | \
    (Gamelogs.homBatSevenID == batter_id) | \
    (Gamelogs.homBatEightID == batter_id) | \
    (Gamelogs.homBatNineID == batter_id)) \
    .order_by(Games.date)
    return render_template('batter_games.html', games=games, batter_id=batter_id)

@app.route("/batters/<batter_id>/random/")
def random_batters(batter_id):
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo) \
    .filter((Gamelogs.visBatOneID == batter_id) | \
    (Gamelogs.visBatTwoID == batter_id) | \
    (Gamelogs.visBatThreeID == batter_id) | \
    (Gamelogs.visBatFourID == batter_id) | \
    (Gamelogs.visBatFiveID == batter_id) | \
    (Gamelogs.visBatSixID == batter_id) | \
    (Gamelogs.visBatSevenID == batter_id) | \
    (Gamelogs.visBatEightID == batter_id) | \
    (Gamelogs.visBatNineID == batter_id) | \
    (Gamelogs.homBatOneID == batter_id) | \
    (Gamelogs.homBatTwoID == batter_id) | \
    (Gamelogs.homBatThreeID == batter_id) | \
    (Gamelogs.homBatFourID == batter_id) | \
    (Gamelogs.homBatFiveID == batter_id) | \
    (Gamelogs.homBatSixID == batter_id) | \
    (Gamelogs.homBatSevenID == batter_id) | \
    (Gamelogs.homBatEightID == batter_id) | \
    (Gamelogs.homBatNineID == batter_id)) \
    .order_by(Games.date)
    num = randint(0, games.count() - 1)
    random_game = games[num][0]
    year = random_game.date[:4]
    month = random_game.date[4:6]
    day = random_game.date[6:]
    db_header = str(random_game.gameNo)
    return redirect("/games/" + random_game.homeTeam + "/" + year + "/" + month + "/" + day + "/" + db_header)

@app.route("/years/")
def years():
    header = "Games By Year"
    games = db.session.query(Games).order_by(Games.date)
    return render_template('years.html', games=games, header=header)

@app.route("/teams/")
def teams():
    header = "Games By Team"
    teams = ["ANA", "ARI", "ATL", "BAL", "BOS", "CHA", "CHN", "CIN", "CLE", "COL", "DET", "HOU",
             "KCA", "LAN", "MIA", "MIL", "MIN", "NYA", "NYN", "OAK", "PHI", "PIT", "SDN", "SEA",
              "SFN", "SLN", "TBA", "TEX", "TOR", "WAS"]
    games = Games.query.all()
    return render_template('teams.html', teams=teams, games=games, header=header)

@app.route("/about/")
def about():
    games = db.session.query(Games).filter((Games.homeTeam == "SF") & Games.date.contains("2014-10-21"))
    return render_template('about.html', games=games)

@app.route("/games/<team>/<int:year>/<int:month>/<int:day>/<int:game_no>/")
def game_page(team, year, month, day, game_no):
    month = '{0}'.format(str(month).zfill(2))
    day = '{0}'.format(str(day).zfill(2))
    games = db.session.query(Games).filter((Games.homeTeam == team) & Games.date.contains(str(year) + str(month) + str(day)) & (Games.gameNo == game_no))
    gamelog = db.session.query(Gamelogs).filter((Gamelogs.homTeam == team) & (Gamelogs.gameNo == game_no) & Gamelogs.date.contains(str(year) + str(month) + str(day))).first()
    month_letter = month_list[int(month) - 1]
    day_ending = ord(int(day))

    game_url = games[0].url.split("?")

    if game_url[0] == "VIDEO_ID":
        game_url = game_url[1].split(",")[1]
    else:
        game_url = game_url[0]


    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + game_url + "&key=AIzaSyCLddbBOg4MWCwl5oz29urPC_BSdZe_dYc"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    channel_info = data["items"][0]["snippet"]

    channel_name = channel_info["channelTitle"]
    channel_url = channel_info["channelId"]

    if gamelog == None:
        ballpark = ""
        visiting_team = ""
        home_team = ""
        time_of_game = ""
    else:
        ballpark = db.session.query(Parkcode).filter((Parkcode.parkId == gamelog.parkId)).first()
        visiting_team = db.session.query(Teamcode).filter((Teamcode.franId == gamelog.visTeam)).order_by(Teamcode.end).first()
        home_team = db.session.query(Teamcode).filter((Teamcode.franId == gamelog.homTeam)).order_by(Teamcode.end).first()
        hours_of_game = int(gamelog.timeOfGame) / 60
        min_of_game = int(gamelog.timeOfGame)  - (hours_of_game * 60)
        time_of_game = str(hours_of_game) + ":" + str(min_of_game).zfill(2)

    header = games[0].awayTeam + " at " + games[0].homeTeam + ", " + str(month_list[int(month)-1]) + " " + str(day) + ", " + str(year)
    return render_template('game_page.html', games=games, gamelog=gamelog, ballpark=ballpark, team=team, year=year, month=month, day=day, month_letter=month_letter,
                                    day_ending=day_ending, positions=positions, visiting_team=visiting_team, home_team=home_team, time_of_game=time_of_game, game_no=game_no,
                                    header=header, channel_name=channel_name, channel_url=channel_url)
# Playlists
@app.route("/playlists/recently-played/")
def recently_played():
    playlist_name = "Recently Played Games"
    description = "Games played most recently to today's date"
    source = ""
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).order_by(Games.date.desc()).limit(25)
    return render_template('playlists.html', games=games, description=description, playlist_name=playlist_name, source=source)

@app.route("/playlists/recently-added/")
def recently_added():
    playlist_name = "Recently Added Games"
    description = "Games added most recently to the database."
    source = ""
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).order_by(Games.id.desc()).limit(25)
    return render_template('playlists.html', games=games, description=description, playlist_name=playlist_name, source=source)

@app.route("/playlists/game-sevens/")
def game_sevens():
    playlist_name = "Game 7's"
    description = "Final game of a 7 game series, loser goes home."
    source = ""
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter(Gamelogs.homTeamGm == "7").filter(Gamelogs.gameType != "").order_by(Games.date)
    return render_template('playlists.html', games=games, description=description, playlist_name=playlist_name, source=source)

@app.route("/playlists/no-hitters/")
def no_hitters():
    playlist_name = "No Hitters and Perfect Games"
    description = 'Major League Baseball (MLB) officially defines a no-hitter as a completed game in which a team that batted in at least nine innings recorded no hits. A pitcher who prevents the opposing team from achieving a hit is said to have "thrown a no-hitter".'
    source = "https://en.wikipedia.org/wiki/No-hitter"
    games = db.session.query(Games, Gamelogs).filter(Games.date == Gamelogs.date).filter(Games.homeTeam == Gamelogs.homTeam).filter(Games.gameNo == Gamelogs.gameNo).filter((Gamelogs.visHits == "0") | (Gamelogs.homHits == "0")).order_by(Games.date)
    return render_template('no-hitters.html', games=games, description=description, playlist_name=playlist_name, source=source)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('404.html'), 500


if __name__ == "__main__":
    app.run()
