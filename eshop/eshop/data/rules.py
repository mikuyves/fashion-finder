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
        'screenshot_js': '''window.scrollBy(0, 240);''',
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
}''',
    },

    'www.ssense.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a::text',
        'text_css': {
            'title': 'h2::text',
            'desc': '.product-description-text::text',
            'details': None,
        },
        'photo_urls_css': '.image-wrapper img::attr(data-src)',
        'screenshot_js': ''';''',
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
        'screenshot_js': ''';''',
    },

    'www.lyst.ca': {
        'has_zh_maybe': False,
        'type': 'Pool',
        'brand': 'h1 div[itemprop=brand] a::text, h3 span[itemprop=brand] a::text',
        'text_css': {
            'title': 'h1 div[itemprop=name]::text, h1 span[itemprop=name]::text',
            'desc': 'div[itemprop=description] p::text',
            'details': None,
        },
        'photo_urls_css': '.image-gallery-thumbnail::attr(data-full-image-url), .image-gallery__carousel__scroll-wrapper__image a::attr(href)',
        'screenshot_js': ''';''',
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
        'screenshot_js': ''';''',
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
        'screenshot_js': ''';''',
    },

    'www.neimanmarcus.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'span[itemprop=brand]::text, span[itemprop=brand] a::text',
        'text_css': {
            'title': 'span[itemprop=name]::text',
            'desc': None,
            'details': 'div[itemprop=description] li::text',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(data-zoom-url)',
        'screenshot_js': '''window.scrollBy(0, 150);''',
    },

    'www.fwrd.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.designer_brand::text',
        'text_css': {
            'title': '.product_name::text',
            'desc': None,
            'details': '.product_detail li::text',
        },
        'photo_urls_css': '.product_z img::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.madstyle.com.au': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MAD STYLE',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': '.std::text',
        },
        'photo_urls_css': '.gallery-image::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.theoutnet.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 a::text',
        'text_css': {
            'title': 'h1 span::text',
            'desc': None,
            'details': '.accordion-content li::text',
        },
        'photo_urls_css': '#large-image img::attr(data-src)',
        'screenshot_js': ''';''',
    },

    'www.armani.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ARMANI',
        'text_css': {
            'title': 'h1::text',
            'desc': '.descriptionContent::text',
            'details': '.descriptionList li::text',
        },
        'photo_urls_css': 'img.thumb::attr(src)',
        'handle_photo_urls': lambda x: [re.sub(r'_13_', '_16_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'us.zimmermannwear.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ZIMMERMANN',
        'text_css': {
            'title': 'h1::text',
            'desc': 'p.itemDesc::text',
            'details': '.small p::text',
        },
        'photo_urls_css': '.showmainImg::attr(data-fullimg)',
        'screenshot_js': '''window.scrollBy(0, 100);''',
    },

    'www.stylebop.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.h1 a::text',
        'text_css': {
            'title': 'h1.h2::text',
            'desc': '.desc-content li::text',
            'details': None,
        },
        'photo_urls_css': 'img::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 300);''',
    },

    'www.tedbaker.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TED BAKER',
        'text_css': {
            'title': 'h2.summary::text',
            'desc': '.description::text',
            'details': '#product_details li::text',
        },
        'photo_urls_css': '.pdp_main_slider img::attr(ng-src)',
        'screenshot_js': ''';''',
    },

    'www.kenzo.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'KENZO',
        'text_css': {
            'title': 'h1::text',
            'desc': '.kz-pp-fiche-desc div::text',
            'details': '.kz-pp-fiche-compo p::text',
        },
        'photo_urls_css': '.kz-pp-image img::attr(src)',
        'screenshot_js': ''';''',
    },

    'cn.sportmax.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'SPORTMAX',
        'text_css': {
            'title': '.c-product-data .h3-like::text',
            'desc': '.description::text',
            'details': 'li::text',
        },
        'photo_urls_css': 'a::attr(data-zoom)',
        'screenshot_js': '''window.scrollBy(0, 220);''',
    },

    'www.melijoe.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'a[itemprop=brand]::text',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': '.detail-bloc-item .value::text',
        },
        'photo_urls_css': '.swiper-slide::attr(data-zoom)',
        'screenshot_js': '''window.scrollBy(0, 100);''',
    },

    'www.modaoperandi.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.designer_title::text',
        'text_css': {
            'title': '.product_title::text',
            'desc': '.description_text p::text',
            'details': None,
        },
        'photo_urls_css': 'img.primary_image_display::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 50);''',
    },

    'www.fashionbarnshop.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1::text',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': '#tabs-1 li::text',
        },
        'photo_urls_css': '.slide a::attr(data-zoom-image)',
        'screenshot_js': '''window.scrollBy(0, 150);''',
    },

    'www.amazon.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '#productTitle::text',
        'text_css': {
            'title': '#productTitle::text',
            'desc': None,
            'details': '#feature-bullets .a-list-item::text',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': 'hiRes":"(\S+)","thumb',
        'screenshot_js': '''window.scrollBy(0, 200);''',
    },

    'www.aliceandolivia.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ALICE AND OLIVIA',
        'text_css': {
            'title': 'h1::text',
            'desc': '.box p font span::text',
            'details': 'li.MsoNormal span::text',
        },
        'photo_urls_css': '.slide img::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.gucci.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'GUCCI',
        'text_css': {
            'title': 'h1::text',
            'desc': '.product-detail p::text',
            'details': '.product-detail li::text',
        },
        'photo_urls_css': 'img.item-content::attr(data-src_standard_retina)',
        'screenshot_js': ''';''',
    },

    'www.selfridges.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 .brand a::text',
        'text_css': {
            'title': 'h1 .description::text',
            'desc': 'p[itemprop=description]::text',
            'details': '.productDetails script::text',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'screenshot_js': '''window.scrollBy(0, 200);''',
    },

    'us.sandro-paris.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'SANDRO',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': 'h2.detaildesc::text',
        },
        'photo_urls_css': '.productlargeimgdata::attr(data-lgimg)',
        'handle_photo_urls': lambda x: x[0].split('|'),
        'screenshot_js': ''';''',
    },

    'www.dereklam.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'DEREK LAM',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': '.os-product-description li::text',
        },
        'photo_urls_css': 'script',
        'photo_urls_re': '''"ImageUrl":"(\S+)","ImageThumbUrl"''',
        'screenshot_js': ''';''',
    },

    'www.tibi.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TIBI',
        'text_css': {
            'title': 'h1::text',
            'desc': '.std p::text',
            'details': '.std li::text',
        },
        'photo_urls_css': 'img.gallery-image::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.flannels.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '#ProductName::text',
        'text_css': {
            'title': '#ProductName::text',
            'desc': 'span[itemprop=description] p::text',
            'details': 'span[itemprop=description] li::text',
        },
        'photo_urls_css': '#piThumbList a::attr(href)',
        'handler_photo_urls': lambda x: [re.sub(r'_l_', '_xxl_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.bluefly.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'p[itemprop=brand] a::text',
        'text_css': {
            'title': 'title::text',
            'desc': 'div[itemprop=description]::text',
            'details': 'ul[data-ui=accordion-content] li::text',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.tadashishoji.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'TADASHI SHOJI',
        'text_css': {
            'title': 'h1::text',
            'desc': '.inner::text',
            'details': '.inner li::text',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
    },

    'www.montaignemarket.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'small.pr_brand a[itemprop=brand]::text',
        'text_css': {
            'title': 'h1::text',
            'desc': 'span[itemprop=description] p::text',
            'details': None,
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.vincecamuto.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'VINCE CAMUTO',
        'text_css': {
            'title': 'h1::text',
            'desc': '.product-tabs::text',
            'details': '.product-tabs li::text',
        },
        'photo_urls_css': 'li img::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.bottegaveneta.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BOTTEGA VENETA',
        'text_css': {
            'title': '.inner.modelName::text',
            'desc': None,
            'details': '.tab-body .value::text',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'photo_urls_re': '\S+.jpg$',
        'handle_photo_urls': lambda x: [re.sub(r'_7_', '_15_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.johnlewis.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': '.mod a img::attr(title)',
        'text_css': {
            'title': 'h1 span::text',
            'desc': 'span[itemprop=description] p::text',
            'details': 'dd::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+_main\$$',
        'handle_photo_urls': lambda x: [re.sub(r'_main', '_lrg', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.harrods.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h1 .brand::text',
        'text_css': {
            'title': '.productname::text',
            'desc': '.description::text',
            'details': '#details li::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+\$thumbnail\$$',
        'handle_photo_urls': lambda x: [re.sub(r'thumbnail', 'fullScreen', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.zadig-et-voltaire.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ZADIG ET VOLTAIRE',
        'text_css': {
            'title': 'h1::text',
            'desc': '.short-description p::text',
            'details': None,
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+530x795\S+',
        'handle_photo_urls': lambda x: [re.sub(r'\/530x795', '', url) for url in x],
        'screenshot_js': ''';''',
    },

    'intl.aritzia.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'ARITZIA',
        'text_css': {
            'title': 'h1::text',
            'desc': '.pdp-tab-content p::text',
            'details': '.pdp-tab-content li::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+thumbnail\S+',
        'handle_photo_urls': lambda x: [re.sub(r'thumbnail', 'large', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.mcq.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MCQ',
        'text_css': {
            'title': 'h1 span::text',
            'desc': '.descriptions .value::text',
            'details': '.compositionInfo .text::text',
        },
        'photo_urls_css': 'img::attr(srcset)',
        'photo_urls_re': ',(\S+) 2x$',
        'screenshot_js': ''';''',
    },

    'shop.nordstrom.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'h2 span::text',
        'text_css': {
            'title': 'h1::text',
            'desc': 'div[itemprop=description] p::text',
            'details': 'li::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '(\S+Zoom\S+.jpg)\?\S+',
        'screenshot_js': ''';''',
    },

    'us.maje.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MAJE',
        'text_css': {
            'title': 'h1 span::text',
            'desc': '.tabs-content p::text',
            'details': '.tabs-content span::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '(\S+.jpg)\?\S+',
        'screenshot_js': ''';''',
    },

    'www.ministryofstyle.com.au': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MINISTRY OF STYLE',
        'text_css': {
            'title': '.styledetails h2::text',
            'desc': '.description::text',
            'details': None,
        },
        'photo_urls_css': 'a::attr(zoom)',
        'screenshot_js': ''';''',
    },

    'www.bally.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BALLY',
        'text_css': {
            'title': 'h1::text',
            'desc': '#tab1 p::text',
            'details': '#tab2 p::text',
        },
        'photo_urls_css': 'img[itemprop=image]::attr(src)',
        'photo_urls_re': '(\S+.jpg)\?',
        'screenshot_js': ''';''',
    },

    'www.katespade.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'KATE SPADE',
        'text_css': {
            'title': 'h1::text',
            'desc': '#small-details::text',
            'details': '#small-description li::text',
        },
        'photo_urls_css': 'img::attr(data-cloudzoom)',
        'photo_urls_re': "image: '(\S+)'",
        'screenshot_js': ''';''',
    },

    'www.bcbg.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'BCBG',
        'text_css': {
            'title': 'h1::text',
            'desc': '#tab2 p::text',
            'details': '#tab2 li::text',
        },
        'photo_urls_css': 'img[itemprop]::attr(src)',
        'screenshot_js': ''';''',
    },

    'www.miumiu.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MIU MIU',
        'text_css': {
            'title': 'h2::text',
            'desc': 'p.desc::text',
            'details': None,
        },
        'photo_urls_css': 'a::attr(data-zoom)',
        'screenshot_js': ''';''',
    },

    'www.equipmentfr.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'EQUIPMENT',
        'text_css': {
            'title': 'span[itemprop=name]::text',
            'desc': 'span.desc::text',
            'details': '.product-description li::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+633x\S+.jpg$',
        'screenshot_js': ''';''',
    },

    'www.moschino.com': {
        'has_zh_maybe': False,
        'type': 'Official',
        'brand': u'MOSCHINO',
        'text_css': {
            'title': 'h1 span::text',
            'desc': '#tab-body p::text',
            'details': '#tab-body span::text',
        },
        'photo_urls_css': 'img::attr(src)',
        'photo_urls_re': '\S+_13_\w\.jpg',
        'handle_photo_urls': lambda x: [re.sub(r'_13_', '_14_', url) for url in x],
        'screenshot_js': ''';''',
    },

    'www.revolve.com': {
        'has_zh_maybe': False,
        'type': 'Retailer',
        'brand': 'span[property=brand]::text',
        'text_css': {
            'title': 'h1::text',
            'desc': None,
            'details': '.product-details__list li::text',
        },
        'photo_urls_css': 'a::attr(data-zoom-image)',
        'screenshot_js': ''';''',
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
