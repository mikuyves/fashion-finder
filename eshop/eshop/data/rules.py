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

    'www.matchesfashion.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a::text',
        'text_css': {
            'title': 'h1 span::text',
            'desc': '.scroller-content p::text',
            'details': None,
        },
        'photo_urls_css': '.gallery-panel__main-image-carousel img::attr(src)',
        'screenshot_js': '''$('.mfp-wrap').remove();
$('.mfp-bg').remove();
window.scrollBy(0, 174);
if ($('.pdp-price__hilite').length != 0){
    var price_text = $('strike:eq(0)').text();
    $('.pdp-price').text(price_text);
}
''',
    },

    'www.ssense.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a::text',
        'text_css': {
            'title': 'h2::text',
            'desc': '.product-description-text::text',
            'details': '.inner-content li::text',
        },
        'photo_urls_css': '.image-wrapper img::attr(data-src)',
        'screenshot_js': '''
''',
    },

    'www.lyst.com': {
        'has_zh_maybe': False,
        'type': 'Pool',
        'brand': 'h1 div[itemprop=brand] a::text, h3 span[itemprop=brand] a::text',
        'text_css': {
            'title': 'h1 div[itemprop=name]::text, h1 span[itemprop=name]::text',
            'desc': 'div[itemprop=description] p::text',
            'details': None,
        },
        'photo_urls_css': '.image-gallery-thumbnail::attr(data-full-image-url), .image-gallery__carousel__scroll-wrapper__image a::attr(href)',
        'screenshot_js': '''
''',
    },

    'www.shopsplash.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'Alexis',
        'text_css': {
            'title': 'h1[itemprop=name]::text',
            'desc': 'div.into::text',
            'details': None,
        },
        'photo_urls_css': 'a.cloud-zoom-gallery::attr(href)',
        'screenshot_js': '''
''',
    },

    'www.stellamccartney.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'Stella Mccartney',
        'text_css': {
            'title': 'h1.title span::text',
            'desc': '.contentDesc .editorialdescription .value::text',
            'details': '.contentDesc .details .value::text',
        },
        'photo_urls_css': 'img::attr(srcset)',
        'photo_urls_re': r',(\S+) 1920w',
        'screenshot_js': '''
''',
    },

    'www.neimanmarcus.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'proxy': True,
        'brand': 'span[itemprop=brand]::text, span[itemprop=brand] a::text',
        'text_css': {
            'title': 'span[itemprop=name]::text',
            'desc': None,
            'details': 'div[itemprop=description] li::text',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(data-zoom-url)',
        'screenshot_js': '''window.scrollBy(0, 150);
$('.item-label').remove();
$('ins.sale-text').remove();
$('.tooltipHolder').remove();
''',
    },
}


###############################################################################
############################ Rules with problems ##############################
#
# neimanmarcus.com will banned your IP and redirect to a url that let you to
# input CAPCHA. We can change IP by middlewares, but there is still something
# wrong with `photo_urls_css`, `brand` and get a screenshot by selenium.
#    'www.neimanmarcus.com': {
#        'has_zh_maybe': False,
#        'type': 'Retailer',
#        'brand': 'span[itemprop=brand]::text, span[itemprop=brand] a::text',
#        'text_css': {
#            'title': 'span[itemprop=name]::text',
#            'desc': None,
#            'details': 'div[itemprop=description] li::text',
#        },
#        'photo_urls_css': 'img[itemprop=image]::attr(data-zoom-url)',
#        'screenshot_js': '''window.scrollBy(0, 150);
#$('.item-label').remove();
#$('ins.sale-text').remove();
#$('.tooltipHolder').remove();
#''',
#    },
