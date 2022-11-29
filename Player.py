import json

#class for the stats
class Player():
  def __init__(self, data): 
    self.username = data['name']
    self.tag = data['tag']
    self.rank = data['currenttierpatched']
    self.rankimage = data['images']['small']
    self.curentRR = data['ranking_in_tier']
    self.rrChange = data['mmr_change_to_last_game']
    self.kd = 0.0
    self.acs = 0.0
    self.headshotPercent = 0.0

  def getUsername(self):
    return self.username
  def getTag(self):
    return self.tag
  def getRank(self):
    return self.rank
  def getImage(self):
    return self.rankimage
  def getRR(self):
    return self.curentRR
  def getRRChange(self):
    return self.rrChange
  def getKD(self):
    return self.kd
  def getACS(self):
    return self.acs
  def getHeadshot(self):
    return self.headshotPercent

  def parseStats(self, data):
    if len(data) < 1:
      return
    tmpKD = 0.0
    tmpACS = 0
    headshots = 0
    totalHits = 0
    #Loop through matches and grab relevant data
    for match in data:
      roundsPlayed = match['metadata']['rounds_played']
      for player in match['players']['all_players']:
        if player['name'] == self.username and player['tag'] == self.tag:
          tmpKD += player['stats']['kills'] / player['stats']['deaths']
          tmpACS += player['stats']['score'] / roundsPlayed
          headshots += player['stats']['headshots']
          totalHits += player['stats']['headshots']+player['stats']['bodyshots']+player['stats']['legshots']
    #Store Stats
    self.kd = tmpKD / len(data)
    self.acs = tmpACS / len(data)
    self.headshotPercent = headshots/totalHits * 100
