from itertools import combinations
from operator import add, mul

# Some user parameters

# Max number of follower teams to display for each individual mission. Does not
# affect the final results.
numCombs = 5
followerFile = 'followers.txt'
missionFile = 'missions.txt'

# List of mechanics, mostly for spell checking the text files.
mechanicsList = [
    'Danger Zones',
    'Deadly Minions',
    'Group Damage',
    'Magic Debuff',
    'Massive Strike',
    'Minion Swarms',
    'Powerful Spell',
    'Timed Battle',
    'Wild Aggression'
    ]

# List of traits, mostly for spell checking the text files.
traitsList = [
    'Extra Training', 'Fast Learner', 'Scavenger',
    'Alchemy', 'Blacksmithing', 'Enchanting', 'Engineering', 'Herbalism',
    'Inscription', 'Jewelcrafting', 'Leatherworking', 'Mining', 'Skinning',
    'Tailoring',
    'Beastslayer', 'Demonslayer', 'Furyslayer', 'Gronnslayer', 'Ogreslayer',
    'Orcslayer', 'Primalslayer', 'Talonslayer', 'Voidslayer',
    'Cave Dweller', 'Cold-Blooded', 'Guerilla Fighter', 'Marshwalker',
    'Mountaineer', 'Naturalist', 'Plainsrunner', 'Wastelander',
    'Ally of Argus', 'Brew Aficionado', 'Canine Companion', 'Child of Draenor',
    'Child of the Moon', 'Death Fascination', 'Dwarvenborn', 'Economist',
    'Elvenkind', 'Gnome-Lover', 'Humanist', 'Totemist', 'Voodoo Zealot',
    'Burst of Power', 'Epic Mount', 'High Stamina',
    'Lone Wolf', 'Dancer', 'Hearthstone Pro',
    'Evergreen', 'Combat Experience'
    ]

# Links racial perefence traits to their associated races.
racialTraits = {
    'Ally of Argus': 'Draenei',
    'Brew Aficionado': 'Pandaren',
    'Canine Companion': 'Worgen',
    'Child of Draenor': 'Orc',
    'Child of the Moon': 'Night Elf',
    'Death Fascination': 'Undead',
    'Dwarvenborn': 'Dwarf',
    'Economist': 'Goblin',
    'Elvenkind': 'Blood Elf',
    'Gnome-Lover': 'Gnome',
    'Humanist': 'Human',
    'Totemist': 'Tauren',
    'Voodoo Zealot': 'Troll'
    }

# Links mission environment type to its counter
environmentTraits = {
    'Beast': 'Beastslayer',
    'Demon': 'Demonslayer',
    'Fury': 'Furyslayer',
    'Breaker': 'Gronnslayer',
    'Ogre': 'Ogreslayer',
    'Orc': 'Orcslayer',
    'Primal': 'Primalslayer',
    'Arakkoa': 'Talonslayer',
    'Undead': 'Voidslayer',
    'Aberration': 'Voidslayer',
    'Underground': 'Cave Dweller',
    'Snow': 'Cold-Blooded',
    'Jungle': 'Guerilla Fighter',
    'Swamp': 'Marshwalker',
    'Mountains': 'Mountaineer',
    'Forest': 'Naturalist',
    'Plains': 'Plainsrunner',
    'Desert': 'Wastelander'
}

