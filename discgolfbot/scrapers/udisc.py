import time
from dateutil.parser import parse
from score.scorecard import Scorecard
from score.player import Player, PlayerName
from scrapers.scraper import Scraper

import requests
from bs4 import BeautifulSoup

class Udisc(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'udisc.com'
        self.url = 'https://udisc.com'


# from selenium import webdriver
# chromeopt = webdriver.ChromeOptions()
# exopt = {
#     "download.default_directory":"C:\\Program Files\\Python310\\Lib\\chromedriver_win32"
# }
# chromeopt.add_experimental_option("prefs",exopt)
class LeagueScraper(Udisc):
    def __init__(self, url):
        super().__init__()
        self.scrape_url = url
        self.score_card = Scorecard("", "", "2021-01-01 12:00", 0)

    def scrape(self):
        start_time = time.time()
        # soup = uscraper.selenium_get_beatifulsoup(4)
        soup = self.selenium_get_beatifulsoup(4)
        url_dgclasses = []
        dg_classes = {}
        if(re.search("division=ALL", url)):
            #expression = re.compile("MuiTypography-root jss\d{2,3} MuiTypography-body1")
            for dg_class in soup.findAll("p", class_= re.compile("MuiTypography-root jss\d{2,3} MuiTypography-body1")): #recurive=False
                #print (dg_class.getText())
                if(re.search("^(FP|MP|MJ|FJ)", dg_class.getText())):
                    #print (dg_class.getText())
                    dg_classes.update({dg_class.get_text().split(" ")[0]:dg_class.getText()})
                    url_dgclasses.append(url.replace("ALL", dg_class.get_text().split(" ")[0]))
        else:
            url_dgclasses = url        

        header = soup.find("div", class_="jss55 jss57")
        if header is None:
            return

        # Course Name
        course_name = header.find("a", class_="MuiTypography-root MuiLink-root MuiLink-underlineHover jss75 MuiTypography-colorPrimary")
        if course_name is None:
            return
        # uscraper.score_card.coursename = course_name.getText().rstrip()
        self.score_card.coursename = course_name.getText().rstrip()
        # Course link
        course_url = course_name['href']
        if course_url is not None:
            # uscraper.score_card.course_url = f'{uscraper.url}{course_url}'
            self.score_card.course_url = f'{self.url}{course_url}'

        # Layout Name
        # uscraper.score_card.layoutname = soup.find("p", class_="MuiTypography-root jss96 MuiTypography-body1").getText().replace("LAYOUT: ", "").rstrip(" ")
        self.score_card.layoutname = soup.find("p", class_="MuiTypography-root jss96 MuiTypography-body1").getText().replace("LAYOUT: ", "").rstrip(" ")
        

        date = header.find("p", class_="MuiTypography-root jss74 MuiTypography-body1")
        if date is None:
            return
        # Date, varies between two formats ("September 12th 2021, or "Sept 12")
        date_text = date.getText().split("·")[1]
        #  uscraper.score_card.date_time = parse(date_text)
        self.score_card.date_time = parse(date_text)
        
        tour_id = soup.find("div", id="tour-leaderboard")
        # Add par
        par = tour_id.find("p", class_="jss122 jss158 undefined").getText()
        self.score_card.par = int(par)
        # uscraper.score_card.par = int(par)
        # Add par for holes
        hole_par_list = tour_id.find_all("p", class_="jss122 jss158")
        for i in range(len(hole_par_list)):
            self.score_card.add_hole(i+1, int(hole_par_list[i].getText()))
            # uscraper.score_card.add_hole(i+1, int(hole_par_list[i].getText()))

        # scrape each division seperately in order to accurately assign scores per class (M*/F*)
        url_class = url_dgclasses[0]
        scorecards = []
        for url_class in url_dgclasses:
            division_label = None
            for key in dg_classes:
                if re.search(key, url_class):
                    print (key)
                    division_label = dg_classes[key]
            division_scorecard = Scorecard(uscraper.score_card.coursename, uscraper.score_card.layoutname, "2021-01-01 12:00", uscraper.score_card.par)
            # division_scorecard = Scorecard(self.score_card.coursename, self.score_card.layoutname,"2021-01-01 12:00", self.score_card.par)
            division_scorecard.date_time = parse(date_text)
            division_scorecard.division = division_label
            uscraper.scrape_url = url_class
            
            # self.scrape_url = url_class
            soup_cup = uscraper.selenium_get_beatifulsoup(4)
            tour_data = soup_cup.find("div", id="tour-leaderboard")
            for player in tour_data.find_all("tr", class_="jss124 false collapsed"):
                player_name = PlayerName("")
                score = ""
                scores = []
                player_row = player.find_all("td", class_="jss126 jss159")
                for row_no in range(len(player_row)):
                    if(row_no == 0):
                        print (f"Position: {player_row[row_no].getText()}")
                    elif(row_no == 1):
                        player_name.name = player_row[row_no].getText()
                    elif (row_no == 2):
                        if (player_row[row_no].getText() == "E"):
                            score = "0"
                        else:
                            score = player_row[row_no].getText().replace("+", "")
                    elif(row_no > 3):
                        scores.append(player_row[row_no].getText())

                total = scores.pop()
                scorecard_player = Player(player_name, total, score)
                for hole_score in scores:
                    scorecard_player.add_hole(hole_score)
                division_scorecard.add_player(scorecard_player)
                #self.score_card.add_player(scorecard_player)
            scorecards.append(division_scorecard)
        self.score_card = scorecards
        self.scraper_time = time.time() - start_time
        print(f'UdiscLeague scraper: {self.scraper_time}')