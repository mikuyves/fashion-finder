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
        'type': 'Retailer',
        'brand': '.lc-product-brand-refresh::text',
        'text_css': {
            'title': '.lc-product-short-description-refresh::text',
            'desc': '.text-paragraph::text',
            'details': '.sizeAndFit li::text',
        },
        'photo_urls_css': '.hero-carousel__img::attr(data-xl)',
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
        'type': 'Retailer',
        'brand': '.designer-name span::text',
        'text_css': {
            'title': '.product-name::text',
            'desc': '.show-hide-content .wrapper p::text',
            'details': '.show-hide-content .wrapper ul li::text',
        },
        'photo_urls_css': '.thumbnail-image::attr(src)',
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
        'type': 'Retailer',
        'brand': '.detail-brand a::text',
        'text_css': {
            'title': '.detail-brand span::text',
            'desc': '.product-detail p[itemprop*=description]::text',
            'details': '.product-detail-dl dd::text',
        },
        'photo_urls_css': '.sliderProduct-link img::attr(data-fullsrc)',
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
        'type': 'Retailer',
        'brand': '.brand-heading a::text',
        'text_css': {
            'title': '.product-title::text',
            'desc': '.content[itemprop*=description]::text',
            'details': 'div[id*=modelSize]::text',
        },
        'photo_urls_css': 'script[type*=text\/javascript]::text',
        'photo_urls_re': 'zoom": "(\S+)"',
        'screenshot_js': '''window.scrollBy(0, 150);
if ($(".originalRetailPrice").length != 0){
    $(".originalRetailPrice").removeClass("originalRetailPrice")
    $(".priceBlock:eq(1)").remove();
}''',
    },

    'www.mytheresa.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/en-us/', '/zh-cn/', x),
        'type': 'Retailer',
        'brand': '.product-shop .product-designer a::text',
        'text_css': {
            'title': '.product-shop .product-name span::text',
            'desc': '.product-description::text',
            'details': '.featurepoints li::text',
        },
        'photo_urls_css': '.gallery-image::attr(src)',
        'handle_photo_urls': lambda x: [re.sub(r'/1088/1088/66/', u'/2176/2176/90/', url) for url in x],
        'screenshot_js': '''window.scrollBy(0, 240);
var price = document.getElementsByClassName('old-price')[0].childNodes[1].innerHTML;
var info = document.getElementsByClassName('price-info')[0];
info.innerHTML = '';
info.appendChild(document.createTextNode(price));
''',
    },

    'us.burberry.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'us.', 'cn.', x) + '?locale=zh-CN',
        'type': 'Official',
        'brand': u'BURBERRY',
        'text_css': {
            'title': 'h1::text',
            'desc': '.cell-paragraph_description li::text',
            'details': '.cell-paragraph_details li::text',
        },
        'text_css_zh': {
            'title': 'h1::text',
            'desc': '.accordion-tab_content p::text',
            'details': '.accordion-tab_sub-item li::text',
        },
        'photo_urls_css': 'div::attr(data-zoom-src)',
        'screenshot_js': ''';''',
    },

    'www.luisaviaroma.com': {
        'has_zh_maybe': True,
        'en2zh': lambda x: re.sub(r'/lang_EN/', '/lang_ZH/', x),
        'type': 'Retailer',
        'brand': '#sp_a_designer::text',
        'text_css': {
            'title': '#sp_a_category::text',
            'desc': None,
            'details': '#sp_details li::text',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': '"PhotosAll":\[(\S+)\],"PhotosByColor"',
        'handle_photo_urls': lambda x: ['https://images.luisaviaroma.com/Zoom' + url for url in re.split('[",]+', x[0]) if url],
        'screenshot_js': '''window.scrollBy(0, 50);
$('#footer_tc_privacy_button').click();
$('table').remove();
var span_price = $('#sp_span_price');
var price_text = span_price.text();
var minus_index = price_text.indexOf('-')
if (minus_index != -1){
price_text.replace(price_text.slice(minus_index), '');
$('#sp_span_discountedprice').remove();
}''',
    },
}
