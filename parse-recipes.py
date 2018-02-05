# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:26:01 2018

@author: Saniyah
"""
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import requests

class Ingredient(object):
    def __init__(self, item, quantity = None, measure = None, other = None):
        self.item = item
        self.quantity = quantity
        self.measure = measure
        self.other = other
        
    def __repr__(self):
        if self.quantity == None:
            q = ""
        else:
            q = self.quantity
        if self.measure == None:
            m = ""
        else:
            m = self.measure
        if self.item == None:
            i = ""
        else:
            i = self.item
        s = str(q) + " " + str(m) + " " + str(i)
        return s
    
    def __hash__(self):
        return hash(self.item)
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.item == other.item
    
    def __ne__(self, other):
        return not isinstance(other, self.__class__) or not self.item == other.item
    
    def __lt__(self, other):
        if self.item == other.item:
            return self.quantity < other.quantity
        else:
            return self.item < other.item
        
    def __le__(self, other):
        if self.item == other.item:
            return self.quantity <= other.quantity
        else:
            return self.item <= other.item

    def __gt__(self, other):
        if self.item == other.item:
            return self.quantity > other.quantity
        else:
            return self.item > other.item 
        
    def __ge__(self, other):
        if self.item == other.item:
            return self.quantity >= other.quantity
        else:
            return self.item >= other.item    

# define a recipe object to hold the information
class Recipe(object):
    def __init__(self, title, source, url, ingredients = [], info = {}, 
                 instr = "", tags = []):
        self.title = title
        self.source = source
        self.url = url
        self.ingredients = ingredients
        self.info = info # quick facts like yield, cook time etc
        self.instr = instr
        self.tags = tags

    def recipe_card(self):
        line = ("-" * 100) + "\n"
        t = str(self.title) + "\n"
        s = "Source: " + str(self.source) + "\n"
        u = "URL: " + str(self.url) + "\n"
        tags = "Tags: \n\t-" + "\n\t-".join(self.tags) + "\n\n"
        inf = "Quick Info: \n\t-" + "\n\t-".join(['%s %s' % (key, value) for (key, value) in self.info.items()]) + "\n\n"
        ing = "Ingredients: \n\t-" + "\n\t-".join([str(i) for i in self.ingredients]) + "\n\n"
        ins = "Instructions: \n" + "\n".join(self.instr) + "\n\n"
        
        return line + t + line + s + u + tags + inf + ing + ins + line
    
    def find_tools(self):
        tools = []
        for i in self.instr:
            ind = i.find("in a")
            if (ind >= 0):
                tools.append(i[ind: ind + 40])
                
        return tools
    
    # pantry is a dictionary of items as strings to ingredient objects
    def can_make(self, pantry):
        if self.ingredients == None or self.ingredients == []:
            return False
        for i in self.ingredients:
            if i.item in pantry:
                if i > pantry[i.title]:
                    return False
            else:
                return False
        return True
    
    # pantry is a dictionary of items as strings to ingredient objects
    def needed_ing(self, pantry):
        ingreds = 0
        for i in self.ingredients:
            if i in pantry:
                if i.quanity > pantry[i.title]:
                   ingreds += 1 
            else:
                ingreds += 1
        return ingreds
    
    def __hash__(self):
        return hash(self.url)
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url
            
    def __repr__(self):
        s = "Title: " + str(self.title) + " Info: " + str(self.info) + "Tags: " + str(self.tags)
        return s
    
#def get_nouns(text):
#    # function to test if something is a noun
#    is_noun = lambda pos: pos[:2] == 'NN'
#    # do the nlp stuff
#    tokenized = nltk.word_tokenize(text)
#    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
#    return nouns

def parse_quantity(string):
    words = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
             'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 
             'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 
             'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
             'eighteen': 18, 'nineteen': 19, 'twenty': 20}
    string = string.lower()
    if string in words:
        return words[string]
    if string.isdigit():
        return int(string)
    parts = string.split("/")
    if len (parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        return (int(parts[0]) / int(parts[1]))
    return None

def parse_ingreds(ls):
    measures = set(["tablespoon", "teaspoon", "pound", "ounce", "can", "cup", 
                "clove", "pint", "quart", "gallon", "drop"])
    measures.update([m + "s" for m in measures])
    measures.update(["dash", "dashes", "pinch", "pinches"])
    ing = []
    for i in ls:
        old_ing = i.replace("-", " ")
        parts = old_ing.split(" ")
        intersect = set(parts) & measures
        
        indices = []
        if not len(intersect) == 0:
            measure = list(intersect)[0]
            indices.append(parts.index(measure))
        else:
            measure = None
        
        quantity = None
        for p in parts:
            q = parse_quantity(p)
            if not q == None:
                indices.append(parts.index(p))
                if quantity == None:
                    quantity = q
                else:
                    quantity = quantity * q
        
        if indices == []:
            item = old_ing
        else:
            item = " ".join(parts[max(indices) + 1:])
        
        ingredient = Ingredient(item, quantity, measure)
        ing.append(ingredient)
    return ing
        

def parse_recipe(page, title = None):
    # check that page exists
    url = page
    request = requests.get(url)
    if not request.status_code < 400:
        return None
   
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    
    if title == None:
        title = soup.find("meta", property="og:title")
    source = "Food Network"

    # get time, yield, level info
    info = {}
    time_info = soup.find("section", class_="o-RecipeInfo o-Time")
    if not time_info == None:
        time_bits = [x for x in time_info.contents[1].contents if x != "\n"]
        for x in range(round (len(time_bits) / 2)):
            info.update({"Time To " + time_bits[x * 2].contents[0]:time_bits[(x * 2) + 1].contents[0]})
    yld = soup.find("section", class_="o-RecipeInfo o-Yield")
    if not yld == None:
        info.update({"Yield:":yld.contents[1].contents[3].string.strip()})
    lvl = soup.find("section", class_="o-RecipeInfo o-Level")
    if not lvl == None:
        info.update({"Level:":lvl.contents[1].contents[3].string.strip()})
    
    # parse ingredients
    ing = soup.find("div", class_="o-Ingredients__m-Body")
    if not ing == None:
        ing = ing.find_all("li")
        info.update({"Number of Ingredients:":len(ing)})
        ing_list = [l.contents[3].contents[0].strip() for l in ing]
    else:
        ing_list = []
    
    # parse directions
    directions = soup.find("div", class_="o-Method__m-Body")
    if not directions == None:    
        instr = [i.string.strip() for i in directions.contents if i != "\n" and len(i.contents) == 1]
    else:
        instr = []

    # parse tags
    tags = soup.find("div", class_="o-Capsule__m-TagList m-TagList")
    if not tags == None:
        all_tags = [t.string.strip().lower() for t in tags.contents if t != "\n"]
    else:
        all_tags = []

    # create recipe object
    recipe = Recipe(title, source, url, parse_ingreds(ing_list), info, instr, all_tags)
    soup.decompose()
    return recipe

def parse_page_of_recipe_links(page):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(page)
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find("div", class_="l-Columns l-Columns--2up").find_all("li")
    next_link = soup.find("a", "o-Pagination__a-Button o-Pagination__a-NextButton ")
    if not next_link == None:
        next_link = "http:" + next_link["href"]
        
    pg_links = {}
    for l in links:
        title = l.string.lower()
        link = "http:" + l.a["href"]
        if not title in pg_links:
            # print("Title: " + title)
            # print("Link: " + link)
            recipe = parse_recipe(link, title)
            # print("Tags: " + str(recipe.tags))
            if not recipe == None:
                pg_links.update({title:recipe})
            
    return pg_links, next_link

def parse_all_recipes():
    # categories = ["123", "a", "b", "c", "d", "e", "f", "g", "h", "i", 
    #               "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
    #              "u", "v", "w", "xyz"]
    categories = ["xyz"]
    recipe_box = {}
    for cat in categories:
        main_page = "http://www.foodnetwork.com/recipes/a-z/" + cat
        pg_links, next_link = parse_page_of_recipe_links(main_page)
        recipe_box.update(pg_links)
        print("|" + next_link + "|")
        while not next_link == None:
            pg_links, next_link = parse_page_of_recipe_links(next_link)
            recipe_box.update(pg_links)
    
    return recipe_box

def print_makeable_recipes(links, pantry):
    for r in links.values():
        if r.can_make(pantry):
            print(r.recipe_card())
            
def print_makeable_recipes_dev(links, pantry, dev):
    for r in links.values():
        if r.needed_ing(pantry) <= dev:
            print(r.recipe_card())
            
def print_recipes_with_tag(links, tag):
    for r in links.values():
        if tag.lower() in r.tags:
            print(r.title + " " + r.url)
            #print(r.recipe_card())
   
def make_pantry_from_recipe(page):         
    recipe = parse_recipe(page)
    pantry = {}
    for i in recipe.ingredients:
        pantry.update({i.item:i})
    return pantry

def test():
    pg_links, nxt = parse_page_of_recipe_links("http://www.foodnetwork.com/recipes/a-z/123")
    print("\n\n\n")
    print_recipes_with_tag(pg_links, "healthy")
# parse_recipe("http://www.foodnetwork.com/recipes/food-network-kitchen/slow-cooker-turkey-chili-3361632")
# soup = parse_page_of_recipe_links("http://www.foodnetwork.com/recipes/a-z/123")