# Mission class to store mission data.
class Mission():
    
    def __init__(self, name, level, ilvl, missionType, length, baseSuccess, slots, mechanics):
        self.name = name
        self.level = int(level)
        self.ilvl = int(ilvl)
        self.missionType = missionType
        self.length = float(length)
        self.baseSuccess = float(baseSuccess)
        assert self.baseSuccess >= 0 and self.baseSuccess <= 1, "Base Success must be between 0 and 1."
        self.slots = int(slots)
        self.mechanics = mechanics
        
        self.difficulty = len(self.mechanics)*3 + self.slots
        
    # Calculates the success chance a team of followers will have on a mission.
    # There is probably a more efficient way to do this, but meh.
    def success(self, followers):
        score = float(0)
        # Contributions keeps track of each follower's contribution to the
        # mission's success.
        contributions = [float(0)]*len(followers)
        # Since we go through followers 1 at a time, we will keep track of
        # mounts and High Stamina/Burst of Power traits for the end.
        mounts = [0]*len(followers)
        shortMission = [0]*len(followers)
        longMission = [0]*len(followers)
        multipliers = [1]*len(followers)
        # Tracks whether each mechanic has been countered already.
        counters = [0]*len(self.mechanics)
        for i in range(len(followers)):
            f = followers[i]
            # Loop through each of a follower's abilities. If we find a mission
            # mechanic that can be countered and hasn't been countered yet, mark
            # it off.
            for c in f.counters:
                for j in range(len(self.mechanics)):
                    if c == self.mechanics[j] and counters[j] == 0:
                        counters[j] = 1
                        contributions[i] += 3
                        break
            for t in f.traits:
                # Racial preferences.
                if t in racialTraits:
                    for groupmate in followers:
                        if groupmate is not f and racialTraits[t] == groupmate.race:
                            contributions[i] += 1.5                
                # Environment traits.
                elif t in environmentTraits.values() and t == environmentTraits[self.missionType]:
                    contributions[i] += 1
                # Checking Epic Mount/Mission Duration traits.
                elif t == 'High Stamina':
                    longMission[i] = 1
                elif t == 'Burst of Power':
                    shortMission[i] = 1
                elif t == 'Epic Mount':
                    mounts[i] = 1
                # I am Blook.
                elif t == 'Combat Experience':
                    contributions[i] += 1
                elif t == 'Dancer' and 'Danger Zones' in self.mechanics:
                    contributions[i] += 1
                elif t == 'Lone Wolf' and self.slots == 1:
                    contributions[i] += 1
                
            # Follower level/item level multiplier calculations.
            undermulti = 1
            overmulti = 1
            if f.level < self.level:
                undermulti *= (3.0 - min(self.level - f.level, 3))/3
            elif f.level > self.level:
                overmulti *= (6.0 + min(f.level - self.level, 3))/6
            if f.ilvl < self.ilvl:
                undermulti *= (15.0 - min(self.ilvl - f.ilvl, 15))/15
            elif self.ilvl > 0 and f.ilvl > self.ilvl:
                overmulti *= (30.0 + min(f.ilvl - self.ilvl, 15))/30
            multipliers[i] = undermulti
            contributions[i] += overmulti
        # Mission duration after epic mounts for duration traits.
        length = self.length/(2**sum(mounts))
        if length < 7:
            contributions = map(add, contributions, shortMission)
        elif length > 7:
            contributions = map(add, contributions, longMission)
        contributions = map(mul, contributions, multipliers)
        score = sum(contributions)
        success = self.baseSuccess + (1 - self.baseSuccess)*score/self.difficulty
            
        return success

# Follower class to store follower data.
class Follower():
    
    def __init__(self, name, race, level, ilvl, counters, traits):
        self.name = name
        self.race = race
        self.level = level
        self.ilvl = ilvl
        self.counters = counters
        self.traits = traits
        
    def __repr__(self):
        return self.name

# Reads in follower data from text file.
def readFollowers(inputFile):
    followers = []
    with open(inputFile, 'r') as inFile:
        for line in inFile:
            line = line.strip()
            if not line[0] == '#':
                line = line.split(',')
                if len(line) > 6:
                    print 'Possible Error, follower: ' + line[0] + ', line too long.'
                elif len(line) < 6:
                    print 'Possible Error, follower: ' + line[0] + ', line too short. Skipping follower.'
                    continue
                for mechanic in line[4].split(';'):
                    if mechanic not in mechanicsList:
                        print 'Follower: ' + line[0] + ', Unknown mechanic counter: ' + mechanic      
                for trait in line[5].split(';'):
                    if trait not in traitsList:
                        print 'Unknown trait: ' + trait
                followers.append(Follower(line[0],line[1],int(line[2]),int(line[3]),line[4].split(';'),line[5].split(';')))
    return followers

