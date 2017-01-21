# -*- coding: utf-8 -*-
import re

# Notice: `en2zh` is a function which change the English website to Chinese.
# TODO: net-a-porter.com, if only change /en/ to /zh/, the spider will be baned.
# But I don't know why yet.
website_rules = {
    'www.lanecrawford.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com.cn', x),
        'css_rules': {
            'brand': '.lc-product-brand-refresh::text',
            'title': '.lc-product-short-description-refresh::text',
            'desc': '.text-paragraph::text',
            'detail': '.sizeAndFit li::text',
            'photo_urls': '.hero-carousel__img::attr(data-xl)',
        }
    },
    'www.net-a-porter.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/us/en/', '/cn/zh/', x),
        'css_rules': {
            'brand': '.designer-name span::text',
            'title': '.product-name::text',
            'desc': '.show-hide-content .wrapper p::text',
            'detail': '.show-hide-content .wrapper ul li::text',
            'photo_urls': '.thumbnail-image::attr(src)',
        }
    },
}
