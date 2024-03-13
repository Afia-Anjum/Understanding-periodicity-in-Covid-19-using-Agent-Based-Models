from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import random
import math
from bokeh.models import Button
from mesa.time import StagedActivation
from mesa.time import BaseScheduler 
from mesa.time import SimultaneousActivation
import time

class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """
    
    '''
    height=100, width=100, agent_density=1000, infected_density=5, infectious_percentage=6, days_to_recover=10, isolating=True, day_of_week=0, steps_to_move=2, step_amount=0
    '''

    def __init__(self, pos, model, agent_type, agent_age_type,agent_disease_type,weekly_total_movement,movement_probability,infection_day_number,agent_incubation_period):
        """
         Create a new Schelling agent.
         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
            age: Indicator for agent's age
            
            Agent Type:
            0->uninfected and so cannot spread; but suscetible to infection
            1->recovered and immune to reinfection ; also cannot spread
            2->infected(covid+ve) but non-spreader [due to isolation]
            3->infected(covid+ve) and spreader [not maintaining]
            4->asymptomatic (covid+ve and did not appear for test) and spreader
            5->asymptomatic (covid+ve and did not appear for test) and non-spreader [due to isolation]
            6->symptomatic (covid+ve and did not appear for test) and spreader [suspected but not maintaining self quarantine]
            7->symptomatic (covid+ve and did not appear for test) and non-spreader [suspected and self quarantined themeselves]
            8->infected and then died, thus initially spreader and then becomes non-spreader
            9->agent who are dying due to other complications[except covid] and are no longer taking part in spreading
            10-> barriers
            11-> vaccinated
            
            Agent Age Type:
            0-> population aging from 0-20
            1-> population aging from 20-40
            2-> population aging from 40-60
            3-> population aging >60
            4->barriers
            
            External complications(disease):
            0->only smoke
            1->only diabetes
            2->diabetes+hypertension
            3->hypertension+obesity
            4->only malnutrition
            5->healthy
            6->barriers
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.age=agent_age_type
        self.disease=agent_disease_type
        self.move_ooporunity=weekly_total_movement
        self.prob_move=movement_probability
        self.agent_infection_interval=infection_day_number # to calculate the recovery interval/time period
        self.agent_incubation_period=agent_incubation_period # to calculate the incubation period
        
    def step(self):
        
        # Agents step function
        #if self.gets_killed():
        #    self.model.kill_agents.append(self)
        similar = 0
        recovery_chance=0.1 #out of the people who are infected, 0.7 is the probability that one would recover
        death_chance=0.01  #out of the people who are infected, 0.2 is the probability that one would die due to the infection
        #tune the parameters
        infection_chance=0.65 #out of the people who are susceptible, 0.6 is the probability that one would get infected
        normal_death_chance=0.01
                
        ##for barrier 
        #recovery_interval=25
        
        recovery_interval=15
        
        '''
        ##for barrier 
        if self.model.schedule.steps>=14:
            recovery_interval=30
        
        '''
        
        #print(self.pos)
        
        '''
        #variation in the proportions with different disease and age type
        if self.age==0:
            recovery_chance=0.85
            death_chance=0.002
            infection_chance=0.25
        
        if self.age==1:
            recovery_chance=0.6
            death_chance=0.002
            infection_chance=0.55
        
        if self.age==2:
            recovery_chance=0.50
            death_chance=0.002
            infection_chance=0.55
        
        if self.age==3:
            recovery_chance=0.3
            death_chance=0.02
            infection_chance=0.6
            
        '''
        
        #introduce new strain
        

        #print(len(self.model.agents))
        
        #for p in range(len(self.model.agents)):
        #    print(self.model.agents[p].type)
        #    print(self.model.agents[p].pos)
        
        #for neighbor in self.model.grid.neighbor_iter(self.pos):
        #    print(neighbor.type)
            
        #main concept:
        # an agent will only get infected by it's affected spreader neigbours.
        #he can't get the infection from people gone into isolation/quarantine and/or from people dying from covid or having a normal death
        #he can remain in his initial agent type as well. 
        # in the last two scenario, he will just move. 
        
        #resistance gain depend korbe agent age type & agent disease type er upore
        #print("I am type:")
        #print(self.type)
        
        week_day_number=(self.model.schedule.steps % 7)+1
        
        
        daily_move=0
        
        if week_day_number==6 or week_day_number==7:
            agents_movement_probability=-0.2
            daily_move=random.randint(0,2)  #2 moves on weekends
        else:
            agents_movement_probability=0.5
            
            #only for barrier
            daily_move=random.randint(0,20)  #0-20 moves on weekdays
        
        
        if self.type==3 or self.type==4 or self.type==6 or self.type==2 or self.type==5 or self.type==7:
            self.agent_infection_interval=self.agent_infection_interval+1
            
        
        initial_type=self.type
        flag=0
        #iterating over the number of moves within each time step
        for d in range(daily_move):
            if self.type==9 or self.type==8:
                break
            
            neigbour_infected=0
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if self.type==0 and (neighbor.type == 3 or neighbor.type == 4 or neighbor.type == 6):  #infected and can spread infection
                    neigbour_infected=1
                    break
            
            
            if neigbour_infected: 
                #self.agent_infection_interval=self.agent_infection_interval+1
                dice_roll=random.uniform(0,1)
                dice_roll2=random.uniform(0,1)
                #if dice_roll < infection_chance:
                if dice_roll + agents_movement_probability <= infection_chance:
                    incub=random.randint(1,3)
                    
                    #this person got in contact with infected person and also passed the dice roll, his infection
                    #interval should also get started 
                    if flag==0:
                        self.agent_infection_interval=self.agent_infection_interval+1
                    
                    #print("Printing incubation:"+str(incub))
                    #print("Printing infection interval:"+str(self.agent_infection_interval))
                    
                    if self.agent_infection_interval>=incub: #and dice_roll < infection_chance: 
                    #if dice_roll  >= infection_chance:
                        num=[2,3,4,5,6,7]
                        
                        random.shuffle(num)
                        self.type=num[0]
                        flag=1
                
                
                #possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
                possible_steps=self.model.get_real_neighbours(self.pos) #UPTO 1 step of neigbours,
                
                new_position=self.random.choice(possible_steps)
                
                cnt=0
                while not (self.model.grid.is_cell_empty(new_position)):
                    #if cnt>12:
                    if cnt>4:
                        break
                    new_position=self.random.choice(possible_steps)
                    cnt+=1
                    
                if self.model.grid.is_cell_empty(new_position):
                    self.model.grid.move_agent(self, new_position)
            
                ##self.model.grid.move_to_empty(self)
                #break
                
        
            elif self.type==0 or self.type==1:
                
                #!!model normal_death model for these agents
                possible_steps=self.model.get_real_neighbours(self.pos)
                new_position=self.random.choice(possible_steps)
                cnt=0
                while not (self.model.grid.is_cell_empty(new_position)):
                    #if cnt>12:
                    if cnt>8:
                        break
                    new_position=self.random.choice(possible_steps)
                    cnt+=1
            
                if self.model.grid.is_cell_empty(new_position):
                    self.model.grid.move_agent(self, new_position)
        
            elif self.type==2 or self.type==5 or self.type==7: 
                #self.agent_infection_interval=self.agent_infection_interval+1
                
                dice_roll=random.uniform(0,1)
                if self.agent_infection_interval>=recovery_interval:
                    if dice_roll > recovery_chance: 
                        self.type=1
                    elif dice_roll < death_chance:
                        self.type=8
                    else:
                        num=[2,5,7]
                        random.shuffle(num)
                        self.type=num[0]
                else:
                    num=[2,5,7]
                    random.shuffle(num)
                    self.type=num[0]
                
        
        
            elif self.type==3 or self.type==4 or self.type==6:
                #self.agent_infection_interval=self.agent_infection_interval+1
                
                dice_roll=random.uniform(0,1)
                if self.agent_infection_interval>=recovery_interval:
                    if dice_roll > recovery_chance: 
                        self.type=1
                    elif dice_roll < death_chance:
                        self.type=8
                    else:
                        num=[3,4,6]
                        random.shuffle(num)
                        self.type=num[0]
                else:
                    num=[3,4,6]
                    random.shuffle(num)
                    self.type=num[0]
                        
                possible_steps=self.model.get_real_neighbours(self.pos)
                new_position=self.random.choice(possible_steps)
                
                cnt=0
                while not (self.model.grid.is_cell_empty(new_position)):
                    if cnt>4:
                        #if cnt>12:
                        break
                    new_position=self.random.choice(possible_steps)
                    cnt+=1
                if self.model.grid.is_cell_empty(new_position):
                    self.model.grid.move_agent(self, new_position)    
                    #self.model.grid.move_agent(self, new_position)
                    #break
        

        if self.type!=initial_type:
                    
            if (self.type==2 or self.type==5 or self.type==7) and (initial_type==2 or initial_type==5 or initial_type==7):
                return 
            if (self.type==3 or self.type==4 or self.type==6) and (initial_type==3 or initial_type==4 or initial_type==6):
                return 
                
            if self.type==1:
                self.model.resistance_gain += 1
                
            elif self.type==8:
                self.model.covid_death += 1
            
                        
            elif self.type==9:
                self.model.normal_death += 1
                self.model.susceptible =self.model.susceptible - 1
            elif self.type==2 or self.type==3 or self.type==4 or self.type==5 or self.type==6 or self.type==7:
                #if self.agent_infection_interval>=incub:
                self.model.susceptible =self.model.susceptible - 1
                self.model.infected =self.model.infected + 1
                #self.model.current_infections=self.model.current_infections-1
        
        