# Reads in mission data from text file.
def readMissions(inputFile):
    missions = []
    with open(inputFile, 'r') as inFile:
        for line in inFile:
            line = line.strip()
            if not line[0] == '#':
                line = line.split(',')
                if len(line) > 8:
                    print 'Possible Error, mission ' + line[0] + ', line too long.'
                elif len(line) < 8:
                    print 'Possible Error, mission ' + line[0] + ', line too long. Skipping mission.'
                    continue
                for mechanic in line[7].split(';'):
                    if mechanic not in mechanicsList:
                        print 'Mission: ' + line[0] + ', Unknown mechanic: ' + mechanic
                missions.append(Mission(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7].split(';')))
    return missions

# Branch and bound optimization to find the minimum number of followers from
# which teams can be constructed to achieve maximum success for the missions
# specified.
def followerBnB(teams, curTeam = set(), minSize=float('inf')):
    global bnbcounter
    teamList = []
    if len(teams) == 1:
        for t in teams[0]:
            bnbcounter += 1
            newTeam = t | curTeam
            if len(newTeam) < minSize:
                teamList = [newTeam]
                minSize = len(newTeam)
            elif len(newTeam) == minSize:
                teamList.append(newTeam)
    else:
        for t in teams[0]:
            bnbcounter += 1
            newTeam = t | curTeam
            if len(newTeam) > minSize:
                continue
            possibleTeams = followerBnB(teams[1:], newTeam, minSize)
            if possibleTeams:
                if len(possibleTeams[0]) < minSize:
                    teamList = possibleTeams
                    minSize = len(possibleTeams[0])
                else:
                    teamList += possibleTeams
    return teamList

if __name__ == '__main__':

    followers = readFollowers(followerFile)
    missions = readMissions(missionFile)
    
    teams = []
    # Go through every possible combination of followers for each mission and
    # calculate their success chance. Construct a list of teams for each mission
    # that maximizes success chance.
    for m in missions:
        print 'Mission: ' + m.name
        successList = []
        for c in combinations(followers,m.slots):
            successList.append((m.success(c),c))
        successList = sorted(successList, reverse=True)
        for t in successList[:min(numCombs,len(successList))]:
            print str(t[0]) + ' ' + str(t[1])
        print
        if len(successList) > 0:
            missionTeams = [set([member for member in successList[0][1]])]
            for t in successList[1:]:
                if t[0] >= 1 or t[0] == successList[0][0]:
                    missionTeams.append(set([member for member in t[1]]))
            teams.append(missionTeams)
        else:
            print 'No teams were found. Do you have less than ' + str(m.slots) + ' followers?'
            
    successList = None
    missionTeams = None
    
    # Sort missions by how many teams can maximize success chance for more
    # efficient optimization.
    teams = sorted(teams, key=lambda t: len(t))
    bnbcounter = 0
    # Optimization to find the minimal set of followers that maximizes success
    # for every mission. There may be duplicates.
    sm = followerBnB(teams)
    totalCombinations = 1
    for m in teams:
        totalCombinations *= len(m)
    print 'Branch and Bound Optimization completed after considering ' + \
          str(bnbcounter) + ' complete and incomplete combinations out of ' + \
          'a total of ' + str(totalCombinations) + '.'
    print 'Minimum team size: ' + str(len(sm[0])) + '.'
    
    smallestTeams = []
    # Removing duplicate sets of followers.
    for i in sm:
        if not i in smallestTeams:
            smallestTeams.append(i)
    sm = None
    
    for i in smallestTeams:
        print 'Team: ' + str(tuple(i))
