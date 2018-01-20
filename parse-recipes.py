# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:26:01 2018

@author: Saniyah
"""

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
# import pandas as pd
import requests

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
        t = "Title: " + str(self.title) + "\n"
        s = "Source: " + str(self.source) + "\n"
        u = "URL: " + str(self.url) + "\n"
        tags = "Tags: \n\t-" + "\n\t-".join(self.tags) + "\n\n"
        inf = "Quick Info: \n\t-" + "\n\t-".join(['%s %s' % (key, value) for (key, value) in self.info.items()]) + "\n\n"
        ing = "Ingredients: \n\t-" + "\n\t-".join(self.ingredients) + "\n\n"
        ins = "Instructions: \n" + "\n".join(self.instr) + "\n\n"
        
        return line + t + line + s + u + tags + inf + ing + ins + line
    
    def find_tools(self):
        tools = []
        for i in self.instr:
            ind = i.find("in a")
            if (ind >= 0):
                tools.append(i[ind: ind + 40])
                
        return tools

    def __repr__(self):
        s = "Title: " + str(self.title) + " Info: " + str(self.info) + "Tags: " + str(self.tags)
        return s

def parse_recipe(page):
    url = page

    request = requests.get(page)
    if not request.status_code < 400:
        return None
   
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(url)
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    
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
    ing = soup.find_all("div", class_="o-Ingredients__m-Body")[0].find_all("li")
    if not ing == None:
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
        all_tags = [t.string.strip() for t in tags.contents if t != "\n"]
    else:
        all_tags = []

    # create recipe object
    recipe = Recipe(title, source, url, ing_list, info, instr, all_tags)
    
    # soup.decompose()
    
    return recipe

def parse_page_of_recipe_links(page):
    # query the website and return the html to the variable ‘page’
    page = urllib.request.urlopen(page)
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find("div", class_="l-Columns l-Columns--2up").find_all("li")
    
    pg_links = {}
    for l in links:
        title = l.string.lower()
        link = "http:" + l.a["href"]
        if not title in pg_links:
            print("Title: " + title)
            print("Link: " + link)
            recipe = parse_recipe(link)
            if not recipe == None:
                pg_links.update({title:recipe})
            
    return pg_links

def parse_all_recipes():
    return 0

# parse_recipe("http://www.foodnetwork.com/recipes/food-network-kitchen/slow-cooker-turkey-chili-3361632")
# soup = parse_page_of_recipe_links("http://www.foodnetwork.com/recipes/a-z/123")