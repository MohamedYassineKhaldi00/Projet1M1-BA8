import scrapy
from ScrapyEng.items import ProgrammeEsb

class ParcoursSpider(scrapy.Spider):
    name = 'Parcours'
    allowed_domains = ['esb.tn']
    start_urls = ['https://www.esb.tn/programs-3/bachelors-degree/sciences-de-gestion2/',
 'https://www.esb.tn/programs-3/bachelors-degree/bachelors-degree-in-business-computing/',
 'https://www.esb.tn/programs-3/bachelors-degree/bachelors-degree-in-applied-mathematics/',
 'https://www.esb.tn/en/programs-3/masters/professional-master-of-digital-management-information-systems/',
 'https://www.esb.tn/en/programs-3/masters/professional-master-in-digital-marketing/',  
 'https://www.esb.tn/en/programs-3/masters/professional-master-in-business-analytics/', 
 'https://www.esb.tn/en/programs-3/masters/professional-master-of-accounting-control-audit/',
 'https://www.esb.tn/programs-3/masters/master-professionnel-gamma-2/',
 'https://www.esb.tn/programs-3/masters/professional-master-in-digital-finance/']

    def parse(self, response):
        item = ProgrammeEsb()

        item['Title'] = response.css('h1.elementor-heading-title::text').get()
        # item['description'] = response.css('div[id^="elementor-tab-content"] blockquote p::text').get().strip()
        item['Degree'] = response.css('p.elementor-icon-box-description::text').getall()[0].strip()
        item['Prerequisite'] = response.css('p.elementor-icon-box-description::text').getall()[1].strip() 
        item['Credits'] = response.css('p.elementor-icon-box-description::text').getall()[2].strip() 
        item['Duration'] = response.css('p.elementor-icon-box-description::text').getall()[3].strip()
        item['Format'] = response.css('p.elementor-icon-box-description::text').getall()[4].strip()
        item['Careers'] = response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=1 or position()=2]/div[1]/ul | //*[contains(@id, "htmegatab")]/div/div/div/div/section[2]/div/div/div[1]/div/div/div[3]/div/div/ul').xpath('.//text()').getall()
        item['Sectors'] =  response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=1 or position()=2]/div[2]/ul//text() | ''//*[contains(@id, "htmegatab")]/div/div/div/div/section[2]/div/div/div[2]/div/div/div[3]/div/div/ul//text()').getall()
        item['Subjects'] = response.xpath('//*[contains(@id, "elementor-tab-content")]/div[position()=2 or position()=3]/div/div//text() | ''//*[contains(@id, "htmegatab")]/div/div/div/div/section[3]/div/div/div/div/div/div[2]/div/div//text()').getall()
        item['Skills'] = response.xpath('//*[@id="elementor-tab-content-7772"]/ul[5] | //*[@id="elementor-tab-content-7773"]/ul[5] | //*[@id="elementor-tab-content-7522"]/ul[2] | //*[@id="elementor-tab-content-7523"]/ul[5] | //*[@id="elementor-tab-content-1301"]/ul[2] | //*[@id="elementor-tab-content-7021"]/ul[2] | //*[@id="elementor-tab-content-1901"]/ul[2] | //*[@id="elementor-tab-content-2481"]/ul[6] | //*[@id="elementor-tab-content-2011"]/ul | //*[@id="elementor-tab-content-1831"]/ul[2] | //*[@id="elementor-tab-content-1461"]/ul').xpath('.//text()').getall()

        yield item
