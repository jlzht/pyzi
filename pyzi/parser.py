import csv
import json

import os

from .graph import Graph

class Parser:
    LEVELDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'level.json')
    GRAPHDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'game.csv')
    
    @staticmethod
    def load_graph():
        graph = Graph()
        with open(Parser.GRAPHDATA_DIR, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                graph.add_node(row[0], row[2], row[3], row[4])
                for i in row[1]:
                    if not row[0] == i:
                        graph.add_edge(row[0],i)
            for i in graph.missing_pairs:
                graph.add_edge(i[0],i[1])
        return graph

    @staticmethod
    def load_levels():
        with open(Parser.LEVELDATA_DIR, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

        levels = []
        for level in data:
            levels.append([level.get("level"), level.get("original"), level.get("saved"), [level.get("cursor")]])
        return levels

    @staticmethod
    def save_levels(levels):
        data = []
        for level in levels:
            data.append({
                'level': level[0],
                'original': level[1],
                'saved': level[2],
                'cursor': level[3][0]
            })
        
        with open(Parser.LEVELDATA_DIR, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
