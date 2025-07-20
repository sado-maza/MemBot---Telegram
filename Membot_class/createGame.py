from sql.sqlMemBot import random_phrases

    
#creating a game session
class GameSession:
    def __init__(self):
        self.players = {}                    #tg_id: tg_name
        self.state_game = 'waiting'          #game mode
        self.list_pharese = random_phrases() #list with phrases
        self.votes_received = 0              #number of voters in the round
        self.points = {}                     #tg_id: points
        self.nunber_round=0                  #round number
        self.current_poll_id = None          #poll_id
        self.votes = {}                      #votes_id: votes_index

    
    def next_round(self):
        if self.nunber_round == 10:
            return False
        return True



