cnt=0

class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """
    #400 cells area-> 320 cells people, 30 cells(lakes,jungle, forest, etc.); 50 cells are empty
    #out of 320 cells people-> agent_age,agent_disease, agent_type
    def __init__(self, height=100, width=100, density=0.1,initial_outbreak=0.01,non_accesible_area_density=0.075,agent_type_pcs=[.99, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0],agent_age_type_pcs=[0.05,0.4,0.05,0.5],agent_disease_type_pcs=[0.25,0.07,0.22,0.24,0.08,0.14],social_distancing=False):
        """
        """
        
        self.height = height
        self.width = width
        self.density = density
        self.initial_outbreak = initial_outbreak
        
        #print("Printing: initialoutbreak:"+str(self.initial_outbreak))
        
        self.agent_type_pcs = agent_type_pcs
        self.agent_age_type_pcs = agent_age_type_pcs
        self.agent_disease_type_pcs = agent_disease_type_pcs
        self.non_accesible_area_density = non_accesible_area_density
        self.schedule = RandomActivation(self)
        #self.schedule = StagedActivation(self)
        #self.schedule = BaseScheduler(self)
        #self.schedule =SimultaneousActivation(self)
        self.grid = SingleGrid(width, height, torus=True)
        self.social_distancing=social_distancing
        self.kill_agents = []
        
        #self.agent_type_pcs[3]=initial_outbreak
        
        #self.agent_type_pcs[0]=1-initial_outbreak
        
        self.resistance_gain = 0
        self.covid_death=0
        #self.susceptible=int(self.height * self.width * self.density*self.agent_type_pcs[0])
        #self.infected=int(self.height * self.width * self.density)-self.susceptible
        
        g=abs(int(self.height * self.width * self.density*self.initial_outbreak)-(self.height * self.width * self.density*self.initial_outbreak))

        if g<=0.5:
            self.infected=math.floor(self.height * self.width * self.density*self.initial_outbreak)
        else:
            self.infected=math.ceil(self.height * self.width * self.density*self.initial_outbreak)
        
        #self.infected=self.height * self.width * self.density*self.initial_outbreak
        #print("Printing g:")
        #print(self.infected)
            
        #self.infected=int(self.height * self.width * self.density*self.initial_outbreak)  
        self.susceptible=int((self.height * self.width * self.density)-self.infected)
        
        #self.vaccinated=int((self.height * self.width * self.density*self.agent_type_pcs[10]))
        
        #everyday, two percent of the population should get vaccinated
        #self.daily_vaccination=int((self.height * self.width * self.density))*0.02
        
        #daily vaccination rate for canada
        #0.34% weekly, 0.05% 
        self.daily_vaccination=int((self.height * self.width * self.density))*0.0005
        
        g=abs(int((self.height * self.width * self.density)-self.infected)-((self.height * self.width * self.density)-self.infected))
        if g<=0.5:
            self.susceptible=math.floor((self.height * self.width * self.density)-self.infected)
        else:
            self.susceptible=math.ceil((self.height * self.width * self.density)-self.infected)
        
        

        self.normal_death=0

        self.newly_infected=self.infected
        
        self.datacollector = DataCollector(
            {"resistance_gain": "resistance_gain","covid_death": "covid_death","infected": "infected","susceptible": "susceptible","social_distancing":"social_distancing","newly_infected":"newly_infected"},  
            # Model-level count of different number of agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        
        total_agents = math.ceil(self.height * self.width * self.density)
        #print(total_agents)
        #barrier_cells=self.height * self.width *self.non_accesible_area_density
        agents_by_type = [total_agents*val for val in self.agent_type_pcs]
        agents_by_age_type = [total_agents*val for val in self.agent_age_type_pcs]
        agents_by_disease_type = [total_agents*val for val in self.agent_disease_type_pcs]

        
        self.agents = []
        
        self.cnt=0
        
        '''
        #removing the single barrier
        
        #single barrier
        x1=50
        y1=0
        
        while (y1<=99):
            pos1=(x1,y1)
            #print(pos1)
            agent1 = SchellingAgent((x1, y1), self, 10,0,0,0,0,0,0)
            self.grid.place_agent(agent1, pos1)
            #self.schedule.add(agent1)
            #self.agents.append(agent1)
            if y1>=20 and y1<=80:
                #place your condition here and check what happens:
                self.kill_agents.append(agent1)
                #self.kill_agents.append(pos1)
            y1=y1+1
        
        '''
        
        
        infect=0
        
        #set up all the agents 
        types=len(self.agent_type_pcs)
        for i in range(types):
            if i==3 or i==4 or i==6:
                #total_agents1=int(total_agents*self.initial_outbreak)
                #infect=infect+total_agents1
                total_agents1=total_agents
            else:
                total_agents1=total_agents
            #pos = self.grid.find_empty()
            #print(pos)
            for j in range(len(self.agent_age_type_pcs)):
                type1=total_agents1*self.agent_type_pcs[i]*self.agent_age_type_pcs[j]
                #print(type1)
                if abs(type1-int(type1)) <=0.5:
                    #take floor
                    type_1=math.floor(type1)
                else:
                    type_1=math.ceil(type1)
                #print(type_1)
                #for k in range(type_1):
                for l in range(len(self.agent_disease_type_pcs)):
                    type2=type_1*self.agent_disease_type_pcs[l]
                    if abs(type2-int(type2)) <=0.5:
                        type_2=math.floor(type2)
                    else:
                        type_2=math.ceil(type2)
                    
                    for m in range(type_2):
                        move_prob=random.uniform(0,1)
                        #move_opportunity=random.randint(200,800)
                        move_opportunity=random.randint(0,200)
                        
                        #ONLY FOR BARRIER
                        '''
                        if i==3:
                            #print("printing position:")
                            pos = self.grid.find_empty()
                            while not pos[0]<=49:
                                pos = self.grid.find_empty()
                                #print(pos)
                        else:
                            pos = self.grid.find_empty()
                        #print(pos)
                        '''
                        #if barrier is applied, comment out this line:
                        pos = self.grid.find_empty()
                        
                        if i==3:
                            infection_day_number=random.randint(1,3)
                            #infection_day_number=1
                            incubation_day_number=0
                        else:
                            infection_day_number=0
                            incubation_day_number=0
                        agent = SchellingAgent(pos, self, i,j,l,move_opportunity,move_prob,infection_day_number,incubation_day_number)
                        #self.grid.position_agent(agent, pos)
                        self.grid.place_agent(agent, pos)
                        self.schedule.add(agent)
                        self.agents.append(agent)
        
        self.running = True
        self.datacollector.collect(self)
    
    def eucledean_distance(self, x1,x2,y1,y2,w,h):
        # http://stackoverflow.com/questions/2123947/calculate-distance-between-two-x-y-coordinates
        return math.sqrt(min(abs(x1 - x2), w - abs(x1 - x2)) ** 2 + min(abs(y1 - y2), h - abs(y1-y2)) ** 2)
    
    def sort_neighborhood_by_distance(self, from_pos, neighbor_spots):
        from_x, from_y = from_pos
        return sorted(neighbor_spots, key = lambda spot: self.eucledean_distance(from_x, spot[0], from_y, spot[1], self.grid.width, self.grid.height))

    
    def find_nearest_empty(self, pos, neighborhood):
        nearest_empty = None
        sorted_spots = self.sort_neighborhood_by_distance(pos, neighborhood)
        index = 0
        while (nearest_empty is None and index < len(sorted_spots)):
            if self.grid.is_cell_empty(sorted_spots[index]):
                nearest_empty = sorted_spots[index]
            index += 1
        return nearest_empty
    
    def get_real_neighbours(self,pos):
        x=pos[0]
        y=pos[1]
        neighbour_list=[]
        real_neighbour_list=[]
        
        #first boundary circulating the current position : 8 spots
        neighbour_list.append((x+1,y))
        neighbour_list.append((x+1,y+1))
        neighbour_list.append((x,y+1))
        neighbour_list.append((x-1,y+1))
        neighbour_list.append((x-1,y))
        neighbour_list.append((x-1,y-1))
        neighbour_list.append((x,y-1))
        neighbour_list.append((x+1,y-1))
        
        
        
        #only for barrier
        '''
        if self.social_distancing==True:
            #neighbour_list = [m for m in neighbour_list if not m[0] == 50 and (m[1] >= 20 or m[1]<=75)]
            neighbour_list = [m for m in neighbour_list if not (m[0] == 50 and (m[1] >= 0 or m[1]<=99))]
        if self.social_distancing==False:
            neighbour_list = [m for m in neighbour_list if not (m[0] == 50 and (m[1] >= 75 or m[1]<=20))]
        
        
        '''
        
        #print(neighbour_list)
        #if neighbour_list
        #50,20 --50,75
        
        
        # so that neighbour does not go out of boundary
        
        i=0
        for (x,y) in neighbour_list:
            if x<0 or x>self.width-1 or y<0 or y>self.height-1:
                i+=1
                pass
            else:
                real_neighbour_list.append(neighbour_list[i])
                i+=1
        return real_neighbour_list
        
    
    
    def step(self):
        """
        Run one step of the model. If All agents are achieves resitance to covid-19, then halt the model.
        """
        '''
        terminating condition would be: death plus people who gained resistance==total no of agents.
        '''
        
        # Reset counter of agents at each step
        #self.resistance_gain = 0  
        #self.covid_death=0
        #self.infected=0
        #self.normal_death=0
        #self.susceptible=0
        
        prev_infected=self.infected
        #print(self.susceptible)
        print("Printing the variables in each step:\n")
        print("number of day: "+str((self.schedule.steps % 7)+1))
        
        
        #print(len(self.agents))
        #print(self.susceptible)
        
        #vaccination 2 percent each day
        '''
        #if len(self.agents)>=20:
        if self.susceptible>=20:
            chosen_agents=[]
            for i in range(0,20):
                rand_agent=random.choice(self.agents)
                while rand_agent.type!=0: #or rand_agent.type!=1:
                    rand_agent=random.choice(self.agents)
                chosen_agents.append(rand_agent)
                chosen_agents[i].type=11
        
            self.agents = list(set(self.agents) - set(chosen_agents))
            self.susceptible=self.susceptible-len(chosen_agents)
        
        print(len(self.agents))
        
        '''
        
        
        ###VACCINATION
        
        '''
        
        #vaccination 0.34 percent weekly , 0.05 percent each day, which means (0.05/100)*1000=0.5 ~= 1
        
        if (self.schedule.steps+1)%2==0:
            if len(self.agents)>=1:
                #if self.susceptible>=4:
                chosen_agents=[]
                #for i in range(0,4):
                rand_agent=random.choice(self.agents)
                while rand_agent.type==8 or rand_agent.type==9:
                    rand_agent=random.choice(self.agents)
                    #chosen_agents.append(rand_agent)
                rand_agent.type=11
                            
                self.agents = list(set(self.agents) - set(chosen_agents))
                self.susceptible=self.susceptible-len(chosen_agents)
                            
                print(len(self.agents))
        
        '''
        
        #print(len(chosen_agents))
        
        print(self.infected)
        print(self.susceptible)
        print(self.covid_death)
        print(self.resistance_gain)
        print(self.normal_death)
        
        self.schedule.step()
        
        cumulative_infected=self.infected
        
        print(cumulative_infected)
        
        #for tracking the daily new number of infections 
        self.newly_infected=cumulative_infected-prev_infected
        
        
        #global cnt 
        
        '''
        ##REPORTING ARTIFACT #large bump on Mondays
        if ((self.schedule.steps % 7)+1)==6:
            #cnt+=self.newly_infected
            self.cnt+=self.newly_infected
            self.newly_infected=0
        if ((self.schedule.steps % 7)+1)==7:
            #cnt+=self.newly_infected
            self.cnt+=self.newly_infected
            self.newly_infected=0        
        if ((self.schedule.steps % 7)+1)==1:
            #self.newly_infected=self.newly_infected+cnt
            self.newly_infected=self.newly_infected+self.cnt
        
        '''
        
        ##testing ARTIFACT #biweekly
        if ((self.schedule.steps % 7)+1)==1 or ((self.schedule.steps % 7)+1)==2 or ((self.schedule.steps % 7)+1)==4 or ((self.schedule.steps % 7)+1)==5 or ((self.schedule.steps % 7)+1)==7:
            #cnt+=self.newly_infected
            self.cnt+=self.newly_infected
            self.newly_infected=0 
        if ((self.schedule.steps % 7)+1)==3 or ((self.schedule.steps % 7)+1)==6:
            #self.newly_infected=self.newly_infected+cnt
            self.newly_infected=self.newly_infected+self.cnt
        print("Printing cnt:")
        print(cnt)
        
        #print(len(self.kill_agents)) 5 ashtese, no problem
        
        # collect data and determine the number of agent acquired resistance or are dead, susceptible or infected
        self.datacollector.collect(self)
        
        #print(self.infected)
        
        '''
        ##for barrier
        if self.schedule.steps>=14:
            self.social_distancing=False
        '''
            
        #print("Printing social distancing:")
        #print(self.social_distancing)
        
        if not self.social_distancing:
            for i in range(len(self.kill_agents)):
                vai=self.kill_agents[i]
                #print(vai)
                self.grid.remove_agent(vai)
            self.kill_agents=[]
        
        
        '''
        count=0
        for agent in self.schedule.agent_buffer(shuffled=False):
            print(agent)
            count+=1
        print("Total no of agents in the buffer are:")
        print(count)
        '''
        
        #self.resistance_gain=0
        #self.covid_death=0
        #self.infected=0
        #self.normal_death=0
        #self.susceptible=0
        
        count_all=self.resistance_gain+self.covid_death
        #self.running=True
        if cumulative_infected==count_all+2:
        #can do
        #if abs(cumulative_infected-count_all) <5:
        #if self.schedule.get_agent_count()==count_all:
            self.running = False
        #if self.susceptible<20:
        #    self.running = False
