import scrapy
from ScrapyEng.items import ProgrammeEsb

class ParcoursSpider(scrapy.Spider):
    name = 'Parcours'
    allowed_domains = ['esb.tn']
    start_urls = ['https://www.esb.tn/programmes/masters-professionnels/',
                  "https://www.esb.tn/programmes/licences/"]

    def parse(self, response):
        programs = response.css('div.caption')
        
        for program in programs:
            item = ProgrammeEsb()
            lien = program.css('a.button::attr(href)').get()

            item['titre'] = program.css('div.title h2::text').get()
            item['description'] = program.css('div.text::text').get(default='').strip()
            item['url'] = lien

            yield response.follow(lien, self.detailsDuProgramme, meta={'item': item})

    def detailsDuProgramme(self, response):
        item = response.meta['item']

        item['niveau'] = response.css('p.elementor-icon-box-description::text').getall()[0].strip()
        item['prerequis'] = response.css('p.elementor-icon-box-description::text').getall()[1].strip() 
        item['credits_ects'] = response.css('p.elementor-icon-box-description::text').getall()[2].strip() 
        item['duree'] = response.css('p.elementor-icon-box-description::text').getall()[3].strip()
        item['regime'] = response.css('p.elementor-icon-box-description::text').getall()[4].strip()
        item['metiers'] = response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=1 or position()=2]/div[1]/ul | //*[contains(@id, "htmegatab")]/div/div/div/div/section[2]/div/div/div[1]/div/div/div[3]/div/div/ul').xpath('.//text()').getall()
        item['secteurs'] =  response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=1 or position()=2]/div[2]/ul//text() | ''//*[contains(@id, "htmegatab")]/div/div/div/div/section[2]/div/div/div[2]/div/div/div[3]/div/div/ul//text()').getall()
        item['modules'] = response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=2 or position()=3]/div/div//text() | ''//*[contains(@id, "htmegatab")]/div/div/div/div/section[3]/div/div/div/div/div/div[2]/div/div//text()').getall()
        item['contenu'] = response.xpath('//*[contains(@id, "elementor-tab-content-1901") or contains(@id, "elementor-tab-content-2011") or contains(@id, "elementor-tab-content-7021")]/ul[1] | //*[contains(@id, "htmegatab-924cee31")]/div/div/div/div/section[1]/div/div/div/div/div/div[4]/div/div/ul').xpath('.//text()').getall() 
        item['competences'] = response.xpath('//*[contains(@id, "elementor-tab-content-1901") or contains(@id, "elementor-tab-content-2011") or contains(@id, "elementor-tab-content-7021")]/ul[position()=2 or position()=3] | //*[contains(@id, "htmegatab")]/div/div/div/div/section[1]/div/div/div/div/div/div[6]/div/div/ul').xpath('.//text()').getall()        
 
        yield item
