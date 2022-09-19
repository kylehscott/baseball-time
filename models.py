from app import db
import sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Games(db.Model):

    __tablename__ = "games"

    #game_info = db.relationship('gamelogs', backref='gamelogs.games', primaryjoin='games.date==gamelogs.date', lazy='joined')

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    date = db.Column(db.String)
    awayTeam = db.Column(db.String)
    homeTeam = db.Column(db.String)
    channelId = db.Column(db.String)
    gameNo = db.Column(db.Integer)

    home_pitcher = relationship("Gamelogs", primaryjoin="and_(Games.date==Gamelogs.date, Games.homeTeam==Gamelogs.homTeam)")


    def __init__(self, url, date, awayTeam, homeTeam, channelId, gameNo):
        self.url = url
        self.date = date
        self.awayTeam = awayTeam
        self.homeTeam = homeTeam
        self.channelId = channelId
        self.gameNo = gameNo


    def __repr__(self):
        return "'{0}', '{1}', '{2}', '{3}'".format(self.url, self.date, self.homeTeam, self.awayTeam)

class Gamelogs(db.Model):

    __tablename__ = "gamelogs"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, ForeignKey('games.date'))
    gameNo = db.Column(db.String)
    dayOfWeek = db.Column(db.String)
    visTeam = db.Column(db.String)
    visTeamGm = db.Column(db.String)
    homTeam = db.Column(db.String, ForeignKey('games.homeTeam'))
    homTeamGm = db.Column(db.String)
    dayNight = db.Column(db.String)
    parkId = db.Column(db.String)
    attendance = db.Column(db.String)
    timeOfGame = db.Column(db.String)
    visManId = db.Column(db.String)
    visMan = db.Column(db.String)
    homManId = db.Column(db.String)
    homMan = db.Column(db.String)
    visPitchId = db.Column(db.String)
    visPitch = db.Column(db.String)
    homPitchId = db.Column(db.String)
    homPitch = db.Column(db.String)
    visBatOneID = db.Column(db.String)
    visBatOne = db.Column(db.String)
    visBatOnePos = db.Column(db.String)
    visBatTwoID = db.Column(db.String)
    visBatTwo = db.Column(db.String)
    visBatTwoPos = db.Column(db.String)
    visBatThreeID = db.Column(db.String)
    visBatThree = db.Column(db.String)
    visBatThreePos = db.Column(db.String)
    visBatFourID = db.Column(db.String)
    visBatFour = db.Column(db.String)
    visBatFourPos = db.Column(db.String)
    visBatFiveID = db.Column(db.String)
    visBatFive = db.Column(db.String)
    visBatFivePos = db.Column(db.String)
    visBatSixID = db.Column(db.String)
    visBatSix = db.Column(db.String)
    visBatSixPos = db.Column(db.String)
    visBatSevenID = db.Column(db.String)
    visBatSeven = db.Column(db.String)
    visBatSevenPos = db.Column(db.String)
    visBatEightID = db.Column(db.String)
    visBatEight = db.Column(db.String)
    visBatEightPos = db.Column(db.String)
    visBatNineID = db.Column(db.String)
    visBatNine = db.Column(db.String)
    visBatNinePos = db.Column(db.String)
    homBatOneID = db.Column(db.String)
    homBatOne = db.Column(db.String)
    homBatOnePos = db.Column(db.String)
    homBatTwoID = db.Column(db.String)
    homBatTwo = db.Column(db.String)
    homBatTwoPos = db.Column(db.String)
    homBatThreeID = db.Column(db.String)
    homBatThree = db.Column(db.String)
    homBatThreePos = db.Column(db.String)
    homBatFourID = db.Column(db.String)
    homBatFour = db.Column(db.String)
    homBatFourPos = db.Column(db.String)
    homBatFiveID = db.Column(db.String)
    homBatFive = db.Column(db.String)
    homBatFivePos = db.Column(db.String)
    homBatSixID = db.Column(db.String)
    homBatSix = db.Column(db.String)
    homBatSixPos = db.Column(db.String)
    homBatSevenID = db.Column(db.String)
    homBatSeven = db.Column(db.String)
    homBatSevenPos = db.Column(db.String)
    homBatEightID = db.Column(db.String)
    homBatEight = db.Column(db.String)
    homBatEightPos = db.Column(db.String)
    homBatNineID = db.Column(db.String)
    homBatNine = db.Column(db.String)
    homBatNinePos = db.Column(db.String)
    gameType = db.Column(db.String)
    homTeamLg = db.Column(db.String)
    visHits = db.Column(db.String)
    homHits = db.Column(db.String)
    visHBP = db.Column(db.String)
    visBB = db.Column(db.String)
    visIBB = db.Column(db.String)
    homHBP = db.Column(db.String)
    homBB = db.Column(db.String)
    homIBB = db.Column(db.String)


    def __init__(self, date, gameNo, dayOfWeek, visTeam, visTeamGm, homTeam,
                 homTeamGm, dayNight, parkId, attendance, timeOfGame, visManId,
                 visMan, homManId, homMan, visPitchId, visPitch, homPitchId,
                 homPitch, visBatOneID, visBatOne, visBatOnePos, visBatTwoID,
                 visBatTwo, visBatTwoPos, visBatThreeID, visBatThree, visBatThreePos,
                 visBatFourID, visBatFour, visBatFourPos, visBatFiveID, visBatFive,
                 visBatFivePos, visBatSixID, visBatSix, visBatSixPos, visBatSevenID,
                 visBatSeven, visBatSevenPos, visBatEightID, visBatEight, visBatEightPos,
                 visBatNineID, visBatNine, visBatNinePos, homBatOneID, homBatOne,
                 homBatOnePos, homBatTwoID, homBatTwo, homBatTwoPos, homBatThreeID,
                 homBatThree, homBatThreePos, homBatFourID, homBatFour,
                 homBatFourPos, homBatFiveID, homBatFive, homBatFivePos,
                 homBatSixID, homBatSix, homBatSixPos, homBatSevenID, homBatSeven,
                 homBatSevenPos, homBatEightID, homBatEight, homBatEightPos,
                 homBatNineID, homBatNine, homBatNinePos, gameType, homTeamLg, visHits, homHits,
                 visHBP, visBB, visIBB, homHBP, homBB, homIBB):
        self.date = date
        self.gameNo = gameNo
        self.dayOfWeek = dayOfWeek
        self.visTeam = visTeam
        self.visTeamGm = visTeamGm
        self.homTeam = homTeam
        self.homTeamLg = homTeamLg
        self.homTeamGm = homTeamGm
        self.dayNight = dayNight
        self.parkId = parkId
        self.attendance = attendance
        self.timeOfGame = timeOfGame
        self.visManId = visManId
        self.visMan = visMan
        self.homManId = homManId
        self.homMan = homeMan
        self.visPitchId = visPitchId
        self.visPitch = visPitch
        self.homPitchId = homPitchId
        self.homPitch = homPitch
        self.visBatOneID = visBatOneID
        self.visBatOne = visBatOne
        self.visBatOnePos = visBatOnePos
        self.visBatTwoID = visBatTwoID
        self.visBatTwo = visBatTwo
        self.visBatTwoPos = visBatTwoPos
        self.visBatThreeID = visBatThreeID
        self.visBatThree = visBatThree
        self.visBatThreePos = visBatThreePos
        self.visBatFourID = visBatFourID
        self.visBatFour = visBatFour
        self.visBatFourPos = visBatFourPos
        self.visBatFiveID = visBatFiveID
        self.visBatFive = visBatFive
        self.visBatFivePos = visBatFivePos
        self.visBatSixID = visBatSixID
        self.visBatSix = visBatSix
        self.visBatSixPos = visBatSixPos
        self.visBatSevenID = visBatSevenID
        self.visBatSeven = visBatSeven
        self.visBatSevenPos = visBatSevenPos
        self.visBatEightID = visBatEightID
        self.visBatEight = visBatEight
        self.visBatEightPos = visBatEightPos
        self.visBatNineID = visBatNineID
        self.visBatNine = visBatNine
        self.visBatNinePos = visBatNinePos
        self.homBatOneID = homBatOneID
        self.homBatOne = homBatOne
        self.homBatOnePos = homBatOnePos
        self.homBatTwoID = homBatTwoID
        self.homBatTwo = homBatTwo
        self.homBatTwoPos = homBatTwoPos
        self.homBatThreeID = homBatThreeID
        self.homBatThree = homBatThree
        self.homBatThreePos = homBatThreePos
        self.homBatFourID = homBatFourID
        self.homBatFour = homBatFour
        self.homBatFourPos = homBatFourPos
        self.homBatFiveID = homBatFiveID
        self.homBatFive = homBatFive
        self.homBatFivePos = homBatFivePos
        self.homBatSixID = homBatSixID
        self.homBatSix = homBatSix
        self.homBatSixPos = homBatSixPos
        self.homBatSevenID = homBatSevenID
        self.homBatSeven = homBatSeven
        self.homBatSevenPos = homBatSevenPos
        self.homBatEightID = homBatEightID
        self.homBatEight = homBatEight
        self.homBatEightPos = homBatEightPos
        self.homBatNineID = homBatNineID
        self.homBatNine = homBatNine
        self.homBatNinePos = homeBatNinePos
        self.gameType = gameType
        self.visHits = visHits
        self.homHits = homHits
        self.visHBP = visHBP
        self.visBB = visBB
        self.visIBB = visIBB
        self.homHBP = homHBP
        self.homBB = homBB
        self.homIBB = homIBB

    def __repr__(self):
        return "'{0}', '{1}', '{2}', '{3}', '{4}'".format(self.date, self.visTeam, self.visTeamGm, self.homTeam, self.parkId)


class Parkcode(db.Model):

    __tablename__ = "parkcode"

    id = db.Column(db.Integer, primary_key=True)
    parkId = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    aka = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    league = db.Column(db.String)
    notes = db.Column(db.String)


    def __init__(self, parkId, name, aka, city, state, start, end, league, notes):
        self.parkId = parkId
        self.name = name
        self.aka = aka
        self.city = city
        self.state = state
        self.start = start
        self.end = end
        self.league = league
        self.notes = notes


    def __repr__(self):
        return "{0}".format(self.name)

class Teamcode(db.Model):

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.String)
    franId = db.Column(db.String)
    league = db.Column(db.String)
    div = db.Column(db.String)
    location_name = db.Column(db.String)
    nickname = db.Column(db.String)
    alt_nickname = db.Column(db.String)
    start = db.Column(db.String)
    end = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)


    def __init__(self, teamId, franId, league, div, location_name, nickname, alt_nickname, start, end, city, state):
        self.teamId = teamId
        self.franId = franId
        self.league = league
        self.div = div
        self.location_name = location_name
        self.nickname = nickname
        self.alt_nickname = alt_nickname
        self.start = start
        self.end = end
        self.city = city
        self.state = state


    def __repr__(self):
        return "{0}".format(self.name)
