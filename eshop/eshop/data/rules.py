# -*- coding: utf-8 -*-
################################### Notice ####################################
# `en2zh` is a function which changes the English url into Chinese one.
# `screenshot_js` steps:
# 1) Let the screen focus on the item.
# 2) Set the price back to origin if it is on sale.
# 3) Delete the elements about discount.
#
# TODO: net-a-porter.com, if only change /en/ to /zh/, the spider will be baned.
# But I don't know why yet.
###############################################################################
import re


website_rules = {
    'www.lanecrawford.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com.cn', x),
        'css_rules': {
            'brand': '.lc-product-brand-refresh::text',
            'title': '.lc-product-short-description-refresh::text',
            'desc': '.text-paragraph::text',
            'detail': '.sizeAndFit li::text',
        },
        'photo_urls_css': '.hero-carousel__img::attr(data-xl)',
        'photo_urls_re': None,
        'screenshot_js': '''window.scrollBy(0, 174);
if ($(".discounted-price").text().replace(/(^\s*)|(\s*$)/g, '').length != 0){
    $(".sale-price").text($(".discounted-price").text());
    $(".discounted-price").remove();
    $(".save-percentage").remove();
};''',
    },

    'www.net-a-porter.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/us/en/', '/cn/zh/', x),
        'css_rules': {
            'brand': '.designer-name span::text',
            'title': '.product-name::text',
            'desc': '.show-hide-content .wrapper p::text',
            'detail': '.show-hide-content .wrapper ul li::text',
        },
        'photo_urls_css': '.thumbnail-image::attr(src)',
        'photo_urls_re': None,
        'screenshot_js': '''window.scrollBy(0, 174);
if ($(".container-title .sale") != 0){
    $(".container-title .sale-price").text($(".container-title .full-price").text());
    $(".container-title .sale").removeClass("sale");
    $(".container-title s").remove();
    $(".container-title .discount").remove();
}''',
    },

    'www.farfetch.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'.com', '.com/cn', x),
        'css_rules': {
            'brand': '.detail-brand a::text',
            'title': '.detail-brand span::text',
            'desc': '.product-detail p::text',
            'detail': '.product-detail-dl dd::text',
        },
        'photo_urls_css': '.sliderProduct-link img::attr(data-fullsrc)',
        'photo_urls_re': None,
        'screenshot_js': '''window.scrollBy(0, 50);
if ($(".js-discount-label").html().replace(/(^\W\s*)|(\W\s*$)/g, '').length != 0){
    $(".js-discount-label").html($(".js-price-without-promotion").html());
    $(".js-price-without-promotion").remove();
    $(".js-price").remove();
}''',
    },

    'www.shopbop.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'www.', 'cn.', x),
        'text_css': {
            'brand': '.brand-heading a::text',
            'title': '.product-title::text',
            'desc': '.content[itemprop*=description]::text',
            'detail': 'div[id*=modelSize]::text',
        },
        'photo_urls_css': 'script[type*=text\/javascript]::text',
        'photo_urls_re': 'zoom": "(\S+)"',
        'screenshot_js': '''window.scrollBy(0, 150);
if ($(".originalRetailPrice").length != 0){
    $(".originalRetailPrice").removeClass("originalRetailPrice")
    $(".priceBlock:eq(1)").remove();
}''',
    },
}
