from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import xlrd
import random
import numpy

author = 'Danlin Chen'

doc = """
match with previous 3 players and multiply 150 ECUs with the outcome 
"""


class Constants(BaseConstants):
    name_in_url = 'M3_die_match_RET'
    players_per_group = 4
    num_rounds = 10
    
    thrown = [1,2,3,4,5,6]
    reward = [c(100),c(200),c(300),c(400),c(500),c(600)]
    file_location1 = "_static/data/OldData_tax.xlsx"

    prob = 0

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()
        if self.round_number == 1:
            workbook1 = xlrd.open_workbook(Constants.file_location1)
            sheet1 = workbook1.sheet_by_name('Module2')
            x1 = []
            groups = [[], [], [], [], [], [], [], [], [], []]
            for value in sheet1.col_values(9):
                if isinstance(value, float):
                    x1.append(int(value))
            print("x1: ", x1)
            index = 0
            while index < len(x1):
                groups[int(index/48)].append(sorted([x1[index], x1[index+1], x1[index+2], x1[index+3]]))
                index += 4

            for p in self.get_players():
                p.participant.vars['data'] = sorted(x1)
                p.participant.vars['groups'] = groups
                p.participant.vars['dices'] = [random.randint(1,6) for i in range(0, 10)]
                p.participant.vars['all_m2_payoff'] = []
                p.participant.vars['m2_payoff'] = 0
                p.participant.vars['matched_outcomes'] = []
                p.participant.vars['all_declare_gain'] = []


class Group(BaseGroup):

    def set_groupAmount(self, round):
        tot = sum([p.participant.vars['all_declare_gain'][round-1] for p in self.get_players()])
        return tot/Constants.players_per_group

    def set_payoff(self):
        for p in self.get_players():
            p.payoff = 0
        dice_sort = [[p, p.real_die_value] for p in self.get_players()]
        dice_sort = sorted(dice_sort, key=lambda x:x[1])
        player_sorted = [0,0,0,0]
        p1_index = 0
        p2_index = 1
        p3_index = 2
        p4_index = 3

        if dice_sort[0][1] == dice_sort[1][1] and random.randint(0,1): # flip with p2
            temp = p1_index
            p1_index = p2_index
            p2_index= temp
        if dice_sort[0][1] == dice_sort[2][1] and random.randint(0,1): # flip with p3
            temp = p1_index
            p1_index = p3_index
            p3_index = temp
        if dice_sort[0][1] == dice_sort[3][1] and random.randint(0,1): # flip with p4
            temp = p1_index
            p1_index = p4_index
            p4_index = temp
        if dice_sort[1][1] == dice_sort[2][1] and random.randint(0,1): # p2 and p3 flip
            temp = p2_index
            p2_index = p3_index
            p3_index = temp
        if dice_sort[1][1] == dice_sort[3][1] and random.randint(0,1): # p2 and p4 flip
            temp = p2_index
            p2_index = p4_index
            p4_index = temp
        if dice_sort[2][1] == dice_sort[3][1] and random.randint(0,1): # p3 and p4 flip
            temp = p3_index
            p3_index = p4_index
            p4_index = temp

        player_sorted[p1_index] = dice_sort[0][0]
        player_sorted[p2_index] = dice_sort[1][0]
        player_sorted[p3_index] = dice_sort[2][0]
        player_sorted[p4_index] = dice_sort[3][0]

        round_groups = player_sorted[0].participant.vars['groups'][self.round_number-1]
        cur_group = random.sample(round_groups, 1)[0]

        # set matched level & matched payoff
        player_sorted[0].matched_level = '4th'
        player_sorted[1].matched_level = '3rd'
        player_sorted[2].matched_level = '2nd'
        player_sorted[3].matched_level = '1st'

        for i in range(0,Constants.players_per_group):
            cur_player = player_sorted[i]
            cur_player.matched_payoff = 150 * cur_group[i]
            cur_player.participant.vars['matched_outcomes'].append(cur_player.matched_payoff)



        print([[p, p.payoff, p.real_die_value] for p in player_sorted])



class Player(BasePlayer):
    real_die_value = models.IntegerField() # virtual dice value report
    chosen_round = models.IntegerField()

    matched_payoff = models.IntegerField()
    matched_level = models.StringField()

    declare_gain = models.IntegerField()

    def roll_die(self):
        self.real_die_value = random.randint(1,6)
        print(self.real_die_value)

    def set_final_payoff(self):
        self.chosen_round = random.randint(1, Constants.num_rounds)
        groupAmount = self.group.set_groupAmount(self.chosen_round)
        self.payoff = c(self.participant.vars['matched_outcomes'][self.chosen_round-1] - self.participant.vars['all_declare_gain'][self.chosen_round-1]*0.1 + groupAmount)
        self.participant.vars['m2_payoff'] = self.payoff
        print("set final: ", self.matched_level, self.payoff, self.participant.vars['matched_outcomes'] )
