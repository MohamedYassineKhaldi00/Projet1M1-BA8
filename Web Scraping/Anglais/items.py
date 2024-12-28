# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProgrammeEsb(scrapy.Item):
   Title = scrapy.Field()
   url = scrapy.Field()
   description = scrapy.Field()
   Degree = scrapy.Field()
   Prerequisite = scrapy.Field()
   Credits = scrapy.Field()
   Duration = scrapy.Field()
   Format = scrapy.Field()
   contenu = scrapy.Field()
   Skills = scrapy.Field()
   Careers = scrapy.Field()
   Sectors  = scrapy.Field()
   Subjects = scrapy.Field()

class laborStatsUS(scrapy.Item):
   Career_cluster = scrapy.Field()
   Career_pathway = scrapy.Field()
   Url = scrapy.Field()
   Occupation = scrapy.Field()
   Tasks = scrapy.Field()
   Technology_skills = scrapy.Field()
   Activities = scrapy.Field()
   Skills = scrapy.Field()
   Knowledge = scrapy.Field()
   Abilities = scrapy.Field()
   Education = scrapy.Field()
   Interests = scrapy.Field()
   Values  = scrapy.Field()
   Traits = scrapy.Field()


class Studyrama(scrapy.Item):
   secteur = scrapy.Field()
   url = scrapy.Field()
   metier = scrapy.Field()
   

 
 