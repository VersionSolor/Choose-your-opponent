# import libraries
from bs4 import BeautifulSoup
import urllib3
import numpy as np

# class gathering team data
class Team:
    def __init__(self, name, elo, nationality=0, group=0, group_rank=0, point=0, goal_difference=0, goal_for=0, competition_rank=1):
        self.name = name
        self.elo = elo
        self.nationality = nationality
        self.group = group
        self.group_rank = group_rank
        self.point = point
        self.goal_difference = goal_difference
        self.goal_for = goal_for
        self.competition_rank = competition_rank
    
    #finir methode str mais pas super utile pour linstant
    def __str__(self):
        print(self.name + " " + self.elo)

    def set_name(self, name):
        self.name = name

    def set_elo(self, elo):
        self.elo = elo
        
    def set_nationality(self, nationality):
        self.nationality = nationality

    def set_group(self, group):
        self.group = group
        
    def set_group_rank(self, group_rank):
        self.group_rank = group_rank

    def set_point(self, point):
        self.point = point
        
    def set_goal_diffrence(self, goal_diffrence):
        self.goal_diffrence = goal_diffrence

    def set_goal_for(self, goal_for):
        self.goal_for = goal_for
    
    def set_competition_rank(self, competition_rank):
        self.competition_rank = competition_rank


# functions to generate url
def convert_date_to_string(day, month, year):
    return str(year) + "-" + str(month) + "-" + str(day)


def get_clubelo_url(str_date):
    return "http://clubelo.com/" + str_date + "/Ranking"


# set elos for all teams
def set_elo_from_soup(soup, team_list):
    ranking = soup.find("table", attrs={"class": "ranking"})
    for team in team_list:
        set_elo_from_ranking(ranking, team)


# set elo for one team
def set_elo_from_ranking(ranking, team):
    team_info = ranking.find("a", string=team.name).parent.parent
    # elo is what contain the elo information
    elo = team_info.find("td", attrs={"class": "r"})
    # .string to get  only the elo
    # then we convert into int
    team.set_elo(int(elo.string))

    
# set elos for all teams
def set_nationality_from_soup(soup, team_list):
    ranking = soup.find("table", attrs={"class": "ranking"})
    for team in team_list:
        set_elo_from_ranking(ranking, team)


# set elo for one team
def set_nationality_from_ranking(ranking, team):
    team_info = ranking.find("a", string=team.name).parent.parent
    # nationality is what contain the elo information given by the
    # photo of the flag on our case
    nationlity = team_info.find("img")
    # .string to get  only the elo
    # then we convert into int
    team.set_nationality(nationality.string)

# do what you think it does with elo formulas
def victory_probability_1vs2(team1, team2):
    diff_elo = team1.elo - team2.elo
    return 1 / (10 ** (-diff_elo / 400) + 1)


# set probabilities into a matrix
def fill_victory_matrix(team_list):
    number_of_teams = len(team_list)
    matrix = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        for j in range(i+1, number_of_teams):
            matrix[i][j] = victory_probability_1vs2(team_list[i], team_list[j])
            matrix[j][i] = 1 - matrix[i][j]
    return matrix


def victory_matrix(team_list, day, month, year):
    # specify the url from the date you want
    http = urllib3.PoolManager()

    str_date = convert_date_to_string(day, month, year)
    url = get_clubelo_url(str_date)

    # get page
    response = http.request('GET', url)

    # make it usable
    soup = BeautifulSoup(response.data, "html.parser")

    set_elo_from_soup(soup, team_list)

    return fill_victory_matrix(team_list)

######## Parser on UEFA group site on google ########

def can_1_play_2(team1, team2):
    if(team1.group = team2.group or team1.nationality = team2.nationality):
         return false
    else:
         return true

def fill_playable_match_matrix(team_list):
number_of_teams = len(team_list)
    matrix = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        matrix[i][i] = false
        for j in range(i+1, number_of_teams):
            # symetric matrix
            matrix[i][j] = can_1_play_2(team_list[i], team_list[j])
            matrix[j][i] = matrix[i][j]
    return matrix

def playable_match_matrix(team_list, day, month, year):
    # specify the url from the date you want
    http = urllib3.PoolManager()
    url = get_uefa_group_url(year)

    # get page
    response = http.request('GET', url)

    # make it usable
    soup = BeautifulSoup(response.data, "html.parser")

    set_team_info_from_soup(soup, team_list)

    return fill_playable_match_matrix(team_list)

def compute_competition_ranking(team_list):
    number_of_teams = len(team_list)
    group_winner_list = []
    runner_up_list = []
    # first we compare wether the team has won its group or not
    for i in range(number_of_teams):
        if(team_list[i].group_rank = 1):
              group_winner_list.append(team_list[i])
        else:
            team_list[i].competition_rank = number_of_teams + 1 
            runner_up_list.append(team_list[i])
    # then we start comparing the points of each team to rank them
    compare_point(group_winner_list) 
    compare_point(runner_up_list) 
    # if there are tie cases we compare on Goal Difference
    compare_goal_difference(team_list)
    # if there are tie cases we compare on Goal For
    compare_goal_for(team_list)
    # we then hope that all cases are cleared or we should add 
    # the other decider rules
    
    
# do what it does
def search_tie_case(team_list):   
    return 0
    
# return lists of tie cases
def build_tie_case(team_list):
    return 0
       
# compare team point then add rank to the one with lowest point
def compare_point(team_list):
    number_of_teams = len(team_list)              
    for i in range(number_of_teams):
        for j in range(i+1, number_of_team):
            if(team_list[i].point > team_list[j].point):
                team_list[j] += 1
      
# compare team goal_differebce then add rank to the one with lowest point
def compare_goal_difference(team_list):
    number_of_teams = len(team_list)              
    for i in range(number_of_teams):
        for j in range(i+1, number_of_team):
            if(team_list[i].goal_difference > team_list[j].goal_difference):
                team_list[j] += 1
   
#compare team goal_for then add rank to the one with lowest point
def compare_goal_for(team_list):
    number_of_teams = len(team_list)              
    for i in range(number_of_teams):
        for j in range(i+1, number_of_team):
            if(team_list[i].goal_for > team_list[j].goal_for):
                team_list[j] += 1
                
        
                
