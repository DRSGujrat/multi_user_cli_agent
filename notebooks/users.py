from dataclasses import dataclass, field
class User:
    def __init__(self,user_id:str,memory = None):
        self.user_id = user_id
        self.memory = memory or list()
        self.profile = UserProfile()
        self.summary = list()
@dataclass
class UserProfile:
    
    goals: list = field(default_factory=list)
    preferences: list = field(default_factory=list)
    likes: list = field(default_factory=list)
    dislikes : list = field(default_factory=list)
    hobbies: list = field(default_factory=list)
    projects: list = field(default_factory= list)
    skills: list = field(default_factory = list)
    def to_prompt(self):
        return f""" User prefers {self.preferences} ,
        user goals are {self.goals}, 
        interests of user are {self.likes},
        hobbies of user are {self.hobbies}, 
        the user does not like{self.dislikes}, the user is working on {self.projects} and the current skills of user are{self.skills}"""
        
class UserManager:
    def __init__(self):
        self.users = dict()
    
    def get_user_summary(self,user_id):
        if len(self.users[user_id].summary) > 0:
            return self.users[user_id].summary[-1]
        else:
            return list()
            
    def get_user_profile(self,user_id):
        if self.is_user_present(user_id):
            return self.get_user_object(user_id).profile

        print("User not present")        
        
        
    def create_user(self,user_id):
        if self.is_user_present(user_id):
            print("User already there")
            return
        u = User(user_id)
        self.users[user_id] = u
        print("New User Created")
    
    def append_memory_message(self,user_id,message : str):
        u = self.users[user_id]
        u.memory.append(message)
        
    def append_all_user_memory_message(self,message:str):
        for user_obj in self.users.values():
            user_obj.memory.append(message)
    
    def append_memory_message_list(self,user_id,message_list : list):
        u = self.users[user_id]
        u.memory = u.memory + message_list
        
    
    def display_every_user(self):
        if not self.users:
            print("No users present")
            return 
        users = self.users.keys()

        for i in users:
            print(i)
        
    def is_user_present(self,user_id:str) -> bool:
        return user_id in self.users
                
    def get_user_object(self,user_id:str):
        if self.is_user_present(user_id):
            return self.users[user_id]
        print("User not present")
        
    def delete_user(self,user_id:str):
        if user_id in self.users:
            del self.users[user_id]
        print("User Deleted")
        
    def get_user_memory(self,user_id:str):
        if self.is_user_present(user_id):
            return self.users[user_id].memory
        return None
    
    def delete_user_memory(self,user_id:str):
        if user_id not in self.users:
            print("User does not exist")
            return 
        memory = self.get_user_memory(user_id)
        memory.clear()
        print("Memory Cleared")
        
    def display_every_user_memory(self):
        for user,objects in self.users.items():
            print(f"{user} : {objects.memory}")   
    
    def delete_every_user(self):
        if not self.users:
            print("No users present")
            return
        self.users.clear()
        print("All users deleted")
        
    def delete_every_user_memory(self,):
        for user in self.users.keys():
            memory = self.get_user_memory(user)
            memory.clear()
        print("Memory for all Users Cleared")
    
        
        