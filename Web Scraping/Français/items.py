# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProgrammeEsb(scrapy.Item):
   titre = scrapy.Field()
   url = scrapy.Field()
   description = scrapy.Field()
   niveau = scrapy.Field()
   prerequis = scrapy.Field()
   credits_ects = scrapy.Field()
   duree = scrapy.Field()
   regime = scrapy.Field()
   contenu = scrapy.Field()
   competences = scrapy.Field()
   metiers = scrapy.Field()
   secteurs  = scrapy.Field()
   modules = scrapy.Field()

class Studyrama(scrapy.Item):
   secteur = scrapy.Field()
   url = scrapy.Field()
   metier = scrapy.Field()
   
