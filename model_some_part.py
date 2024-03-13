# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:26:43 2020

@author: Asus
"""

        initial_type=self.type
        #if self.type==10:
        #    return
        neigbour_infected=0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            #print("Inside:")
            #print(neighbor.type)
            #if self.type==0 and neighbor.type==0:
            #    similar += 1
            if self.type==0 and (neighbor.type == 3 or neighbor.type == 4 or neighbor.type == 6):
                neigbour_infected=1
                break
        
        if neigbour_infected: 
            #self.agent_infection_interval=self.agent_infection_interval+1
            
            dice_roll=random.uniform(0,1)
            dice_roll2=random.uniform(0,1)
            #if dice_roll < infection_chance:
            if dice_roll + agents_movement_probability >= infection_chance:
                num=[2,3,4,5,6,7]
                random.shuffle(num)
                self.type=num[0]
                #self.type=random.randint(2,8)
            elif dice_roll2 < normal_death_chance:
                self.type=9
            else:
                self.type=0
            #possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
            possible_steps=self.model.get_real_neighbours(self.pos) #UPTO 1 step of neigbours,
            #change it upto 3 steps of neigbours
            #in every directions later on
            #print(possible_steps)
            new_position=self.random.choice(possible_steps)
            #print(possible_steps)
            #print(self.pos)
            #print(new_position)
            
            cnt=0
            while not (self.model.grid.is_cell_empty(new_position)):
                #if cnt>12:
                if cnt>4:
                    break
                new_position=self.random.choice(possible_steps)
                cnt+=1
            
            #if cnt>4:
            #    #if cnt>12:
            #    break
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)
            
            ##self.model.grid.move_to_empty(self)
            #break
        
        elif self.type==0 or self.type==1:
                
            #!!model normal_death model for these agents
            
            possible_steps=self.model.get_real_neighbours(self.pos)
            new_position=self.random.choice(possible_steps)
            #print(possible_steps)
            #print(new_position)
            cnt=0
            while not (self.model.grid.is_cell_empty(new_position)):
                #if cnt>12:
                if cnt>8:
                    break
                new_position=self.random.choice(possible_steps)
                cnt+=1
            #if cnt>8:
            ##if cnt>12:
            #    break
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)
            #self.model.grid.move_agent(self, new_position)
            #break
        
        elif self.type==2 or self.type==5 or self.type==7: 
            self.agent_infection_interval=self.agent_infection_interval+1
            
            dice_roll=random.uniform(0,1)
            if dice_roll < recovery_chance and self.agent_infection_interval>=15:
            
            #if dice_roll < recovery_chance:
                self.type=1
            else:
                dice_roll2=random.uniform(0,1)
                if dice_roll2 > death_chance:
                    num=[2,5,7]
                    random.shuffle(num)
                    self.type=num[0]
                else:
                    self.type=8
            """        
            ##self.model.grid.move_to_empty(self)
            #possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
            possible_steps=self.model.get_real_neighbours(self.pos)
            new_position=self.random.choice(possible_steps)
            #print(possible_steps)
            #print(self.pos)
            #print(new_position)
            
            cnt=0
            while not (self.model.grid.is_cell_empty(new_position)):
                if cnt>4:
                #if cnt>12:
                    break
                new_position=self.random.choice(possible_steps)
                cnt+=1
            #print(possible_steps)
            #print(new_position)
            if cnt>4:
            #if cnt>12:
                break
            self.model.grid.move_agent(self, new_position)
            """
            #break
        
        #elif self.type==9:
        #    #self.model.normal_death += 1
        #    #self.model.susceptible =self.model.susceptible- 1
        #    break
        #elif self.type==8:
        #    #self.model.covid_death += 1
        #    break
        
        elif self.type==3 or self.type==4 or self.type==6:
            self.agent_infection_interval=self.agent_infection_interval+1
            
            dice_roll=random.uniform(0,1)
            #if dice_roll < recovery_chance-0.1:
            if dice_roll < recovery_chance and self.agent_infection_interval>=15:
                self.type=1
            else:
                dice_roll2=random.uniform(0,1)
                if dice_roll2 < death_chance:
                    self.type=8
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
            #if cnt>4:    
            ##if cnt>12:
            #    break
            if self.model.grid.is_cell_empty(new_position):
                self.model.grid.move_agent(self, new_position)    
            #self.model.grid.move_agent(self, new_position)
            #break
                
        if self.type!=initial_type:
            
            if (self.type==2 or self.type==5 or self.type==7) and (initial_type==2 or initial_type==5 or initial_type==7):
                return 
            if (self.type==3 or self.type==4 or self.type==6) and (initial_type==3 or initial_type==4 or initial_type==6):
                return 
            
            #print(initial_type)
            #print("Changed type:")
            #print(self.type)
            
            #print(initial_type)
            if self.type==1:
                self.model.resistance_gain += 1
                #self.model.infected =self.model.infected - 1
                #self.model.current_infections=self.model.current_infections-1
                #portrayal["Color"] = "green"
                #resistant, which means it was infected
            elif self.type==8:
                self.model.covid_death += 1
                #self.model.current_infections=self.model.current_infections-1
                #not decreasing from the infected, as we are keeping the cumulative infection
            elif self.type==9:
                self.model.normal_death += 1
                self.model.susceptible =self.model.susceptible - 1
            elif self.type==2 or self.type==3 or self.type==4 or self.type==5 or self.type==6 or self.type==7:
                self.model.susceptible =self.model.susceptible - 1
                self.model.infected =self.model.infected + 1
                #self.model.current_infections=self.model.current_infections-1
