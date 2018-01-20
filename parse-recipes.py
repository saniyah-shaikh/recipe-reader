# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:26:01 2018

@author: Saniyah
"""

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

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

    def __repr__(self):
        s = "Title: " + str(self.title) + " Info: " + str(self.info) + "Tags: " + str(self.tags)
        return s

def parse_recipe(page):
    url = page
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    
    # get title and source
    title_bits = soup.title.string.split("|")
    title = title_bits[0]
    source = title_bits[1]
    
    # get time, yield, level info
    info = {}
    recipe_info = soup.find_all("div", class_="parbase recipeInfo")[0]
    bits = recipe_info.contents[2]
    parts = bits.contents
    time_info = parts[3].contents[1].contents[1]
    time_bits = [x for x in time_info.contents if x != "\n"]
    for x in range(round (len(time_bits) / 2)):
        info.update({"Time To " + time_bits[x * 2].contents[0]:time_bits[(x * 2) + 1].contents[0]})
    yld = parts[7].contents[1].contents[3].contents[0].strip()
    info.update({"Yield:":yld})
    level = parts[11].contents[1].contents[3].contents[0].strip()
    info.update({"Level:":level})
    
    # parse ingredients
    ing = soup.find_all("div", class_="o-Ingredients__m-Body")[0].find_all("li")
    info.update({"Number of Ingredients:":len(ing)})
    ing_list = [l.contents[3].contents[0].strip() for l in ing]
    
    # parse directions
    directions = soup.find("div", class_="o-Method__m-Body")
    instr = [i.string.strip() for i in directions.contents if i != "\n"]

    # parse tags
    tags = soup.find("div", class_="o-Capsule__m-TagList m-TagList")
    all_tags = [t.string.strip() for t in tags.contents if t != "\n"]

    # create recipe object
    recipe = Recipe(title, source, url, ing_list, info, instr, all_tags)

    return recipe

def parse_page_of_recipe_links():
    return 0

def parse_all_recipes():
    return 0

# parse_recipe("http://www.foodnetwork.com/recipes/food-network-kitchen/slow-cooker-turkey-chili-3361632")