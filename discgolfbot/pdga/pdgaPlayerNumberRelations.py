import json
from .pdgaPlayer import PdgaPlayer
from pathlib import Path
class PdgaPlayerNumberRelations:
    def __init__(self, db_file):
        self.db_file = db_file
        self.pdga_numbers = {}
        self.pdga_players = {}
        self.by_pdga_number = {}
        self.by_discord_id = {}
        self.player_objects = []
        self.load_db()
    
    def add_relation(self, player_object):
        
        self.by_discord_id[player_object.discord_id] = player_object
        self.by_pdga_number[player_object.pdga_number] = player_object
        self.pdga_numbers[player_object.pdga_number] = player_object
        self.pdga_players[player_object.player_name] = player_object
        self.player_objects.append(player_object)
        self.save_relations()

    def load_db(self):
        relations = self.__load_json__()
        if not None == relations:
            
            for rel_obj in relations['by_discord_id']:
                player = relations['by_discord_id'][rel_obj]
                player_object = PdgaPlayer(pdga_number=player['pdga_number'], player_name=player['player_name'], discord_id=player['discord_id'])
                self.add_relation(player_object)

    def __validate_json__(self):
        
        #Path.joinpath(Path.cwd(),  self.db_file)
        try:
            with open(self.db_file, "r") as rf:
                json.load(rf)
        except:
            return False
        return True
        
    def __load_json__(self):

        if self.__validate_json__():
            with open(self.db_file, "r") as readf:
                relations = json.load(readf)
                return relations
        else:
            ## init file
            with open(self.db_file, "w") as writef:
                # p_dict = PdgaPlayer("","","").to_dict()
                # out = [p_dict.copy()] # hvorfor gjorde jeg dette? hmm.. 
                json.dump({},writef)#p_dict, writef)


    def __to_dict__(self):
        return {"by_discord_id": self.by_discord_id.copy(),
        "by_pdga_number": self.by_pdga_number.copy()}
    
    def save_relations(self):
        with open(self.db_file, "w") as writef:
            coll = {'by_discord_id':{},'by_pdga_number':{}}
            for pl_obj in self.player_objects:
                obj = pl_obj.to_dict()
                coll['by_discord_id'][obj['discord_id']] = obj.copy()
                coll['by_pdga_number'][obj['pdga_number']] = obj
            json.dump(coll, writef, indent=6)
