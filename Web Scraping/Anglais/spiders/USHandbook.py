import scrapy
from ScrapyEng.items import laborStatsUS


class UshandbookSpider(scrapy.Spider):
    name = "laborStatsUS"
    allowed_domains = ["onetonline.org"]
    start_urls = ["https://www.onetonline.org/find/career?c=0"]

    def parse(self, response):
        career_clusters = response.css('table.table tbody tr')

        for cluster in career_clusters:
            item = laborStatsUS()
            lien = cluster.xpath('.//td[4]/a[1]/@href').get()

            item['Career_cluster'] = cluster.css('td[data-title="Career Cluster"]::text').get(default='N/A')
            item['Career_pathway'] = cluster.css('td[data-title="Career Pathway"]::text').get(default='N/A')

            if lien:
                yield response.follow(
                    lien,
                    callback=self.extract_occupation_details,
                    meta={'item': item}
                )

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def extract_occupation_details(self, response):
        item = response.meta['item']

        item['Occupation'] = response.css('span.main::text').get(default='N/A')
        item['Tasks'] = response.css('#Tasks div ul li .order-2.flex-grow-1::text').getall()
        item['Technology_skills'] = response.css('#TechnologySkills div ul li b::text').getall()
        item['Activities'] = response.css('#DetailedWorkActivities div ul li .order-2.flex-grow-1::text').getall()
        item['Skills'] = response.css('#Skills div ul li .order-2.flex-grow-1 b::text').getall()
        item['Knowledge'] = response.css('#Knowledge div ul li div div:first-child').xpath('string(.)').getall()
        item['Abilities'] = response.css('#Abilities div ul li div div:first-child').xpath('string(.)').getall()
        item['Education'] = response.css('#Education ul li').xpath('normalize-space(string(.))').getall()
        item['Interests'] = response.css('#Interests ul li').xpath('normalize-space(string(.))').getall()

        yield item
