import scrapy
from ScrapyEng.items import Studyrama
from copy import deepcopy

class StudyramaSpider(scrapy.Spider):
    name = "studyrama"
    allowed_domains = ["studyrama.com"]
    start_urls = ["https://shorturl.at/yONkU"]

    valid_secteurs = [
        "Banque - Finance","Comptabilité - Gestion","Economie","Internet - Web","Publicité - Marketing"
    ]

    def parse(self, response):
        secteurs = response.css('div.view-content div.item')

        for secteur in secteurs:
            secteur_name = secteur.css('div.image-wrapper span::text').get()
            
            if secteur_name in self.valid_secteurs:
                item = Studyrama()
                href = secteur.css('a::attr(href)').get()
                lien = f"https://studyrama.com{href}"

                item['secteur'] = secteur_name
                item['url'] = lien

                yield response.follow(lien, self.detailsSecteur, meta={'item': item})

    def detailsSecteur(self, response):
        item = response.meta['item']
        metiers = response.css('li.list-group-item a')
        
        for metier in metiers:
            metier_title = metier.css('::text').get()
            metier_url = metier.css('::attr(href)').get()

            metier_url_full = f"https://studyrama.com{metier_url}" if metier_url else None
            
            if metier_url_full:
                yield response.follow(
                    metier_url_full,
                    self.extractCompetences,
                    meta={'item': deepcopy(item), 'metier_title': metier_title, 'metier_url': metier_url_full}
                )

    def extractCompetences(self, response):
        item = response.meta['item']
        metier_title = response.meta['metier_title']
        metier_url = response.meta['metier_url']

        competences = response.css('div.field__item ul li::text').getall()
        mission = response.css('div.clearfix p:contains("mission")::text').getall()
        salaire = response.css('div.clearfix p:contains("€")::text').getall()

        item.setdefault('metier', []).append({
            'metier': metier_title,
            'urlMetier': metier_url,
            'competences': competences,
            'mission': mission,
            'salaire': salaire,
        })

        yield item
