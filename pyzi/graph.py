import random

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.missing_pairs = []

    def add_node(self, character, pinyin, meaning, _class):
        if character not in self.adjacency_list:
            self.adjacency_list[character] = {
                'character': character,
                'pinyin': pinyin,
                'meaning': meaning,
                'class': _class,
                'compound': [],
                'neighbors': [],
            }

    # FIXME: return True or False, do not put missing_pairs here, but inside parser
    def add_edge(self, from_character, to_character):
        if from_character in self.adjacency_list and to_character in self.adjacency_list:
            self.adjacency_list[to_character]['neighbors'].append(from_character)
            self.adjacency_list[from_character]['compound'].append(to_character)
        else:
            if not self.missing_pairs.count([from_character, to_character]):
                self.missing_pairs.append([from_character, to_character])
            else:
                # print("Missing edge:", [from_character, to_character])
                pass

    def get_neighbors(self, character):
        return self.adjacency_list.get(character, {}).get('neighbors', [])

    def get_options(self, node):
        opts = [node]
        for i in range(0, 3):
            try:
                r = self.get_random()
                while r in opts:
                    r = self.get_random()
                opts.append(r)
            except:
                raise ValueError("Deus nos abandonou")

        return [d['meaning'] for d in opts if 'meaning' in d]
    
    def get_random(self, character=None):
        fallback = ["手", "口", "人", "水", "木"]
       
        if not character:
            node = random.choice(fallback)
            return self.get_random(node)
        
        neighbors = self.adjacency_list.get(character, {}).get('neighbors', [])
    
        if not neighbors:
            node = random.choice(fallback)
            return self.get_random(node)

        random_neighbor = random.choice(self.adjacency_list.get(character, {}).get('neighbors', []))
        return self.get_node(random_neighbor)

    def get_node(self, character):
        query = self.adjacency_list.get(character, {})
        if not query:
            raise ValueError("Character queried is not in graph")
        return query

    def __str__(self):
        return {char: {
            'character': info['character'],
            'pinyin': info['pinyin'],
            'meaning': info['meaning'],
            'class': info['class'],
            'neighbors': info['neighbors']
        } for char, info in self.adjacency_list.items()}
