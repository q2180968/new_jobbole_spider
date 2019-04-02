# -*- coding: utf-8 -*-
import scrapy
import re
from urllib import parse
from scrapy import Request
from jobbole_spider.items import ArticleItem, ArticleItemLoader
from jobbole_spider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-post/']

    def parse(self, response):
        # 1、提取详情页URL
        # 2、将每页的URL重新解析
        post_nodes = response.css('#archive .floated-thumb  .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first('')
            front_image_url = post_node.css('img::attr(src)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'front_image_url': parse.urljoin(response.url, front_image_url)},
                          callback=self.parse_detail)

            # 3、获取下一页url并交给scrapy下载，完成后交给parse
            # next_url = response.css('.next.page-numbers::attr(href)').extract_first()
            # if next_url:
            #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # articleItem = ArticleItem()
        #
        # title = response.css('.entry-header h1::text').extract_first('')
        # create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('').strip().replace(' ·', '')
        # praise_nums = response.css('.vote-post-up h10::text').extract_first('')
        # fav_nums = response.css('.bookmark-btn::text').extract_first('')
        # match_num = re.match('.*?(\d+).*?', fav_nums)
        # if match_num:
        #     fav_nums = match_num.group(1)
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract_first('')
        # match_num = re.match('.*?(\d+).*?', comment_nums)
        # if match_num:
        #     comment_nums = match_num.group(1)
        # else:
        #     comment_nums = 0
        # content = response.css('.entry').extract_first('')
        # tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tag_list = [element for element in tags if not element.strip().endswith('评论')]

        front_image_url = response.meta.get('front_image_url', '')
        # 使用item
        # articleItem['title'] = title
        # articleItem['create_date'] = create_date
        # articleItem['url'] = response.url
        # articleItem['url_obj_id'] = get_md5(response.url)
        # articleItem['front_image_url'] = [front_image_url]
        # articleItem['front_image_path'] = ['']
        # articleItem['praise_nums'] = praise_nums
        # articleItem['comment_nums'] = comment_nums
        # articleItem['fav_nums'] = fav_nums
        # articleItem['tags'] = tag_list
        # articleItem['content'] = content

        item_loader = ArticleItemLoader(item=ArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_obj_id', get_md5(response.url))
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_value('front_image_path', ' ')
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('comment_nums', "a[href='#article-comment'] span::text")
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', '.entry')
        articleItem = item_loader.load_item()
        yield articleItem
