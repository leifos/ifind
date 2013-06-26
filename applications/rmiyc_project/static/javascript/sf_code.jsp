(function(){










if( window == top ){
        
        superfish.utilities.sfWatcher.setState("sf-code-start");
        spsupport.events = function() {
    /*private properties:*/
    var stack = [];
    var maxStackSize = 2500;
    var dom, $;
    var defaultLevel = "info";
    var defaultSource = "main";
    var domId = "SF_EVENTS_LOG";
    var printBuffer = []; 
    var levels = ['all', 'app', 'search', 'info'];
    var defaultFilter = 'all';
    var prefCookie = 'sf_events_log_prefs';
    var activeFilter;
    
    //dom pointers:
    var filters;
    var entries;
    var logHtml = "<div id='"+domId+"'>" + //"<span id='tools-btn' />" +
                      "<div id='sf-header-wrap'>"+
                          "<div class='sfheader'>Superfish Events Log</div>" + 
                          "<div id='filters'><span class='label'>Filter By:</span></span><span id='free'><input class='filter' type='text'/><span id='clear'>X</span></span></div>" +
                          "<table cellspacing='0' cellpadding='0' id='entries-header'><tbody><tr>" + 
                                "<th class='label time'><span>Time</span></th>" +
                                "<th class='label level'><span>Level</span></th>" +
                                "<th class='label text'><span>Event</span></th>" +
                                "<th class='label source'><span>Source</span></th>" +
                                "<th class='label url'><span>click to open</span></th>" +
                          "</tr></tbody></table>" +
                      "</div>" +
                      "<div id='entries-wrap'><table cellspacing='0' cellpadding='0' id='entries'><tbody></tbody></table></div>" +
                  "</div>";
    var entryHtml = "<tr class='entry'>" + 
                        "<td class='label time'><span></span></td>" +
                        "<td class='label level'><span></span></td>" +
                        "<td class='label text'><span></span></td>" +
                        "<td class='label source'><span></span></td>" +
                        "<td class='label url' ><a target='_blank' href='#'>click to open</a></td></tr>";
    var urlBox = "<div id='url-box'><div><span class='pointer'></span><a target='_blank' href='' id='api'>open api service<a href='' target='_blank' id='search'>open search service</a></div></div>";
    
    
    /*private methods:*/
    function addLevel(a) {
        levels.push(a);
    }
    
    function isNewLevel(a) {
        if(a) {
            for(var i = 0; i < levels.length; i++) {
                if(a == levels[i]) return false;
            }
            return true;
        }
    }
    
    //create a new entry, add it to the stack and print it.
    //urlParams may be href string or json object
    function log(msg, level, source, urlParams) {
        if (superfish.b && superfish.b.qsObj && superfish.b.qsObj.sflog == "-999") {
        level = level ? level.toLowerCase() : null;
        if(stack.length >= maxStackSize) stack.shift();
        if(isNewLevel(level)) addLevel(level);
        var ts = new Date();
        
        var entry = {
            time: ts,
            timeString: getTimeLabel(ts), 
            text: msg.text || msg,
            level: level || defaultLevel,
            source: source || defaultSource,
            url: urlParams,
            index: stack.length
        };
        
        stack.push(entry);
        print(entry);
        return true;
        }
        else {
            return false;
        }
    }
    
    function print(entry) {
        //if print is called b4 jquery loaded, add event to print buffer.
        if(typeof $ !== 'function') {
            printBuffer.push(entry);
        }
        else {
            if(printBuffer.length > 0) {
                for(var i = 0 ; i < printBuffer.length; i++) {
                    addEventRow(printBuffer.pop());
                }
            }
            addEventRow(entry);
        }
    }
    
    function addEventRow(entry) {
        var row = $(entryHtml);        
        if(activeFilter == 'all' || activeFilter === entry.level) $(row).show();    
        else $(row).hide();            
        $(row).addClass(entry.level);
        $(row).prop('id', entry.index);
        if(stack.length%2 === 0) $(row).addClass('alt');
        $('.time span',row).text(entry.timeString);
        $('.level span', row).text(entry.level.toUpperCase());
        $('.text span', row).text(entry.text);
        $('.source span', row).text(entry.source);
        if(entry.url) {
            if(entry.level !== 'search') {
                $('.url a', row).attr('href', entry.url);
            }
            $('.url a', row).css('display', 'block');
        }        
        $(entries).append(row);
        $(entries).parent().prop({ scrollTop: $(entries).parent().prop("scrollHeight") });
    }
    
    function setFilter(level) {
        activeFilter = level;
        if(level == 'all') $('.entry', entries).show();
        else {
            $('.entry:not(.'+level.toLowerCase()+')', entries).hide();
            $('.entry.'+level.toLowerCase(), entries).show();   
        }
    }
    
    function setPreferences(p){
        var val = p;
        var exp=new Date();
        exp.setDate(exp.getDate() + 365);
        val = escape(val) + ((exp==null) ? "" : "; expires="+exp.toUTCString());
        document.cookie = prefCookie + "=" + val;
    }
    
    function getPreferences()
    {
        var i,x,y,jar =document.cookie.split(";");
        for (i = 0; i < jar.length; i++) {
            x = jar[i].substr(0,jar[i].indexOf("="));
            x = x.replace(/^\s+|\s+$/g,"");
            
            if (x == prefCookie) {
                y = jar[i].substr(jar[i].indexOf("=")+1);
                return unescape(y);
            }   
        }
        return false;
    }
    
    function getTimeLabel(ts) {
        var h = ts.getHours().toString();
        var m = ts.getMinutes().toString();
        var s = ts.getSeconds().toString();
        var ms = ts.getMilliseconds().toString();        
        return h + ":" + (m.length > 1 ? m : "0"+m) + ":" + (s.length > 1 ? s : "0"+s)  + ":" + (ms.length > 2 ? ms : (ms.length > 1 ? "0"+ms : "00"+ms));
    }
        
    function togglefilters(a) {
        if(a == 'show' || parseInt($(filters).css('height'),10) == 0) {
            $(filters).animate({height:50}, 200);
        } 
        else {
            $(filters).animate({height:0}, 200);
        }
    }
    
    function exportStack(level) {
        if(level && level.length > 0) {
            var items = [];
            for(var i = 0; i < stack.length; i++) {
                if(stack[i].level == level) items.push(stack[i]);
            }
            return items;
        }
        return stack;
    }
    
    function openUrl(a, params) {
        try {
            params = $.parseJSON(params);
        }
        catch(e) {
            params = 0;
            log('error parsing JSON params for openUrl()', 'error');
        }
        if(params) {
            var pos = $(a).position();
            $(urlBox).css('left', parseInt(pos.left, 10)-200);
            $(urlBox).css('top', parseInt(pos.top, 10)+20);
            $('#api', urlBox).attr('href', buildApiUrl(params));
            $('#search', urlBox).attr('href', buildSearchUrl(params));
            $(a).parent().append(urlBox);
            $(urlBox).show();
        }
    }

    function buildApiUrl(p){
        
        return "http://ia1-p:10009/apiservice/debug?"+ 
            "runtype=byParams"+
            "&session="+p.sessionid+
            "&imageUrl="+p.imageURL+
            "&imageTitle="+p.imageTitle+
            "&documentTitle="+p.documentTitle+
            "&imageRelatedTitle="+p.imageRelatedText+
            "&productUrl="+p.productUrl+
            "&merchantName="+p.merchantName+
            //"&partnerID=&imageType=&sourceId=&identicalOnly=&country=&minimumQuality=
            "&pageType="+p.pageType; //&presentationType=&siteOrigin=&cardPriorities=";
    }
    
    function buildSearchUrl(p){
        return "http://wa1-p:7004/Search/debug?"+
            "session="+p.sessionid+
            "&requestType=byUrl"+
            "&url="+p.imageURL+
            "&imageTitle="+p.imageTitle+
            "&documentTitle="+p.documentTitle+
            "&imageRelatedText="+p.imageRelatedText+
            "&pageUrl="+window.location.href; //&partnerId=&country=";
    }
          
    function init(jquery) {
        if(!dom) {
            $ = jquery;
            dom = $(logHtml);
            $('head').append('<link rel="stylesheet" type="text/css" href="http://www.superfish.com/ws/css/events_log.css">');            
            $('body').append(dom);
            filters = $('#filters', dom);
            entries = $('#entries', dom);
            urlBox = $(urlBox);
            for(var i = 0; i < levels.length; i++){
                $('#free', filters).before("<button class='filter' type='button' value='"+levels[i]+"'>"+levels[i]+"</button>")
            }            
            //bind ui events:
            $('button.filter', filters).click(function() {
                $('button.filter', filters).removeClass('active');
                $(this).addClass('active');
                var filter = $(this).text();
                setFilter(filter);
                setPreferences(filter);
            });            
            $('#clear', filters).click(function() {
                $('input[type="text"]', filters).val('').focus();                
            });            
            $('input[type="text"]', filters).keyup(function(e) {
                if($(this).val() == '') setFilter('all');
                else {
                    for(var i = 0; i < levels.length; i++) {
                        if($(this).val() == levels[i]) {
                            setFilter(levels[i]);
                        }
                    }
                }
            });

            $(entries).on('click', '.search .url a', function(e) {
               var entryId = $(this).closest('tr').prop('id');
               var entry = stack[entryId];
               openUrl(this, entry.url); //entry.url is params json               
               if(e.preventDefault) e.preventDefault();
               else e.returnValue = false;
               return false;
            });
            
            $("#entries-wrap", dom).scroll(function(){
                $("#url-box", dom).hide();
            });
            
            var filter = getPreferences();
            if(filter) {
                $('button.filter[value="'+filter+'"]', filters).click();
                setFilter(filter);
            }
            else {
                $('button.filter[value="'+defaultFilter+'"]', filters).click();
            }
            log('log ready'); 
        }
    }
    
    return {
        init: init,
        reportEvent: log,
        get: exportStack
    };
    
}();

var originalJq = window.jQuery,
correctJqVersion = originalJq ? originalJq.fn.jquery === '1.7.1' : false;
if (superfish.b && superfish.b.qsObj && superfish.b.qsObj.sflog == "-999") {
    if(!correctJqVersion) {
        yepnope([{
            load: "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js?111",
            callback: function(){
                (function() {
                    spsupport.events.init(jQuery);
                })();
            }
        }]);
    }
    else {
        spsupport.events.init(jQuery);
    }
}
        
        superfish.b.site="https://www.superfish.com/ws/";
        superfish.b.ip="1.1.1.1";
        superfish.b.userid=superfish.b.qsObj.userId;
        superfish.b.appVersion="12.2.9.0";
        superfish.b.clientVersion=(superfish.b.qsObj.clientVersion || superfish.b.qsObj.dlsource);

        superfish.b.wlVersion="6.1";
        superfish.b.wlOldVersion="6.0";
        superfish.b.wlDestDate="2013.05.14";
        superfish.b.wlStartDate="2013.05.08";

        superfish.b.cpnVersion="36";
        superfish.b.cpnOldVersion="35";
        superfish.b.cpnDestDate="2013.04.14";
        superfish.b.cpnStartDate="2013.04.08";

        superfish.b.cdnUrl="http://ajax.googleapis.com/ajax/libs/dojo/1.5.1/";
        superfish.b.pluginDomain="https://www.superfish.com/ws/";
        superfish.b.dlsource="diigo";
        superfish.b.sgt=(superfish.b.qsObj.sgt || "");
        superfish.b.statsReporter=(superfish.b.qsObj.statsReporter == "true");
        superfish.b.CD_CTID=superfish.b.qsObj.CTID;
        superfish.b.w3iAFS=(superfish.b.qsObj.w3iAFS || "");
        

superfish.b.images='diigo';
superfish.b.partnerCustomUI=0;
superfish.b.bl='|lesaubaines.com|laredoute.fr|bloomberg.com|delta-search.com|architecte3d.com|blogger.com|zazzle.com|mycouponbuddy.com|leobell.net|fotosnaturaleza.es|www.easymobility.co.uk|www.theground-up.com|www.thegroundup-ssi.com|portail.dartybox.com|gadgets-toons-cadeaux.com|mercadolibre.com.ar|mercaodlibre.com.co|mercadolibre.com.cr|mercadolibre.com.cl|mercadolibre.com.do|mercadolibre.com.ec|mercadolibre.com.mx|mercadolibre.com.pa|mercadolibre.com.pe|mercadolibre.com.pt|mercadolibre.com.uy|mercadolibre.com.ve|mercadolivre.com.br|mercadolivre.com|abajournal.com|alexa.com|autotrader.com|baidu.com|bedandbreakfast.com|bernadettelivingston.com|beso.com|birdviewprojects.com|bizrate.com|booking.com|cam4.com|cj.com|cnn.com|crunchyroll.com|cvsphoto.com|dcinside.com|deviantart.com|drudgereport.com|facebook.com|flickr.com|furniture-quest.com|history.com|hotmail.com|imdb.com|imvu.com|linkedin.com|lolhehehe.com|lowpriceshopper.com|microsoft.com|mercadolivre.com|msn.com|myspace.com|netflix.com|nytimes.com|pandora.com|picasa.com|pinterest.com|politico.com|polybags4less.com|pricegrabber.com|publicstorage.com|qq.com|rue89.com|salon.com|searchenginewatch.com|sfgate.com|shopzilla.com|shutterfly.com|sommerfrischeamsemmering.wg.vu|spardeingeld.com|techcrunch.com|usamm.com|verizon.com|venturebeat.com|westsiderentals.com|wired.com|yankodesign.com|yahoo.com|youtube.com|';
superfish.b.addBl='|123inkjets.com|24hourfitness.com|4inkjets.com|6pm.com|att.com|adobe.com|adorama.com|shop.com|advanceautoparts.com|audible.com|autopartswarehouse.com|avenue.com|backcountry.com|basspro.com|bestbuy.com|bodenusa.com|brooksbrothers.com|carbonite.com|celebrateexpress.com|chainlove.com|chegg.com|competitivecyclist.com|dell.com|departmentofgoods.com|dogfunk.com|endless.com|ftd.com|footsmart.com|gamefly.com|gamehouse.com|gap.com|garmin.com|golfnow.com|hp.com|snapfish.com|hsn.com|harryanddavid.com|homedecorators.com|homedepot.com|lenovo.com|lightinthebox.com|lowes.com|musiciansfriend.com|newegg.com|overstock.com|petco.com|qvc.com|quill.com|rei.com|shindigz.com|shoebuy.com|shopbop.com|skinstore.com|store.com|sony.com|staples.com|strawberrynet.com|tirerack.com|harryanddavid.com|footsmart.com|plaingreenloans.com|fansedge.com|hottopic.com|ecampus.com|gotomypc.com|buycostumes.com|keen.com|crucial.com|altrec.com|blair.com|smoothfitness.com|callawaygolfpreowned.com|fonts.com|perfumania.com|graveyardmall.com|wbshop.com|framesdirect.com|lids.com|fragrancex.com|tracfone.com|cyberlink.com|golfsmith.com|trendmicro.com|ingdirect.com|shoemall.com|fossil.com|autoanything.com|shopperschoice.com|josbank.com|bodycandy.com|fanatics.com|coffeeforless.com|marylandsquare.com|oakley.com|softsurroundings.com|realcyclist.com|roxio.com|entirelypets.com|lens.com|steepandcheap.com|stamps.com|shoeline.com|vitaminshoppe.com|masoneasypay.com|rosettastone.com|cooking.com|shopjustice.com|dog.com|bird.com|fish.com|masseys.com|thinkgeek.com|venturebeat.com|whiskeymalitia.com|polybags4less.com|pricegrabber.com|zappos.com|sears.com|';
superfish.b.cdnJQUrl='http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
superfish.b.arrFill='#dadee2';
superfish.b.arrBorder='#356595';
superfish.b.supportedBy="Search All Similar Products (to disable)";
superfish.b.shareMsgProd='Search All';
superfish.b.shareMsgUrl='www.smarterfox.com/superfish';
superfish.b.inimg=1;
superfish.b.theme=2;
superfish.b.abTheme=1;
superfish.b.inimgSrp=1;
superfish.b.txtExtr=false;
superfish.b.psuSupportedBy=1;
superfish.b.psuSupportedByText='by Search All';
superfish.b.psuSupportedByTitle='Click for More Information';
superfish.b.inimgSupportedByLink='';
superfish.b.isPublisher=false;
superfish.b.multiImg=0;
superfish.b.ignoreWL=0;
superfish.b.icons=1;
superfish.b.spLogoClick=0;
superfish.b.sfDomain='www.superfish.com';
superfish.b.partnerLogoLink='javascript:superfish.util.bCloseEvent(document.getElementById(\"infoBtn\"), 2);';
superfish.b.partnerFooterLink='javascript:superfish.util.bCloseEvent(document.getElementById(\"infoBtn\"), 2);';
superfish.b.searchget=0;
superfish.b.sgAllenby=0;
superfish.b.stDt=1;
superfish.b.rvDt=100;
superfish.b.sgSupportedByLink='http://www.searcho.com/superfish.html';
superfish.b.sgPrompt='The Search All Visual <br>Search engine will be <br>disabled for';
superfish.b.sgSleepTime=1000*60*60*24;
superfish.b.sgSleepText='24 hours';
superfish.b.lgWi='232';
superfish.b.lgHe='45';
superfish.b.lgTo='8';
superfish.b.drWi='260';
superfish.b.drLf='';
superfish.b.iButtonLink='';
superfish.b.sgIc=1;
superfish.b.noIcon=0;
superfish.b.slideup=0;
superfish.b.slideupSrp=0;
superfish.b.iiHv=0;
superfish.b.secMd='1';
superfish.b.sgSupportedByText='Search All';
superfish.b.cpn='0|0';
superfish.b.topPpc=0;
superfish.b.cpnWLver='35';
superfish.b.cpnWLcb='SF_cpnWlCb';
superfish.b.rvWLver='3';
superfish.b.rvWLcb='SF_isRvURISupported';
superfish.b.lp=0;
superfish.b.sfsrp=0;
superfish.b.redIcon=0;
superfish.b.whiteIcon=0;
superfish.b.largerIi=1;
superfish.b.reportNoneSite=0;
superfish.b.logoText='Search All';
superfish.b.noPopup=0;
superfish.b.inImgDt=1; 
superfish.b.at=0; 
superfish.b.pipLinksExists='1234amazon.com1234|1234pgpartnet.com1234|1234dealtime.com1234|1234ebay.com1234';
superfish.b.pipKeywordInDomain='store1234|buy1234|estore';
superfish.b.pipBrandInDomain='american ironhorse|aprilia|arctic cat|austin healey|benelli|big dog|bimota|bombardier|boss hoss|bourget|bsa|buell|bultaco|can am|cushman|daewoo|datsun|delorean|desoto|desperado|ducati|eagle|edsel|ferrari|geo|greeves|harley davidson|hodaka|husaberg|husqvarna|hyosung|indian|infiniti|international harvester|isuzu|jaguar|jeep|kawasaki|koenigsegg|ktm|kymco|lancia|land rover|lifan|maybach|mg|mini|moto guzzi|mv agusta|nash|norton|opel|qlink|ram|rolls royce|royal enfield|saab|scion|sea doo|smart|titan|triumph|ural|vento|vespa|victory|vincent|volkswagen|willys|senseo|lavazza|world jerseys|assos|defeet|descente|gore bike|primal wear|pinarello|bianchi|cervelo|colnago|axiom|skin industries|alex evenings|joie|just cavalli|js boutique|js collections|ellsworth|diamond back|cannondale|noritake|maxim lighting|arroyo craftsman|minute mirth|gary fisher|jamis|mia shoes|mighty fine|miss sixty|callaway golf|access lighting|craftmade|marc ecko|marc jacobs|top knobs|sport tek|safco|sabrina silver|mezco|paul fredrick|ebc|tri mountain|petit bateau|schlage|source naturals|hal leonard|hudson lighting|sc sports|silver jeans|simple shoes|propper|techno earth|flow snowboards|flow snowboarding|gabriella gold|fox head|french connection|graham spencer|giordana|joy carpets|zip heaters|powers collectibles|alessi|all clad|zac posen|aqua brass|mountain plumbing|tibi|spring step|minka lavery|hansgrohe|martini|southern comfort|johnny walker|international silver|j renee|price pfister|trina turk|sue wong|walker|comfy feet|louis garneau|moog|proform|elizabeth james|evan picone|merrell|music legs|my oilcloth|lbl lighting|rbk|rider jeans|sonia jewels|duragadget|mens wearhouse|quiksilver|saucony|fel pro|kyb|allen edmonds|royal doulton|walking cradles|kwikset|ultra force|velvet eyewear|volcom|wacoal|wicked audio|wonderbra|aetrex|wrangler|aerosoles|tech lighting|breville|border concepts|betty crocker|bialetti|bodum|chicago metallic|casafina|corningware|cook\'s essentials|nature\'s way|pentair|meyle|danner|hotpoint ariston|kenroy home|kidsline|flos|eglo|koldfront|kd dance|outdoor research|smeg|universal housewares|thierry mugler|nanette lepore|womanwithin|dale tiffany|nina ricci|stella mccartney|code luna|vera wang|rachel roy|duravit|nordic ware|norpro|oriental furniture|range kleen|pyrex|office star|2(x)ist|2xist|3com|3m|aarco|abu garcia|accumulair|acer|acura|adesso|adidas|adirondack|adriana papell|affliction|aga|ahava|air king|akai|aldo|alesis|alfa romeo|alfani|all mankind|all star|allure|alpina|alpine|alpinestars|alto shaam|amana|amc|amco|amd|american dj|american range|american standard|amisco|amzer|andis|angry birds|ann taylor|anne klein|antec|apple|apricorn|archos|arcosteel|ariat|ariel|armani|armitron|arri|asics|asko|asko|aston martin|asus|atari|athleta|ati|auburn|audi|audio technica|augusta|aurora|austin|avent|aviator|avon|axis|babette holland|babolat|baby bjorn|baby einstein|baby phat|babyliss|babyvision|badgley mischka|bakers pride|baldwin hardware|balenciaga|bali blinds|ballard designs|banana republic|bandai|bandolino|bar iii|barbie|bare escentuals|basco|battpit|bb dakota|bcbgeneration|bcbgmaxazria|beach handbags|bedford|beeko|behringer|belkin|ben sherman|benetton|benq|bentley|beretta|bern|besa|betty jackson|beverage air|beyblade|bic|billabong|birkenstock|biscotti|bissell|black decker|blackberry|bloch|blodgett|bmw|body glove|bolle|bonnie jean|boonie hat|bosch|bose|boss black|brass accents|braun|breyer|briggs stratton|brita|britax|broan|broil mate|broilmaster|brooks|brother|brylane home|brylanehome|bsn|buffalo boots|bugaboo|bugatti|buick|bulova|bumbleride|burberry|burley|burton|bushnell|bvlgari|cables to|cadent|cadillac|cafepress|cal trend|callaway|calphalon|calvin klein|cambro|cambro|camelbak|campagnolo|camper|canada goose|canon|capezio|care bears|carhartt|carrera|cartier|case logic|casio|casual canine|caterpillar|celestron|chamilia|chaps|char broil|charm bracelet|cheap monday|chevrolet|chicco|chinese laundry|christian audigier|christian dior|christian louboutin|chrysler|cinch|cisco|citizen|citroen|clarion|clarks|clinique|cobian|cobra|coby|cold steel|coldwater creek|cole haan|coleman|colonial mills|columbia sportswear|combi stroller|comfort choice|continental elec|converse|cooler master|coolmax|cord|cosabella|covergirl|coverking|craftsman|crayola|creative recreation|crocs|cross|crown verity|cuisinart|cutter and buck|cyberpower|d link|da lite|dacor|daiwa|dakine|danby|danesco|danskin|dansko|danze|datamax|dc shoes|ddi|de buyer|delfield|dell|delonghi|delta|demarini|denby|denon|denso|desota|deuter|dewalt|dewitt|diadora|diamond audio|diamondback|dickies|diesel|dior|dirt devil|disney|dkny|dockers|dodge|dolan|dolce gabbana|donna karan|donna morgan|dooney bourke|dora explorer|dr martens|dreamgear|dremel|drew shoe|ducane|duke|dunlop|duracell|durex|dw drum|dyeables|dymatize|dymo|dyson|dyson|earrings|earth pan|easton|easy spirit|ecco|echo|eddie bauer|edelbrock|edgestar|edible|eileen fisher|ekco|electrolux|elenco|elizabeth arden|elk lighting|elkay|ella moss|ellen tracy|ellie|emerica|emo|emporio armani|emsco|emtek|endura|energizer|engagement ring|enzo|epiphone|epson|ermanno scervino|escort radar|esp|estee lauder|etnies|evans|evenflo|ever pretty|everlast|evga|ex officio|faded glory|falken|fan mats|farberware|fashion forms|faucet|fein|fellowes|fender|fendi|festool|fiat|fila|firestone|firstgear|fisher paykel|fisher price|fisherprice|fiskars|fitball|fitflop|fitzwell|flexfit|florsheim|fluke|fluval|footjoy|footsmart|ford|ford|forplay|fossil|fox racing|fpv|franco sarto|fred perry|free people|freestyle|frigidaire|friskies|frontier|frontline|fruit loom|frye|fsa|fuji|fujifilm|fujioh|fujitsu|furla|futaba|g star|gap|gardena|garmin|garnier|gateway|ge|general electric|genetic denim|geox|gerber|gestetner|gibson guitar|gigabyte|gildan|gillette|giorgio armani|giro|gitzo|giuseppe zanotti|givenchy|glastender|gmc|gnc|gola|goodyear|graco|gretsch|grillworks|grohe|gucci|guerlain|guess|guidecraft|guillemot|gund|habitat|haier|hallmark|halston|hamilton|hanes|harry potter|hasbro|hatco|hauck|havaianas|heavy duty|heelys|hella|hello kitty|helly hansen|hennessey|hennessy|henry j|herman miller|hershey|hi tec|high sierra|hinkley|hitachi|holden|holley|holster|homedics|homer laughlin|honda|honeywell|hoover|horchow|horizon hobby|hot wheels|hp|hsv|htc|huawei|hubbardton forge|hue|huffy|huggies|hugo|hugo boss|hummer|hurricane toys|hush puppies|hyundai|ibanez|ibm|ibuypower|iittala|ikea|iluv|ilve|imari|incipio|intel|invicta|iomega|izod|j brand|j crew|jabra|jack spade|jakks|jansport|jbl|jeffrey campbell|jensen|jerzees|jessica howard|jessica london|jessica mcclintock|jetboil|jimmy choo|jl audio|jm collection|joe boxer|joes jeans|john deere|joop|joseph joseph|juicy couture|just size|justice design|jvc|k swiss|kalorik|kangol|karcher|karen kane|kate spade|kay unger|keds|keen|kenda|kenmore|kenneth cole|kensie|kensington|kenwood|kettler|keurig|kia|kichler|kichler lighting|kidkraft|kidwise|kikkerland|kindle|kinect|kinerase|kingston|kingston brass|kipling|kirby|kitchenaid|kleenex|klipsch|kms|knex|kodak|konica|kooba|koolertron|korg|korres|koss|kryptonite|kuhn rikon|kumho|kyocera|kyosho|la made|lacie|lacoste|lacrosse|lamaze|lamborghini|lancome|lange boot|lange boots|lange ski|lansinoh|lasalle|laura ashley|lazy susan|le creuset|leapfrog|leatherman|lee|leg avenue|lego|leica|lekue|lenmar|lenovo|lenox|lesportsac|levis|lexar|lexmark|lexus|lg|libbey|liberty hardware|lifefactory|lilly pulitzer|lincoln|linksys|lite source|little pony|little tikes|liz claiborne|logitech|longchamp|loreal|lotus|louisville slugger|lucky brand|ludwig|luminox|lynx|m audio|mac|mackie|maclaren stroller|mad catz|magellan|maggy london|magnaflow|majestic athletic|makita|manfrotto|mango|maruti|maserati|mattel|mauviel|mavic|maxell|maxi-cosi|maxi cosi|maxicosi|maxxis|maybelline|maytag|mazda|mbt|mcfarlane|mcgraw hill|mclaren|medela|medion|melissa doug|mercedes|mercedes benz|mercedes-benz|mercury|meritor|merona|merrell|metabo|metal fusion|metal mulisha|metropolitan vacuum|michael antonio|michael kors|mickey friends|mickey mouse|microsoft|miele|mikasa|miller welders|minnetonka|minolta|mintcraft|minton|miraclesuit|missoni|mistubishi|mitsubishi|mitchell ness|mizuno|moen|mongoose|monster cable|montegrappa|moon climbing|mossimo|motorola|mountain hardwear|movado|msi|msr|mtd|mtx|munchkin|murray feiss|music skins|naot|napoleon|nashbar|natrol|naturalizer|nature made|nautica|navitech|ncstar|nec|neca|neff|neiman marcus|nerf|netgear|neutrogena|new balance|newport brass|nike|nikon|nine west|nintendo|nirve|nissan|nite ize|nitto|nivea|nokia|nokian|nordic ware|nordica|norpro|north face|now foods|nuby|numark|nutcase|nvidia|nylabone|oakley|oki|okuma|olay|oldsmobile|olympus|omas|omega|omnia|omron|oneill|oneill|onkyo|opi|optimum nutrition|optoma|oral b|oreck|original penguin|osram|oster|otterbox|oxo|pacific play|packard|paco rabanne|pagani|pampers|panache|panasonic|pantech|parker pen|patagonia|paul smith|payot|pearl izumi|peavey|peg perego|pelco|pelikan|pentax|perfume|perodua|perry ellis|petmate|petsafe|peugeot|pfaltzgraff|philips|phylrich|pierce arrow|pikachu|pikolinos|pilot|piloti|pioneer|pirelli|pixi|planet bike|plantronics|playkids|playmobil|playskool|playstation|playtex|pleaser|plymouth|pny|polaris|polaroid|polk audio|pontiac|porsche|pottery barn|poulan|power acoustik|powerwarehouse|powr flite|prada|prepac|primigi|pro tec|proaire|procter gamble|proform|progress lighting|propet|ps3|puma|purely pets|purina|pyle|pyramid|quicksilver|quinny|quoizel|quorum|qupid|rachel pally|radio flyer|ralph lauren|rapala|rashguard|ravensburger|rawlings|ray ban|razor|recaro|red devil|red dot|reebok|renault|revlon|revo|ricoh|rieker|riobel|rip curl|rocawear|rocket dog|rockford fosgate|rockport|rohl|rolls royce|roocase|ros hommerson|roshco|ross simons|rotary|roxy|royal doulton|rubbermaid|rubies costume|ruger|rvca|ryobi|sabre|saeco|safavieh|safety 1st|safety first|saint laurent|saitek|saleen|sally hansen|salvatore ferragamo|sam edelman|samsonite|samsung|sandisk|sansa|santoni|sanuk|sanyo|sassy|satco|saturn|saucony|sauder|savoy house|schleich|scholastic|schwinn|scosche|scotsman|scotts|screwpull|seagate|sebago|sebo|sega|seiko|sennheiser|sesame street|sharp|shelby|shimano|shirley hollywood|shiseido|shock absorber|shoei|shop vac|shopvac|shure|siemens|skechers|skinit|sklz|skoda|skullcandy|smart4two|smirnoff|smith wesson|sog|sony|sony ericsson|spalding|spanx|sparco|speck products|speedo|sperry top|spiderman|spongebob squarepants|spri|stamina|stanton|star wars|steelseries|step2|sterling|stetson|steve madden|stila|stride rite|stuart weitzman|studebaker|stuhrling|stx|stylecraft|subaru|summer infant|suncast|sunshine kids|super pet|sure fit|surya|suunto|suzuki|swanstone|swatch|swiss army|swiss gear|swiss legend|sylvania|syma|t tahari|tablet|tag heuer|talbots|tama|tamron|tappan|targus|tata|taylor made|techfuel|ted baker|tefal|tesla|teva|thermaltake|thermos|things remembered|thomas engine|thomas train|thrustmaster|thule|timberland|timex|tippmann|tissot|titleist|tommy bahama|tommy hilfiger|tomtom|tomy|topeak|topps|torker|torrid|tory burch|toshiba|touch ups|tous|toy story|toyo|toyota|trane|trans globe|transcend|travel smith|traxxas|treadmill|trendnet|triumph|troy lighting|true religion|tumi|u line|ugg|ujena|umbro|under armour|undergear|unicel|uniden|uniflame|usp|uttermost|valeo|vaneli|vans|vaude|vera bradley|verbatim|versace|vestal|vibram|vichy|victorias secret|victorinox|viewsonic|viking|villeroy boch|vince camuto|vinotemp|vivitar|vizio|volks wagen|volvo|vulcan hart|vutec|wac|wahl|walco|waterman|weathertech|weber|wedgwood|weekender|wellco|wesc|western digital|westinghouse|whirlpool|wii|wiley|wilson|wilton|winchester|winnie pooh|wmf|wonderbra|wonderworld|woodard|wwe|xbox|xerox|xhilaration|yamaha|yankee candle|yonex|zagg|zara terez|zeiss|zildjian|zippo';
superfish.b.CPMSites='google;surfcanyon';
superfish.b.CPMSupportedTypes=';wl;';
superfish.b.awakeEnabled=0;
superfish.b.CPMEnabled=0;
superfish.b.vvCookie='sf_valid_version';
superfish.b.vvDlsources='mozilla,w3i,openinstaller';
superfish.b.checkAppVersion=0;
superfish.b.urlDel='_$_';
superfish.b.uninstCookie='sf_uninstall';
superfish.b.uninstCookieCoupons='sf_uninstall_coupons';
superfish.b.inimgDisplayBox=2;
superfish.b.inImageextands=1;
superfish.b.inimgExploreBecomeSearch=0;
superfish.b.inimget=0;
superfish.b.testBp=0;
superfish.b.dlsrcEnableCpnPip=1;

    if (superfish.b && superfish.b.qsObj && superfish.b.qsObj.CTID) {
        superfish.b.partnerLogoLink = superfish.b.partnerLogoLink.replace("prdct=allPrdcts", "prdct=" + superfish.b.qsObj.CD_CTID);
        superfish.b.partnerFooterLink = superfish.b.partnerFooterLink.replace("prdct=allPrdcts", "prdct=" + superfish.b.qsObj.CD_CTID);
        superfish.b.sgSupportedByLink = superfish.b.sgSupportedByLink.replace("prdct=allPrdcts", "prdct=" + superfish.b.qsObj.CD_CTID);
    }
    
    if (navigator.userAgent.toLowerCase().indexOf("msie") > -1){
        superfish.b.checkAppVersion = 0;
    }
    superfish.b.uc = "--";



        superfish.clientVersion = superfish.b.qsObj.clientVersion || "-1";
        
        superfish.info = {
    infoId: 'SF_SA_INFO',
    infoOn: 0,
    infoHt: 380,
    isCustomActionEnabled: 0,
    from: 0,
    h: 394,
    w: 324,
    ifrh: 345,
    ci: function(sfDomain, dlsource, userid, CD_CTID, ver, theme) {
        var t = this;
        var css = 'display:none;z-index:1990000;-moz-user-select: none;-khtml-user-select:none;user-select:none;width:324px;height:394px; background: transparent;',
            cssIfr = 'z-index:200005;width:323px;height:'+(t.infoHt - 35)+'px;overflow-x: hidden;overflow-y: hidden;top:25px;left:0;padding:0;position:absolute; background: url(' + sfDomain + 'images/bgp.png) repeat-y scroll -1742px 0 transparent;';
//        if (theme == 2) {
//            css = 'display:none;z-index:1990000;-moz-user-select: none;-khtml-user-select:none;user-select:none;width:324px;height:394px; background: transparent;';
//            cssIfr = 'z-index:200005;width:323px;height:'+(t.infoHt - 35)+'px;overflow-x: hidden;overflow-y: hidden;top:25px;left:0;padding:0;position:absolute; background: url(' + sfDomain + 'images/bgp.png) repeat-y scroll -1742px 0 transparent;';
//        }    
        return ["<div id='"+ t.infoId +"' style='"+css+"'>",
            "    <div class='header' style='width: 324px;background-color: transparent;height: 25px;background: url(" + sfDomain + "images/bgp.png) -1094px 0 transparent;'><div onmouseout='SF.infoEvent(this, 0);' onmouseover='SF.infoEvent(this, 1);' onclick='SF.infoEvent(this, 2);' id='infoClose'></div>"+
                    "<div class='closeButton' style='width:19px;height:19px;background: url(" + sfDomain + "images/bClose.png) 0 0 no-repeat;position:absolute;top:3px;right:4px;cursor:pointer;'></div>"+
                 "</div>",
            "   <iframe  id='"+ t.infoId +"_CONTENT' allowTransparency='true' src='" + t.getInfoSrc(sfDomain, dlsource, userid, CD_CTID, ver, theme) + "' style='"+cssIfr+"' scrolling='yes' frameborder='0'></iframe>",
            "<div class='footer' style='height: 35px;width: 324px;bottom: 0;background-color: transparent;background: url("+ sfDomain +"images/bgp.png) -1418px 0 transparent;position:absolute; top:350ox;'></div>",
            "</div>"
            ].join('');    
    },
        
    getInfoSrc: function(sfDomain, dlsource, userid, CD_CTID, ver, theme) {
            if (!theme) {
                theme = 1;
            }
            var q = [],
                path = sfDomain + "iPage.jsp?";                
            q.push("dlsource=" + dlsource);
            q.push("userid=" + userid);
            q.push("CTID=" + CD_CTID);
            q.push("ver=" + ver);
            q.push("theme=" + theme);
            return path + q.join('&');
    },
    
    ev: function(css, from, type) {
        if(this.isCustomActionEnabled) {
             if(typeof this.customActions[superfish.b.qsObj.dlsource] == 'function') {
                 this.customActions[superfish.b.qsObj.dlsource]();
             }
        }
        else {
            if (!this.infoOn) {
                this.open(css, from, type);
            }
            else {
                if (this.infoOn == from) {
                    this.close();
                }
                else {
                    this.jInfo.hide()
                    this.open(css, from, type);
                }
            }
        }
    },
    
    open: function(css, from, type) {
        this.infoOn = from;
        if (!css) {
            css = {};
        }
        css.height = 4;
        css. width = 4;
        var ht, ifrHt;
        if (type == 2) {
            ht = 100;
            ifrHt = 50;
        }
        else {
            ht = this.h;
            ifrHt = this.ifrh;
        }
        this.jIfr.css({
            'height' : ifrHt
        });
        this.jInfo.css(css).show()
        .animate({
            'height': ht + 'px',
            'width': this.w + 'px'
        }, 600, null, function(){});
    },
    
    close: function() {
        var t = this;
        t.infoOn = 0;
        t. from = 0;
        t.jInfo.animate({
            'height': 4,
            'width': 4
        }, 600, null, function(){
            t.jInfo.hide()
        });
    },
    customActions: {
        conduit: function() {
            if(typeof TPI != 'undefined' && typeof TPI.Manager == 'function') {
                var oManager = new TPI.Manager();
                if(typeof oManager != 'undefined' && typeof oManager.SendMessage == 'function') {
                    oManager.SendMessage("superfish-mam-msg", "whatsThisLinkClicked");
                }
            }
        }
    }
};
        
        
        superfish.b.cpn = superfish.utilities.blacklistHandler.getCpnData();

        superfish.b.secMd = (+superfish.b.secMd);
        if (window.location.protocol.indexOf( "https" ) > -1 && !superfish.b.secMd) return;
        superfish.b.sm = (window.location.protocol.indexOf( "https" ) > -1 ? 1 : 0);
        superfish.b.pluginDomain = (superfish.b.sm ? superfish.b.pluginDomain.replace("http:","https:") : superfish.b.pluginDomain.replace("https","http"));
        superfish.b.tg = "";
        superfish.b.xdMsgDelimiter = "*sfxd*";
        superfish.b.fullUIMaxHeight = 0;
        spsupport.whiteStage = {
    $: 0,
    st: 0,
    rv: 0,
    wl: 0,
    pip: 0,
    domain: '',
    bl: '',
    html: '',
    h1Data: [],
    prc: false,
    de: 0,
    validReason:'',
    matchedBrand:'',
    isCheckout: false,
    siteType: '',
    isWLCallbacks: {
        successCallback: "",
        failedCallback: "",
        timeout: null,
        urlToValidate:""
    },
    checkSiteTypeParams:{
        pipProps: null,
        checkoutProps: null,
        finishCallback: ''
    },
    
    stDt: [{},
        {   // 1 - english
            lng: '',
            cntr: '',
            lngRx: /a/gi,
            lngNum: 30,
            stRx: /(add\s?(item)?\s?to\s?(my)?\s?(shopping|digital)?\s?(cart\b|bag\b|basket|order))|(free|no anxiety) shipping|shipping (charges|policy|options)|(continue|start|safe|secure|no minimum) shopping|order status|(refund|return) policy|easy (replacement|return)|(my|your|view|show) \bcart\b|shopping (\bcart\b|\bbag\b|\bbasket\b|categories)|(\bwatch|wish)\s?list\b|gift voucher|bulk orders|cash (purchase|on delivery)|replacement (guarantee|options)|(fast|ontime) delivery/ig,
            stNum: 1                       
        },
        {   // 2 - german
            lng: 'de',
            cntr: 'de|at|ch',
            lngRx: /[äöü\u00E4\u00F6\u00FC]/gi,
            lngNum: 30,
            stRx: /warenkorb|mein ((benutzer)?konto|account)|einkaufen|einkaufs(liste|-?wagen|tasche)|express-(zustellung|lieferung)|(meine |kostenfreie |standard |24-stunden-|speditions)lieferung|rück(sendungen|versand|gabe|nahme)|liefer(status|zeit)|sofort-kaufen|versand|mwst|bestellen|bestellung|wunsch(zettel|liste)|wish list|merkzettel|gutschein|geschenkkarte|widerruf|zur kasse gehen/ig,
            stNum: 1   
        },
        {   // 3 - french
            lng: 'fr',
            cntr: 'fr|ca',
            alter: 5,
            lngRx: /[àâæçéèêëîïôœùûÿ\u00E0\u00E2\u00E6\u00E7\u00E8\u00E9\u00EA\u00EB\u00EE\u00EF\u00F4\u00F6\u00F9\u00FB\u00FF]/gi,
            lngNum: 40,
            stRx: /a\s?joutez\s?au\s?(panier|comparateur)|(votre|mon|voir le) panier|panier d\'achat|préférés|spécial soldes|en soldes|livraison (offerte|gratuite|à domicile sur rendez-vous)|je retourne par la poste|(livré|disponible) sous|retours (acceptés|gratuits)|reprise ou achange gratuit|enchères|enchèrir|commander\s?(\(?en ligne\)?)?|continue[rz]? (vos|mes) (achats|continuer) le shopping|liste objets désirés|listes d\'envies|commandé|prochainement disponible/ig,
            stNum: 1   
        },
        {   // 4 - spanish
            lng: 'es',
            cntr: 'es',
            lngRx: /[áéíñóú\u00E1\u00E9\u00ED\u00D3\u00F1\u00F3\u00FA]/gi,
            lngNum: 30,
            stRx: /iniciar compra|políticas de envío|envío (gratuito|gratis)|envíos y gastos envío|comprar ya en 1-clic|(tu|mi|ir|la|a) cesta|ver carrito|lista de (favoritos|deseos)|mi boisa|cheques regalo|añadir a cesta|devolución y envío gratuitos/gi,
            stNum: 0   
        },
        {   // 5 - italian
            lng: 'it',
            cntr: 'it',
            lngRx: /[àèéìíîòóùú\u00E0\u00E9\u00E8\u00EC\u00ED\u00EE\u00F2\u00F3\u00F9\u00F9]/gi,
            lngNum: 20,
            stRx: /prenota ora|spedizioni|spese di (consegna|spedizione|trasporto)|spedizione gratuita|aggiungi al carrello|(servizio|modalità) di spedizione|pagamento per contrassegno|\bacquista\b|articoli selezionati|\bordina\b|vai alla cassa|continua shopping|(stato|storico) ordini|buono acquisto|diritto di recesso|carrello|pagamenti rateali|buoni (sconto|regalo)|lista (dei )?desideri|proseguire l\'ordine|mio account|restituire/ig,
            stNum: 1   
        },  
        {   // 6 - portuguese
            lng: 'pt',
            cntr: 'pt|br',
            lngRx: /[áâãàçéêóôõú\u00E1\u00E2\u00E3\u00E0\u00E7\u00E8\u00EA\u00F3\u00F4\u00F5\u00F9]/gi,
            lngNum: 20,
            stRx: /carrinho|(meus|seus) pedidos|acompanhe seus pedidos|entrega|trocas|devoluções|minha (conta|cesta)|meu cadastro|lista de (desejos|presentes|casamento)|super descontos|FRETE GRÁTIS|comprar (este|produto|agora|com 1-click|com garantia)|caixa expresso|envio imediato|em estoque|meu caminhão/ig,
            stNum: 1   
        },  
        {   // 7 - india
            lng: '',
            cntr: 'in',            
            lngNum: 20,
            stRx: /(add\s?(item)?\s?to\s?(my)?\s?(shopping|digital)?\s?(cart\b|bag\b|basket|order))|(fast|ontime) shipping|shipping (charges|policy|options)|(continue|safe|secure|no minimum) shopping|order status|return policy|easy (replacement|return)|cart item|(my|your|view|show) shopping (\bcart\b|\bbag\b|\bbasket\b|categories)|(your|view|show) \bcart\b|wish\s?list|cash (purchase|on delivery)|replacement guarantee/ig,
            stNum: 1   
        },  
        {   // 8 - mexico
            lng: 'es',
            cntr: 'mx',
            lngRx: /[áéíñóú\u00E1\u00E9\u00ED\u00D3\u00F1\u00F3\u00FA]/gi,
            lngNum: 30,
            stRx: /\bcomprar\b|(mi|su) cuenta|(envío|entrega a domicilio|para cambio) gratis|(mi|ver) carrito|(mis?|ver estado del) pedido|\bagregara\b|forma de envío|políticas de garantías y devoluciones|pago contra entrega|tiendas online|bolsa de compra|orden rápida|lista de deseos/gi,
            stNum: 0   
        },  
        {   // 9 - holland
            lng: '',
            cntr: 'nl|be',
            lngRx: /\baan\b|\bachter\b|\bbinnen\b|\bboven\b|\bbij\b|\bdaar\b|\bdat\b|\bdeze\b|\bdit\b|\bdoordat\b|\been\b|\bhet\b|\bhoe\b|\bmaar\b|\bmet\b|\bnaar\b|\bnaast\b|\bnabij\b|\bomdat\b|\bomhoog\b|\bonder\b|\bop\b|\brond\b|\btegen\b|\btenzij\b|\bterwijl\b|\btoen\b|\btotdat\b|\btot\b|\btussen\b|\buit\b|\bvan\b|\bvoor\b|\bvoordat\b|\bzoals\b|\bzodat\b|\bzonder\b|\bna\b/gi,
            lngNum: 20,
            stRx: /(in )?winkelmand|shopping leeg|gratis (bezorgd en retour|verzend|retour|ruilen|bezorgd|bezorging)|verder winkelen|shopping\s?bag|veilig online shoppen|levering (1 á 3|in 2-5) werkdagen|(bestel|shop) nu|verlanglijst|verzendkosten|retourneren en reclameren|retourkosten|wishlist|(in( de)?|mijn) winkelwagen|naar kassa|klik & bestel|retourgarantie|ruilen en retourneren/gi,
            stNum: 0   
        }  
        
    ],
    
    init: function(jq){
    	this.$ = jq;
    },
    
    /**
     * Check the site type and if the checked page is checkout page
     */
	checkSiteTypeAndIsCheckoutPage: function(pipProps, checkoutProps,sfBaseUrl,wlUrl,wlVersion,finishCallback){
        this.checkSiteTypeParams.pipProps = pipProps;
        this.checkSiteTypeParams.checkoutProps = checkoutProps;
        this.checkSiteTypeParams.finishCallback = finishCallback;

	    this.isWLPage(document.location.host,this.checkSiteTypeAndIsCheckoutPageCB,this.checkSiteTypeAndIsCheckoutPageCB,sfBaseUrl,wlUrl,wlVersion);
	},

	checkSiteTypeAndIsCheckoutPageCB: function(wlData,whiteStageObj){

            //set if the page is checkout page
	        whiteStageObj.setIsCheckoutPage(whiteStageObj.checkSiteTypeParams.checkoutProps);

	        if (whiteStageObj.wl){
	            whiteStageObj.siteType = "wl";
	            if(typeof whiteStageObj.checkSiteTypeParams.finishCallback === 'function') {
	                whiteStageObj.checkSiteTypeParams.finishCallback();
	            }

	            return;
	        }

    		if(whiteStageObj.isCheckout || whiteStageObj.isStore()){
    			whiteStageObj.siteType = "st";
    		}else if (whiteStageObj.isReview()){
    			whiteStageObj.siteType = "rv";
    		}else if(whiteStageObj.isProductInPage(whiteStageObj.checkSiteTypeParams.pipProps)){
    			whiteStageObj.siteType = "pip";
    		}else{
    			whiteStageObj.siteType = "other";
    		}

    		if(typeof whiteStageObj.checkSiteTypeParams.finishCallback === 'function') {
                whiteStageObj.checkSiteTypeParams.finishCallback();
            }
    	},
    
    isDomain: function(){
        var d = this.getDomain().toLowerCase();
        this.domain = d;
        d = d.split('.');
        
        var o = d[d.length-1];
        if ( this.bl.indexOf('|'+ this.domain + '|') == -1 ) {
            if (o == 'com' || o == 'net') {
                var url = document.location.href;
                if (url.indexOf('/fr/') > -1) {
                    return 3;
                }
                else if (url.indexOf('/de/') > -1) {
                    return 2;
                }
                else if (url.indexOf('/es/') > -1) {
                    return 4;
                }
                else {
                    return 1;
                }
            }
            else if (o == 'fr' || o == 'ca') {               
                return 3;
            }
            else if (o == 'es') {               
                return 4;
            }
            else if (o == 'it') {               
                return 5;
            }
            else if (o == 'br' || o == 'pt') {               
                return 6;
            }
            else if ( o == 'de' ||
                o == 'at' ||
                o == 'ch' ){
                    return 2;
            }
            if (o == 'in') {
                return 7;
            }
            if (o == 'mx') {
                return 8;
            }
            if (o == 'nl' || o == 'be') {
                return 9;
            }
            
            if ( o == 'au' || (o == 'uk' && d[d.length-2] == 'co') || (o == 'nz' && d[d.length-2] == 'co') || (o == 'au' && (d[d.length-2] == 'co' || d[d.length-2] == 'com'))) {
                return 1;
            }
        }
        return 0;
    },
    
    getDomain: function(){
        return this.getDomainByUrl(document.location.host);
    },

    getDomainByUrl: function(url){
            var dD = url;
            var dP = dD.split(".");
            var len = dP.length;
            if ( len > 2 ){
                var co = ( dP[ len - 2 ] == "co" || dP[ len - 2 ] == "com" ? 1 : 0 );
                dD = ( co ? dP[ len - 3 ] + "." : "" ) + dP[ len - 2 ] + "." + dP[ len - 1 ];
            }
            return dD;
        },
    
    arrUn: function(arr) {
        if (arr) {    
            var a = [];
            var l = arr.length;
            for(var i=0; i<l; i++) {
                for(var j=i+1; j<l; j++) {
                    // If arr[i] is found later in the array
                    if (arr[i].toLowerCase() === arr[j].toLowerCase())
                        j = ++i;
                }
                a.push(arr[i]);
            }
            return a;
        }
        else{
            return arr;
        }
    },
    
    lngDt: function(lng) {
        var e;        
        if (lng > 1) {
            if (this.stDt[lng].lngRx) {
                e = this.html.match(this.stDt[lng].lngRx);
                if (!e || (e && e.length < this.stDt[lng].lngNum)) {
                    lng = 1;
                }
            }
        }
        else if (lng == 1) {
            for (var i = 2; i < this.stDt.length; i++) {
//                spsupport.log(i);
//                spsupport.log(this.stDt[i]);
                e = this.html.match(this.stDt[i].lngRx);
//                spsupport.log(e);
//                spsupport.log(e ? e.length : "nothing catched");
                if (e && e.length > this.stDt[i].lngNum) {
                    lng = i;
                    break;
                }
            }
        }
        return lng;
    },

    isStore: function(){
    	this.st = 0;
        var lng = this.isDomain();
//        spsupport.log("lng = " + lng);
        if (!lng) {
            return this.st;
        }
        
        this.html = this.$('body').html();
        if (!this.html) {
            this.html = "";
        }
        
        var irl = this.html.match(/[ğş]/gi);
        if (irl && irl.length > 20) {
            return this.st;
        }
        
        var url = window.location.href;
        url = url.replace(/[\+-_]/g, ' ');
        var inUrl = url.match(/shop|marketplace|kaufen|boutique/gi);
        
        if (inUrl) {
            //this.matchedBrand =  "In URL: " + this.arrUn(inUrl).join(" | ").replace(" | undefined","");
            this.validReason =  "In URL: " + this.arrUn(inUrl).join(" | ").replace(" | undefined","");
            this.st = 1;            
        }
        else {        
            lng = this.lngDt(lng);
//            spsupport.log("lng2 = " + lng);
            var c, d;

            var eur = /(([\$\£]|eur|rs)(<[^>]+>|&nbsp;|\s)?([0-9]+\,)?[0-9]+)|((([0-9]+,)?[0-9]+)(<[^>]+>|&nbsp;|\s|\s\,\-\s)?eur?)/ig;
            var eurSign = /[\€\u20AC]/gi;
            var num = /[0-9]+\,[0-9]+/ig;
            
            if (lng > 1) {
//                spsupport.log("lng > 1  " + lng);
//                spsupport.log(this.stDt[lng].stRx);
                c = this.html.match(this.stDt[lng].stRx);
//                spsupport.log(c);
                if (!c) {
                    if (this.stDt[lng].alter) {
                        c = this.html.match(this.stDt[this.stDt[lng].alter].stRx);
                    }
                }
                if (c && c.length > this.stDt[lng].stNum) {
                    if(this.html.match(eurSign)) {
                        d = this.html.match(num);
                    }
                    else {
                        d = this.html.match(eur);
                    }
                }
            }
            else {
                c = this.html.match(this.stDt[lng].stRx);
                if (c) {
                    d = this.html.match(/([\$\£]|eur|rs)\s?(<[^>]+>|&nbsp;)?([0-9]+\,)?[0-9]+\.?[0-9]+/ig);
                }
            }

            //spsupport.log(c);
            //spsupport.log(d);
            if (d && c) {
                this.st = 1;
                //this.matchedBrand =  this.arrUn(c).join(" | ").replace(" | undefined",""); // + this.arrUn(d).join(" | ").replace(" | undefined","");
                this.validReason =  this.arrUn(c).join(" | ").replace(" | undefined","");             
            }
        }
        return this.st;
    },
    
    chCt: function(ct, pc) {
        var ln = ct.split('|').length;
        ln = parseInt(ln*pc/100);
        var p = new RegExp(ct, 'gi');
        var r = this.txt.match(p);
        r = this.arrUn(r);
        if (r.length >= ln) {
            return 1;
        }
        return 0;
    },

    isReview: function() {
    	this.rv = 0;
        if (!this.isDomain()) {
            return 0;
        }
        this.txt = this.$('body').text();
        
        var p = this.txt.match(/[\$\£]\s?(<[^>]+>|&nbsp;)?([0-9]+\,)?[0-9]+\.?[0-9]+/ig);
        var r = this.txt.match(/review/gi);   
        var c = this.txt.match(/comment|rating|newsletter|rss|recommend/gi);
        var m = this.txt.match(/bluetooth|\bfax\b|\bbattery\b|\bcharger\b|\bgps\b|\bstereo\b|speaker|\bradio\b|subwoofers|\btv\b|projector|\bdvd\b|\bMP3|\bMP4|\bipod\b|clock|microphones|cameras|monitors|camcorder/gi);
        if(p && r && c && m) {
            this.rv = 1;
        }
        return this.rv;
    },
    
    isProductInPage: function(pipProps){
    		var pipKeywordInDomain, pipBrandInDomain, pipLinksExists;
    		pipKeywordInDomain = (typeof(superfish) != "undefined" ? superfish.b.pipKeywordInDomain : pipProps["pipKeywordInDomain"]);
    		pipBrandInDomain = (typeof(superfish) != "undefined" ? superfish.b.pipBrandInDomain : pipProps["pipBrandInDomain"]);
    		pipLinksExists = (typeof(superfish) != "undefined" ? superfish.b.pipLinksExists : pipProps["pipLinksExists"]);
            this.pip = 0;
//            this.addText = '';
            
//            if (this.isDomain() == 0) {
//                return this.pip;
//            }
           if (pipLinksExists && this.$('a:regex(href,'+ pipLinksExists + ')').length > 0){
                    this.pip = 1;
                    this.validReason  = "links in page";
            }

            if (pipKeywordInDomain.substring(0,2) != "\b"){
                pipKeywordInDomain = "\\b"+ pipKeywordInDomain.replace(/\|/g,"\\b|\\b") + "\\b";
                pipBrandInDomain = "\\b"+ pipBrandInDomain.replace(/\|/g,"\\b|\\b") + "\\b";
            }
            
            var rBrands = new RegExp(pipBrandInDomain, 'gi'),
                rKeywords = new RegExp(pipKeywordInDomain, 'gi');
            this.rBrands = rBrands;  
            
            var pipBrandArrRst;
            if (!this.pip && pipKeywordInDomain){
                var url = window.location.href;
                url = url.replace(/[\+-_]/g, ' ');
                pipBrandArrRst = url.match(rKeywords);
                if (pipBrandArrRst) {
                    this.pip = 1;
                    this.validReason = "keywords in url";
                } 
                pipBrandArrRst = url.match(rBrands);
                if (pipBrandArrRst != null && pipBrandArrRst.length > 0 ){
                    this.pip = 1; 
                    this.validReason = (this.validReason ? this.validReason + " and " : "") + "brands in url";
                    this.matchedBrand =  pipBrandArrRst;
                }
            }

            if (pipBrandInDomain){
                pipBrandArrRst = this.$(document).attr('title').match(rBrands);
                if (pipBrandArrRst != null && pipBrandArrRst.length > 0 ){ 
                    this.pip = 1;    		
                    this.validReason  = (this.validReason ? this.validReason + " and " : "") + "brand in title";
                    this.matchedBrand = this.matchedBrand ? this.matchedBrand.concat(pipBrandArrRst) : pipBrandArrRst; 
                }
            }

            if (pipBrandInDomain){ // checking H1
                var jH1 = this.$('h1'); //.text();
                var tx = '', del = '***', h1s; 
                if (jH1 && jH1.length) {
                    jH1.each(function() {
                        tx += spsupport.p.$(this).text() + del;
                    });
                    tx = tx.replace(/( |\s){2,}/ig, ' ');  
                    h1s = tx.split(del);      // array of h1 texts
                    h1s.splice(h1s.length-1, 1);
                    // spsupport.log(h1s);
                    this.h1Brands(h1s, rBrands);
                    // spsupport.log(this.h1Data);
                }
            }
            
            if (this.matchedBrand) {
                if (this.matchedBrand.length == 1 && this.validReason.indexOf("keywords in url") == -1) {
                    if (this.matchedBrand[0].length < 3 || this.domain.indexOf(this.matchedBrand[0]) == 0) {
                        this.pip = 0;
                    }
                }
                this.matchedBrand = this.arrUn(this.matchedBrand);
                this.matchedBrand = this.matchedBrand.join(" | ").replace(" | undefined","").toLowerCase();
                //this.matchedBrand = this.matchedBrand.toLowerCase();
            }
            return this.pip;
    }, 
    
    h1Brands: function(h1s, rBrands){
        this.h1Data = [];
        var mb = [];
        var len = Math.min(h1s.length, 20);
        // spsupport.log("h1s length = " + h1s.length);
        for (var i = 0; i < len; i++) {
            mb = h1s[i].match(rBrands);
            if (mb != null && mb.length > 0 ){
                this.h1Data[this.h1Data.length] = {
                    'mb': mb,
                    'tx': h1s[i]
                }
            }
        }

        if (this.h1Data && this.h1Data.length) {
            this.pip = 1;
            this.validReason  = (this.validReason ? this.validReason + " and " : "") + "brand in H1";
            //this.matchedBrand = this.matchedBrand ? this.matchedBrand.concat(pipBrandArrRst) : pipBrandArrRst;
        }
    },
    
    setIsCheckoutPage: function(checkoutProps){
        var docText = this.$(document).text().toLowerCase();
    	var mandatoryWords = checkoutProps["mandatory"];
    	mandatoryWords =  "\\b" + mandatoryWords.replace(/\|/g,"\\b|\\b") + "\\b";
    	var regMv = new RegExp(mandatoryWords, 'gi');
    	var manIsMatch = docText.match(regMv);
    	
    	if(manIsMatch && manIsMatch.length > 0){
    		var optionalWords = checkoutProps["optional"];
    		optionalWords =  "\\b" + optionalWords.replace(/\|/g,"\\b|\\b") + "\\b";
    		var optIsMatch = docText.match(optionalWords);
    		if(optIsMatch && optIsMatch.length > 1){
    			this.isCheckout = true;
    		}
    	}
    	if(!this.isCheckout){
    		var url = document.location.href;
    		if(url.toLowerCase().indexOf("checkout") > 0 || url.toLowerCase().indexOf("payment") > 0&& this.$('iframe').length > 0){
    			this.isCheckout = true;
    		}
    	}
    	return this.isCheckout;
    },


    isWLPage: function(urlToValidate,successCallback,failedCallback,sfBaseUrl,wlUrl,wlVersion){
            if (!urlToValidate)
                return;

            var supportedUrl;

            if (typeof(spsupport) != "undefined" && typeof(spsupport.p) != "undefined" && typeof(superfish) != "undefined" && typeof(superfish.b) != "undefined" ){
 //               supportedUrl = spsupport.p.sfDomain_ + "getSupportedSitesJSON.action?ver=";
                //supportedUrl = this.getRightVersion.chooseVer(supportedUrl, superfish.b.wlStartDate, superfish.b.wlEndDate, superfish.b.wlOldVersion, superfish.b.wlVersion)
//                console.log("a1");
                supportedUrl = spsupport.p.sfDomain_ + "getSupportedSitesJSON.action?ver=" + superfish.b.wlVersion;
            } else {
                supportedUrl = sfBaseUrl + "/" + wlUrl  + "?ver=" + wlVersion;
//                console.log("a2");
            }

            this.isWLCallbacks.urlToValidate = urlToValidate;
            this.isWLCallbacks.successCallback = successCallback;
            this.isWLCallbacks.failedCallback= failedCallback;

            window["sfwsobj"] =this;
            window["SF_isURISupported"] = this.isWLPageCallbackSuccess;

            this.isWLCallbacks.timeout = setTimeout(this.isWLPageCallbackFailed,6100);

            var script = document.createElement('script');
            script.setAttribute('src', supportedUrl);
            script.setAttribute('id', 'SF_isURISupported_call');
            script.setAttribute('type', 'text/javascript');

            document.documentElement.firstChild.appendChild(script);


    },

    isWLPageCallbackSuccess: function(data){
        var whiteStageObj= window["sfwsobj"];
        clearTimeout(whiteStageObj.isWLCallbacks.timeout);
        whiteStageObj.isWLCallbacks.timeout = null;

        var domain = whiteStageObj.getDomainByUrl(whiteStageObj.isWLCallbacks.urlToValidate);

        if (data.supportedSitesMap[domain])
             whiteStageObj.wl = 1;
        else
             whiteStageObj.wl = 0;

        if(typeof whiteStageObj.isWLCallbacks.successCallback === 'function') {
            whiteStageObj.isWLCallbacks.successCallback(data,whiteStageObj);
        }
    },

    isWLPageCallbackFailed: function(){
        var whiteStageObj= window["sfwsobj"];
        clearTimeout(whiteStageObj.isWLCallbacks.timeout);
        whiteStageObj.isWLCallbacks.timeout = null;

        whiteStageObj.wl = 0;

        if(typeof whiteStageObj.isWLCallbacks.failedCallback === 'function') {
            whiteStageObj.isWLCallbacks.failedCallback();
        }
    }


}

;
        if (superfish.b.dlsource.indexOf("ginyas") != -1 & window.location.href.toLowerCase().indexOf("amazon.com") != -1) return;
        spsupport.whiteStage.bl = superfish.utilities.blacklistHandler.getWSBlacklist();

        superfish.utilities.sfWatcher.setState("sf-code-load-site-rules");
        spsupport.pip = {
    imgs: [],
    imgPos: {},
    displ: 0,
    ii: 0,
    br: [], // brands array
    c: 0,   // priority counter
    req: 0,
    dim: 160,
    secDim: 120,
    lvl: 1500,
    secArr: [],
    bannedImages: ';apple.com_callout_download.png;apple.com_hero.png;',
    start: function(sS) {
        if (superfish.inimg) {
            spsupport.api.addSuperfishSupport();
            spsupport.p.supportedImageURLs = sS.imageURLPrefixes;
            spsupport.p.merchantName = sS.merchantName;
            spsupport.api.siteType();
            spsupport.statsREP.init();
            this.analyze();
        }
    },
    
    analyze: function() {
        var imgs = document.images;
        var a, imNm;
        for(var i=0, l=imgs.length; i < l; i++){
            this.imgPos = spsupport.api.getImagePosition(imgs[i]);
            a = imgs[i].src.split('/');
            imNm = a[a.length-1];
            if (this.bannedImages.indexOf(';'+spsupport.p.merchantName+'_'+imNm) == -1 && this.validDispl(imgs[i])) {
                this.preSend(imgs[i]);
                break;
            }
        }        
        if (!this.displ) {
            for (i in this.secArr) {
                this.imgPos = spsupport.api.getImagePosition(this.secArr[i]);
                this.preSend(this.secArr[i]);
                break;
            }
                
            this.findDispl();
        }
    },
    
    preSend: function(img) {
        var si = superfish.inimg;
        this.displ = img;
        this.ii = si.vi(this.imgPos.w, this.imgPos.h, 1);
        this.ii = spsupport.api.careIi(this.ii, 2);                                   
        si.itNum[si.iiInd] = this.ii;
        if (this.validReq(img)) {
            this.imgReq(img);
        }
        else {
            this.txtReq();
        }
        
    },

    imgReq: function(im) {
        var sp = spsupport.p;
        sp.prodPage.p = im;
        sp.imPos = this.imgPos;
        var ob = spsupport.api.getItemJSON(im);
        ob = this.careTexts(ob);
        this.send(ob, 1);        
    },
    
    txtReq: function() {
        var sp = spsupport.p;
        var ob = {
            userid: encodeURIComponent(sp.userid),
            merchantName: encodeURIComponent(sp.merchantName),
            dlsource: sp.dlsource,
            appVersion: sp.appVersion,
            documentTitle: document.title,
            imageURL: document.title,
            imageTitle: document.title,
            imageRelatedText: '',
            productUrl: ''
        };
        ob = this.careTexts(ob);
        this.send(ob, 0);
    },
    
    compare: function(a,b) {
      if (a.wg > b.wg)
         return -1;
      if (a.wg < b.wg)
        return 1;
      return 0;
    },
    
    processData: function() {
        var ws = spsupport.whiteStage;
        var ln, t1, t2, t3, t4, sp1, sp2, b, t5, t6, i, j;
        for (i in ws.h1Data) {
            ln = (ws.h1Data[i].tx.match(/[ \s]/g)||[]).length;
            if (ln) {
                ln++;
            } 
            t1 = ws.h1Data[i].mb;
            t2 = t1.length;
            for (j in t1) {
                t2 += (t1[j].match(/[ \s]/g)||[]).length;
            }
            ws.h1Data[i].wg = ln - t2;
            if (ws.h1Data[i].wg > 4) {
                t3 = ws.h1Data[i].tx.toLowerCase();
                t4 = t1[0].toLowerCase();
                sp1 = t3.indexOf(' ');
                sp2 = t3.indexOf(' ', sp1);
                b = t3.indexOf(t4);
                if (b > sp2) {
                    ws.h1Data[i].wg++;
                }
                
                t5 = t3.split(t4)[1];
                if (t5) {
                    t6 = (t5.match(/[ \s]/g)||[]).length;
                    if (t6) {
                        t6++;
                    }
                    if (t6 > 2) {
                        ws.h1Data[i].wg++;
                    }
                }
            }
        }

        ws.h1Data.sort(this.compare);
    },
        
    careTexts: function(ob) {
        var ws = spsupport.whiteStage;
        this.c = 0;        
        this.br = ws.matchedBrand ? ws.matchedBrand.split(' | ') : [];
        var br1, br2;
                
        if (ws.h1Data && ws.h1Data.length > 3) {
            this.processData();
        }

        var dt = ob.documentTitle, it = ob.imageTitle, irt = ob.imageRelatedText;
        if (ws && ws.rBrands) {
            if (ws.validReason.indexOf('brand in title') == -1 && ws.h1Data.length > 1) {   // if no brand in title, put there h1
                dt = this.putTxt(dt);
            }
            if (it) {
                br1 = it.match(ws.rBrands);
                if (br1 && br1.length) {
                    this.br = this.br.concat(br1);
                }
                else {
                    it = this.putTxt(it);
                }
            }
            else {
                it = this.putTxt(it);
            }
            
            if (irt) {
                br2 = irt.match(ws.rBrands);
                if (br2 && br2.length) {
                    this.br = this.br.concat(br2);
                }
                else {
                    irt = this.putTxt(irt);
                }
            }
            else {
                irt = this.putTxt(irt);
            }
                        
            if (this.br && this.br.length) {
                this.br = ws.arrUn(this.br);
                this.br = this.br.join(" | ").replace(" | undefined","").toLowerCase();
                ws.matchedBrand = this.br;
            }
        }
        
        ob.documentTitle = dt;
        ob.imageTitle = it;
        ob.imageRelatedText = irt;
        
        return ob;
    },
    
    putTxt: function(target) {
        var ws = spsupport.whiteStage;
        if (ws && ws.h1Data && ws.h1Data[this.c]) {
            target = ws.h1Data[this.c].tx;
            this.br = this.br.concat(ws.h1Data[this.c].mb);
            this.c++;
        }
        return target;
    },
    
    validDispl: function(im) {
        var cndM = this.imgPos.w > this.dim && this.imgPos.h > this.dim;
        var cndS = this.imgPos.w > this.secDim && this.imgPos.h > this.secDim;
        var pos = parseInt(this.imgPos.y + this.imgPos.h - 45);
        var cndL = pos < this.lvl && pos > 0;
        var cndV = this.imgPos.x > 0 && spsupport.api.isVisible(im);
        if(cndL && cndV) {
            if (cndM) {
                return 1;
            }
            else if (cndS) {
                this.secArr[this.secArr.length] = im;
            }
        }
        return 0;
    },
    
    validReq: function(img) {
        return spsupport.api.isImageSupported(img);
    },
    
    send: function(ob, pic) {
        superfish.utilities.sfWatcher.setState("send pip request");
        var sfu = superfish.util;
        if (sfu) {
            var sg = 0; // 8
            if (!this.sent) {
                spsupport.p.prodPage.p = this.displ;
                superfish.util.prepareData(ob, 1, sg, 1, this.ii, 0);
                this.sent = 1;            
                sfu.openPopup(this.imgPos, spsupport.p.appVersion, 1, 1);
                sfu.lastAIcon.x = this.imgPos.x;
                sfu.lastAIcon.y = this.imgPos.y;
                sfu.lastAIcon.w = this.imgPos.w;
                sfu.lastAIcon.h = this.imgPos.h;
                sfu.lastAIcon.img = this.displ;                
                spsupport.p.prodPage.s = 2;
            }
        }
        else {
            setTimeout(function() {
                spsupport.pip.send(ob, pic);
            }, 500);
        }
    },               
    
    findDispl: function() {
        this.jo = spsupport.p.$('embed, object');
        var si = superfish.inimg;
        var o;
        for (var i = 0; i < this.jo.length; i++) {
            o = this.jo[i];
            this.imgPos = spsupport.api.getImagePosition(o);
            if (this.validDispl(o)) {
                this.displ = o;
                this.ii = si.vi(this.imgPos.w, this.imgPos.h, 1);
                si.itNum[si.iiInd] = this.ii;
                this.txtReq();                              
                break;
            }
        }
        
    }
}

;
        spsupport.sites = {
    rules: function(){
        var site = spsupport.api.getDomain();
        site = site.substr(0, site.indexOf(".")).replace(/-/g, "_");
        return spsupport.sites["_" + site];
    },
    
    isBlackList: function() {
        var ourHostName = document.location.host;
        var i,subsHosts;
        if (ourHostName == undefined || ourHostName.length == 0)
            return 0;
        ourHostName = ourHostName.toLowerCase();
        subsHosts = ourHostName.replace(/[^.]/g, "").length; // how many time there are "."
        for(i=0 ; i < subsHosts ; i++) {
            if(spsupport.whiteStage.bl.indexOf("|"+ourHostName+"|") != -1){
                return 1
            }
            ourHostName = ourHostName.substring(ourHostName.indexOf(".")+1,ourHostName.length);
        }
        return 0;
    },

    isBlackStage: function() {
        var r = this.rules();
        if( r && r.isBlackStage ){
            return r.isBlackStage();
        }
        return 0;
    },
    
    topPpc: function(sS) {
        var r = this.rules();
        if( r && r.topPpc ){
            return r.topPpc(sS);
        }
        return 0;
    },
    
    txtSrch: function() {
        var r = this.rules();
        if( r && r.txtSrch ){
            return r.txtSrch();
        }
        return 0;
    },

    isSrp: function() {
        var r = this.rules();
        if( r && r.isSrp ){
            return r.isSrp();
        }
        return 0;
    },

    su: function () {
        var r = this.rules();
        if( r && r.su ){
            return r.su();
        }
        return 11;
    },

    iv: function () {
        var r = this.rules();
        if( r && r.iv ){
            return r.iv();
        }
        return 1;
    },

    care : function(){
        var r = this.rules();
        if( r && r.care ){
            r.care();
        }
    },
    
    offInt: function(){
        var r = this.rules();
        if( r && r.offInt ){
            r.offInt();
        }
    },
    
    firstTimeRep: function(){
        var r = this.rules();
        if( r && r.firstTimeRep ){
            r.firstTimeRep();
        }
    },
    
    searchget: function(){
        var r = this.rules();
        if( r && r.searchget ){
            r.searchget();
        }
    },

    validRefState: function(){ // Valid Refresh State
        var r = this.rules();
        if( r && r.validRefState ){
            return r.validRefState();
        }
        return 1;
    },

    vImgURL: function( iU ){ // Validate IMG URL
        var r = this.rules();
        if( r && r.vImgURL ){
            return r.vImgURL( iU );
        }
        return ( iU );
    },

    preInject : function(){
        var r = this.rules();
        if( r && r.preInject ){
            r.preInject();
        }
    },

    validProdImg : function(){
        var r = this.rules();
        if( r && r.validProdImg ){
            return r.validProdImg();
        }
        return 0;
    },

    imgSupported : function( img ){
        var r = this.rules();
        if( r && r.imgSupported ){
            return r.imgSupported( img );
        }
        return 1;
    },

    ph2bi : function(){ // Plugin has to be injected
        var r = this.rules();
        if( r && r.ph2bi ){
            return r.ph2bi();
        }
        return 0;
    },

    gRD : function(){ // Get Refresh Delay
        var r = this.rules();
        if( r && r.gRD ){
            return r.gRD();
        }
        return 500;
    },

    gVI : function(){ // get Images Node
        var r = this.rules();
        if( r && r.gVI ){
            return r.gVI();
        }
        return 0;
    },
    
    killSg : function(){
        if (superfish.sg) {
            superfish.sg.close();
        }
    },

    killIi : function(){
        if (superfish.ii && superfish.ii.k) {
            superfish.ii.k();
        }
        else if (superfish.inimg && superfish.inimg.ii && superfish.inimg.ii.length) {
            for (var i in superfish.inimg.ii) {
                superfish.inimg.cl(i);
            }
        }    
    },

    killPopup : function(){
        if( superfish.util ){
            superfish.util.closePopup();
        }
    },

    inURL : function( u ){
        return ( typeof u == 'string' && window.location.href.toLowerCase().indexOf( u.toLowerCase() ) > -1);
    },
    
    onUrlChange: function() {
            var spsites = spsupport.sites;
            spsites.killSg();
            spsites.killIi();
            spsites.killPopup();
            spsupport.api.killIcons();

            // restart popup/searchget/inimage
            setTimeout(function(){
                spsupport.p.prodPage.reset();
                spsupport.p.SRP.reset();
                spsupport.api.startDOMEnumeration();                    
            }, 1900);
    },
    
    urlChange: function() {
        // get site specific methods
        var r = this.rules(),
        // default url change function
        urlChange = function(){
            spsupport.sites.onUrlChange();
        };

        // call page specific urlchange rules
        if( r && r.urlChange ){
            urlChange = r.urlChange;
        }
        
        // setup event listener for hashchange
        spsupport.p.$(window).on("hashchange", urlChange);
    },

    sgGen: function() {
        spsupport.p.iSpin = new Image();
        spsupport.p.iSpin.src = spsupport.p.imgPath + 'loading.gif';
    },

    getRelTextPP: function (img){
        superfish.utilities.sfWatcher.setState("getRelTextPP");
        var sfsr = spsupport.sites;
        var closeTxt = "";
        imgPos = spsupport.api.getItemPos(img);
        imgPos.x2 = imgPos.x + imgPos.w;
        imgPos.y2 =  imgPos.y + imgPos.h;
        closeText = sfsr.getTextIfClose(imgPos,"h1",200,200);
        if(closeText == "")
            closeText = sfsr.getTextIfClose(imgPos,"h2",100,100);
        if(closeText == "")
            closeText = sfsr.getTextIfClose(imgPos,"h3",100,100);

        return ({
            prodUrl : "",
            iText : closeText
        });
    },

    getTextIfClose: function(imgPos,slaveNode,maxx,maxy){
        var sp = spsupport.p;
        var spa = spsupport.api;
        var sfsr = spsupport.sites;
        var jq = sp.$;
        var titlePos;
        var itemTitle = jq(slaveNode);
        if(itemTitle.length == 0 || itemTitle.length > 5 ){
            return "";
        }
        var maxDisX = (maxx || 100);
        var maxDisY = (maxy || 100);
        var closeTitles = [];
        for(var i = 0; i< itemTitle.length ; i++){
            titlePos = spa.getItemPos(itemTitle[i]);
            var moveX,moveY;
           if(titlePos.y < imgPos.y){ // means it's above the image.
                moveY = imgPos.y -titlePos.y -titlePos.h;
                if(moveY<0) moveY = 0;
            }
            else if(titlePos.y > imgPos.y2){ // if the title is below the image
                moveY = titlePos.y - imgPos.y2;
            } else if (titlePos.y + titlePos.h >= imgPos.y && titlePos.y + titlePos.h < imgPos.y2){ // title is in range of the image
                moveY = 0;
            }
            if((titlePos.x <= imgPos.x)  && (titlePos.x + titlePos.w >= imgPos.x)){ // title is in rage of image
                    // now i know that it starts at the left and ends close to the image.
                    // i give default distance from image of X ( maximum allowed )
                    moveX = 0;
            }
            else if(titlePos.x > imgPos.x2){ // title is on the left of the image
                moveX = titlePos.x - imgPos.x2;
            }
            if(moveX < maxDisX && moveY < maxDisY){
                itemTitle[i].dis = moveX + moveY;
                closeTitles.push(itemTitle[i]);
            }
        }
        if(closeTitles.length == 0){
            return "";
        }
        else if(closeTitles.length == 1){
            return (jq(closeTitles[0]).text());
        }
        else
        {
            closeTitles.sort(sfsr.distSort);
            return (jq(closeTitles[0]).text());
        }
    },

    distSort: function(a,b){
        if (a.dis < b.dis)
            return -1;
        if (a.dis > b.dis)
            return 1;
        return 0;
    },

    getRelText : function(node){
        superfish.utilities.sfWatcher.setState("getRelText");
        if (node) {
            //default val
            var relTxt = {
                prodUrl: "",
                iText: ""
            };

            // if there's any unique treatment
            var r = this.rules();
            if( r && r.getRelText ){
                var v = r.getRelText( node );
                return ( v ? v : relTxt );
            }
            var jq = spsupport.p.$;
            var spa = spsupport.api;
            var max = 5; // how many levels to go up and find "a"
            var links;
            // finding closest "a"
            jq(node).parents().each(function(index, parent) {
                links = jq(parent).find('a');
                if(index > max || links.length>0) {return false;}
            });
            var lNode = links[0];
            if (lNode) {
                var url = lNode.href;
                var txt = spa.textFromLink(lNode, url);
                var re = new RegExp("<[^>]+>","ig"); //remove nojs codes
                txt = txt.replace(re,"");
                txt = jq.trim(txt);
                return ({
                    prodUrl : url,
                    iText : txt
                });
            }
        }
        return 0;
    },
    
    _seesimilar: {
        care: function() {
            superfish.b.multipleIcons = 1;
        }
    },
    
    _tigerdirect: {
        care: function() {
            spsupport.p.$("#homeCategories").mouseenter(function () {
             setTimeout(function() {
                 spsupport.api.fixIiPos();
             }, 200);
            })
            .mouseleave(
            function () {
             setTimeout(function() {
                 spsupport.api.fixIiPos();
             
            }, 200);
        });
        }
    },
        
    _craigslist: {
        txtSrch: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.useWl(1);
            }
        },
        
        searchget: function() {
            var iu = spsupport.sites.inURL;
            var ssg = superfish.sg;

            if ( superfish.b.searchget && ssg && document.images.length == 0) {
                ssg.offset = 1;
                ssg.itemWidth = 94;
                ssg.cssTitle = 'display:block;padding-top: 3px;max-height:48px; overflow: hidden;';
                ssg.cssPrice = 'font-weight: bold;';
                ssg.cssStore = 'display:block; color:#0E774A;text-decoration: none; width: 90px; overflow: hidden;line-height:15px;';
                ssg.cssPrompt = 'top: 20px; right: -37px;';
                ssg.rPad = 32;
                //ssg.q = this.vQ;
                ssg.q = 'h2.postingtitle';
                ssg.cookie = '_craigslist';
                var jQn = spsupport.p.$(ssg.q);
                if (jQn.length) {
                    superfish.b.multiImg = 1;
                    superfish.publisher.limit = superfish.b.searchget;
                    ssg.sSite = 5;
                }
                if (spsupport.txtSr) {
                    spsupport.txtSr.dt = spsupport.txtSr.data['craigslist'];
                    var dd = spsupport.txtSr.gd(window.location.host);
                    dd = dd.split('.');
                    var ext = dd[dd.length-1];
                    var coun = ext == 'com' ? 'us' : (ext == 'de' || ext == 'fr' || ext == 'uk' ? ext : '');
                    //spsupport.log(">>>>>>>>> dd = " + dd );
                    spsupport.txtSr.dt.mn = spsupport.txtSr.dt.mn + (coun ? '-' + coun : '');
                    spsupport.txtSr.jAnc = jQn;
                }
                spsupport.sites.sgGen();
            }
        },

        checkIsGoodImage: function(img,imgPos){
            var bi = 900;
            var imgGood = 1;
            if (img.width > bi || img.height > bi || imgPos.x < 0 || imgPos.y < 10) {
                imgGood = 0;
            }
            return imgGood;
        },

        ph2bi : function(){return 1;},

        isBlackStage: function() {
            var txt = '';
            var jNd = spsupport.p.$('a[href$="/sss/"]');
            txt = jNd.length ? jNd[0].innerHTML : '';
            if (txt.indexOf('for sale / wanted') > -1) {
                spsupport.p.textOnly = 1;
                return 0;
            }            
            return 1;
        },
        
        fNd: function(nd) {
            var txt = '';
            txt += spsupport.p.$('h2').text();
            txt = txt.replace(/[\n\r\t\*]/gi, '');
            txt = spsupport.p.$.trim(txt);
            txt = txt.split('Location:')[0];
            txt = txt.substring(0, 990);            
            return txt;
        },
        
        getRelText : function(node){
            if (node) {
                var txt = this.fNd(node);
                return {
                    prodUrl: '',
                    iText: txt                                        
                };
            }
            return 0;
        }        
    },

    _forever21 : {

        getParentText: function( robj ){
            var obj = robj;
            var foundText = "";
            if( !obj || !obj.parentNode || obj === document || obj.id == "product_rr")
                return "";

            foundText = spsupport.p.$(obj).find(".ItemName").text();
            if(foundText == "")
                foundText = spsupport.p.$(obj).find(".DisplayName").text();
            if(foundText == "")
                foundText = spsupport.p.$(obj).find(".product-title").text();
            if(foundText == ""){
                var tmp = spsupport.p.$(obj).find("a").not(".jqzoom");
                foundText = (tmp.length > 0) ? tmp[0].text : "";
            }
            if(!foundText || foundText == "")
                return this.getParentText( obj.parentNode );
            else
                return foundText;
        },

        getRelText : function(node){
            if (node) {
                var txt = this.getParentText(node);
                return {
                    prodUrl: '',
                    iText: txt
                };
            }
            return 0;
        }

    },

    _google : {

        isBlackStage: function() {
            if(spsupport.p.isIE7) {
                return true;
            }
            if (spsupport.sites.inURL('/reader/') || spsupport.sites.inURL('/contacts/') || spsupport.sites.inURL('/calendar/')) {
                return true;
            }
            return 0;
        },

        vQ: 'li#productbox, li.g.knavi, #rhs, #taw, .g:has(.r a[href^="/products/catalog"])',
        vQm: '#rhs, #taw',
        
        topPpc: function(sS) {
            var sp = spsupport.p;
            superfish.b.inj(window.document, superfish.b.site + "top20/get.jsp?pi=" + sp.dlsource + "&ui=" + sp.userid + "&cc="+ sp.CD_CTID +"&mn="+ sS.merchantName + "&v=" + sp.appVersion, 1);
        }, 
        
        iv: function() {return 0;},

        urlChange : function(){
            var spsites = spsupport.sites;
            spsupport.api.killIcons();
            spsites.killSg();
            spsites.killIi();
            spsites.killPopup();
            spsupport.p.prodPage.reset();
            spsupport.p.SRP.reset();
            spsites._google.prodImg = 0;
            setTimeout(function() {
                spsupport.sites._google.isIacOnlySearch()
                spsupport.sites._google.vIcons();
            }, 500);
        },

        isIacOnlySearch: function(){
            if(superfish.b.qsObj.dlsource == "iacbundle"){
                superfish.b.icons = 0;
            }
        },

        care : function(){
            var db = spsupport.p.$('body');
            spsupport.p.minImageArea = 58*58;
            if(db && db.length && !db[0].evAdded){
                this.isIacOnlySearch();
                db.on( "keydown", function(e){
                    if(spsupport.p.$("input:focus").length > 0){
                        var ch;

                        if(e && e.which){
                            ch = e.which;
                        }else if( window.event ){
                            ch = window.event.keyCode;
                        }
                        if(ch == 13) {
                            spsupport.sites.killSg();
                            spsupport.sites.killIi();
                            setTimeout(function() {
                                spsupport.sites._google.vIcons();
                            }, 500);
                        }
                        else{
                            spsupport.api.killIcons();
                            spsupport.sites.killIi();
                        }
                    }
                });
                db[0].evAdded = 1;
            }
        },

        firstTimeRep: function(){
            spsupport.sites._google.validateREP();
        },

        searchget: function() {
            var iu = spsupport.sites.inURL;
            var ssg = superfish.sg;
            if ( superfish.b.searchget && ssg ) {
                ssg.offset = 0;
                ssg.itemWidth = 94;
                ssg.cssTitle = 'display:block;padding-top: 3px;max-height:48px; overflow: hidden;';
                ssg.cssPrice = 'font-weight: bold;';
                ssg.cssStore = 'display:block; color:#0E774A;text-decoration: none; width: 90px; overflow: hidden;line-height:15px;';
                ssg.cssPrompt = 'top: 20px; right: -37px;';
                ssg.rPad = 40;
                ssg.q = '#rso li';
                ssg.cookie = '_google';
                var jQn = spsupport.p.$(ssg.q);

                if (jQn.length) {
                    superfish.b.multiImg = 1;
                    superfish.publisher.limit = superfish.b.searchget;
                    ssg.sSite = 5;
                }
                if (iu("products/catalog")) {
                    ssg.sSite = 0;
                }
                else if (iu("books.google") ||  iu( "tbs=shop" ) || iu( "tbm=shop" ) || iu( "tbs=bks" ) || iu("tbm=bks") ) {
                    ssg.sSite = 0; /* to enable slide-up instead of searchget */
                }
                
                if (spsupport.txtSr) {
                    spsupport.txtSr.dt = spsupport.txtSr.data['google'];
                    var dd = spsupport.txtSr.gd(window.location.host);
                    dd = dd.split('.');
                    var ext = dd[dd.length-1];
                    var coun = ext == 'com' ? 'us' : (ext == 'de' || ext == 'fr' || ext == 'uk' ? ext : '');  
                    spsupport.txtSr.dt.mn = spsupport.txtSr.dt.mn + (coun ? '-' + coun : '');
                    spsupport.txtSr.jAnc = jQn;
                }
                spsupport.sites.sgGen();
            }
        },
        
        txtSrch: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.useWl();
            }
        },
        
        validateREP : function (){
            var iu = spsupport.sites.inURL;
            if (!(iu("?tbm=") || iu("&tbm=") || !iu("q=") )) {
                spsupport.statsREP.reportStats(spsupport.statsREP.repMode.CPM);
            }
        },

        gVI : function (){
            var iu = spsupport.sites.inURL;
            return ( iu("books.google") || iu("google.com/shopping") || iu("tbm=bks") || iu("tbs=bks") || iu("products/catalog") ) ?
            0 : spsupport.p.$('img.th, img.productthumb, img.rhsg4, .psliimg > img, .pla-unit-img-container img');
        },

        vIcons : function(){
            var ssg = superfish.sg;
            setTimeout(
                function(){
                    spsupport.sites._google.validateREP();
                    var ss = spsupport.sites;
                    var sa = spsupport.api;
                    var iu = ss.inURL;
                    var im = ss._google.gVI();
                    var jQn = spsupport.p.$(ss._google.vQ);
                    superfish.publisher.imgs = [];
                    superfish.publisher.reqCount = 0;
                    superfish.publisher.valCount = 0;
                    if (spsupport.txtSr) {
                        spsupport.txtSr.jAnc = jQn;
                        spsupport.txtSr.sent = 0;
                    }

                    if( jQn.length ){
                        if (ssg) {
                            ssg.sSite = 5;
                        }
                            sa.startDOMEnumeration();
                            setTimeout( function(){
                                sa.wRefresh( 500 );
                            }, 900 );
                    }
                    else {
                        if (ssg) {
                            ssg.sSite = 0;
                        }
                        if( iu("tbs=shop") ||  iu("tbm=shop") ){
                            sa.startDOMEnumeration();
                            setTimeout( function(){
                                sa.wRefresh( 350 );
                            }, 900 );
                        }
                        else if(  iu("books.google" ) || iu("tbs=bks") || iu("tbm=bks")) {
                            sa.startDOMEnumeration();
                            setTimeout( function(){
                                sa.wRefresh( 350 );
                            }, 900 );
                        }
                    }
                }, 1400 );
        },

        ph2bi : function(){
            return 1;
        },

        validRefState : function(){
            var iu = spsupport.sites.inURL;
            // match query for supported google pages
            return  ( 
                spsupport.p.$(this.vQ).length
                || iu("tbs=shop")
                || iu("tbm=shop")
                || iu("products/catalog" )
                || iu("books.google" )
                || iu("tbm=bks")
                || iu("tbs=bks")
                || iu("google.com/shopping")
                );
        },

        preInject : function(){
            var iu = spsupport.sites.inURL;
            var sIU = spsupport.p.supportedImageURLs;
            if ( sIU ){
                sIU[sIU.length] = "jpg;base64";
                sIU[sIU.length] = "jpeg;base64";
            }
            else{
                sIU = ["jpg;base64", "jpeg;base64"];
            }

            if(iu("books.google")){
                var wN = spsupport.p.$('div[id *= "_sliders"]')
                if(wN.length){
                    wN.each(function() {
                        spsupport.domHelper.addEListener(this, spsupport.api.onDOMSubtreeModified, "DOMSubtreeModified");
                    });
                }
            }
        },

        validProdImg : function(){
            if( spsupport.p.$( this.vQ ).length && !this.prodImg ){
                this.prodImg = 1;
                return 1;
            }
            return 0;
        },

        imgSupported : function( im ){
            if( im.id && im.id.indexOf("vidthumb")> -1 ||
                im.className.indexOf("vidthumb") > -1 ||
                im.className.indexOf("imgthumb") > -1 ){
                return 0;
            }
            return 1;
        },

        getRelText : function(node){
            if (node) {
                var spa = spsupport.api;
                var lNode = spa.getLinkNode(node, 3);
                if (lNode) {
                    var url = lNode.href;
                    var pUrl = "";
                    if( url.indexOf( "javascript" ) == -1 ){
                        if( url.indexOf("http://www.google.com/url?") > -1 ){
                            var pSign = url.indexOf("=");
                            if( pSign > -1 ){
                                url = url.substr( pSign + 1, url.length );
                            }
                        }
                        try{
                            url = decodeURIComponent( url );
                        }catch(e){
                        // not encoded
                        }
                        var prm = url.indexOf("&");
                        if( prm > -1 ){
                            url = pUrl = url.substr(0, prm);
                        }
                        var sec = node;
                        var cl = 0;
                        for (var i = 0; i < 20; i++) {
                            sec = sec.parentNode; 
                            if (sec && sec.getAttribute) {
                                cl = sec.getAttribute('class');
                                if (cl && cl.indexOf('knavi') > -1 || sec.nodeName == 'body') {
                                    break;
                                }
                            }
                            else { 
                                break; 
                            }
                        }
                        var txt = '';
                        if (!txt) {
                            txt = this.moreRelText(lNode);
                        }
                    }
                    return({
                        prodUrl : ( pUrl != "" ? pUrl : lNode.href ),
                        iText : txt
                    });
                }
            }
            return 0;
        },
        
        moreRelText: function(lNode) {
            var txt = '';
            if (lNode) {
                var parent = lNode.parentNode;
                for (var i = 0; i < 4; i++) {
                    if (parent) {
                        var a = spsupport.p.$('a', spsupport.p.$(parent));
                        txt = a.text();
                        if (txt) {
                            break;
                        }
                        else {
                            parent = parent.parentNode;
                        }
                    }
                }
            }
            if (txt.length > 70) {
                txt = txt.substring(0, 69);
            }
            return txt;
        },
        
        su : function(){
            return 1;
        }
    },
    
    _macys : {
        care : function(){
            setTimeout( function(){
                spsupport.sites._macys.paging();
            }, 1000 );
        },

        urlChange : function(){
            if( !spsupport.sites._macys.evtc ){
                spsupport.api.killIcons();
                setTimeout( function(){
                    spsupport.p.prodPage.reset();
                    spsupport.p.SRP.reset();
                    spsupport.api.startDOMEnumeration();
                }, 1700 );
                setTimeout( function(){
                    spsupport.api.wRefresh( 300 );
                }, 2700 );
                setTimeout( function(){
                    spsupport.sites._macys.paging();
                }, 3500 );
            }
        },
        
        paging : function(){
            var pgn = spsupport.p.$('.paginationSpacer');
            if(pgn.length){
                setTimeout(function(){
                    pgn.each(                            
                        function() {
                            var tDel = 1500;
                            spsupport.p.$(this).on('mouseup', function(){
                                spsupport.api.killIcons();
                                spsupport.sites._macys.evtc = 1;
                                setTimeout( function(){
                                    spsupport.api.startDOMEnumeration();
                                }, tDel );
                                setTimeout( function(){
                                    spsupport.api.wRefresh( tDel / 3 );
                                },  tDel * 2 );
                                setTimeout( function(){
                                    spsupport.sites._macys.paging();
                                }, tDel * 2.5 );
                            });
                        });
                }, 1400);
                this.evtc = 0;
            }
        }
    },
    
    _bing : {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },
        
        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('bing');
            }
        }
    },

    _yahoo : {
        vImgURL : function( u ){
            var uD = u.split( "http" );
            if( uD.length > 2 ){
                uD = uD[ 2 ];
            }else if( uD.length == 2){
                uD = uD[ 1 ];
            }else{
                uD = uD[ 0 ];
            }
            uD = uD.split( "&" );
            uD = uD[ 0 ];
            return "http" + uD;
        },
        
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },
        
        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('yahoo');
            }
        },                

        validProdImg : function(){
            return 1;
        }
    },

    _amazon : {        
        intVal: 0,
        activePop:0,
        
        care : function(){
            var storedSearch = window.location.search;
            t = this;
            this.intVal = window.setInterval(function () {
                if (window.location.search != storedSearch) {
                    storedSearch = window.location.search;
                    spsupport.sites.onUrlChange();
                }
            }, 2000);

            if (superfish.b.dlsource.toLowerCase() == "mozilla" || superfish.b.dlsource.toLowerCase() == "chrome_superfish"){
                superfish.b.inimgSrp = 0;
                superfish.b.inimg = 0;
                superfish.b.icons = 0;
            }

            spsupport.p.$("#holderMainImage, #image-block-widget,#main-image-canvas").click(function(){
                spsupport.p.$("#SF_IIAD_0").css("z-index",998);
                spsupport.p.$("#sf_see_similar").css("z-index",998);
                t.activePop = 1;
                window.setTimeout("spsupport.sites._amazon.activePopup()",1000);
            });
            
        },

        activePopup:function(){
            if(spsupport.p.$("div#ap_overlay").length>0){ // then the big overlay is open
                this.activePop = window.setTimeout("spsupport.sites._amazon.activePopup()",1000);
            }else{
                this.disableActivePopup();
            }
        },

        disableActivePopup: function(){
            window.clearTimeout(this.activePop);
            this.activePop = null;
            spsupport.p.$("#SF_IIAD_0").css("z-index",12010);
            spsupport.p.$("#sf_see_similar").css("z-index",12005);
        },

        offInt: function() {
            if(this.intVal){
              window.clearInterval(this.intVal)
              this.intVal = 0;
          }
        },        

        gRD : function(){
            return 1300;
        }
    },
    
    _superfish: {
        su: function () {
            return 10;
        }
    },
    
    _searchcompletion: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('searchcompletion');
            }
        }        
    },
    
    _widdit: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('searchcompletion');
            }
        }        
    },
    
    _autocompletepro: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('searchcompletion');
            }
        }        
    },
    
    _protectedsearch: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('searchcompletion');
            }
        }        
    },

    _certified_toolbar: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('searchcompletion');
            }
        }        
    },

    _brandthunder: {
        care: function(){
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('brandthunder');
            }
        }        
    },
    
    _surfcanyon: {
        care: function(){            
            if (spsupport.txtSr) {
                spsupport.txtSr.disableAll();
            }
        },
        
        firstTimeRep: function(){
            spsupport.events.reportEvent("in surfcanyon care", "info");
            spsupport.statsREP.reportStats(spsupport.statsREP.repMode.CPM);
        },

        ph2bi : function(){
            return spsupport.txtSr ? spsupport.txtSr.ph2bi() : 0;
        },

        searchget: function() {
            if (spsupport.txtSr) {
                spsupport.txtSr.searchget('surfcanyon');
            }
        }        
    },

    _ebay: {
        care : function(){
            spsupport.p.prodPage.d = 149;
            spsupport.p.prodPage.l = 1500; 
            superfish.b.inimgSrp = 0;
        },

        searchget: function() {
            spsupport.p.prodPage.d = 149;
            spsupport.p.prodPage.l = 1500;           
            var vQ = '#vi-tTblC2 > div, #RightSummaryPanel > div, #AdPanel, #BuyingOptions3, #viewad-sidebar'; //#BuyOptionsWrapper';//.si-trs-top'; // default (us)
            vQ += ', #isclmn + td > div'; // .de, .fr, .co.uk

            var ssg = superfish.sg;

            if (ssg && superfish.b.searchget) {
                if(spsupport.p.$(vQ).length) {
                    superfish.b.sgAllenby = 0;
                    ssg.sSite = 3;
                    ssg.q = vQ;
                    ssg.powered1 = 'by&nbsp;';
                    var st = 'font-size:11px;font-family: Arial,sans-serif;';
                    ssg.cssMainTitle = 'color:#000000;' + st ;
                    ssg.cssPowered = 'text-align:right;color:#0E774A;' + st;
                    ssg.relpos = 'insertBefore';
                    ssg.itemWidth = 92;
                    ssg.cssTitle = 'color:#002398;display:block;padding-top:3px;font-size:11px;overflow: hidden;'+(spsupport.p.isIE ? "height:25px;" : "max-height: 25px;");
                    ssg.cssPrice = 'padding-top: 2px;font-size:11px;';
                    ssg.cssStore = 'display:block;font-size:11px;height:14px; overflow: hidden;color:#0E774A;';
                    ssg.cookie = '_ebay';
                    spsupport.sites.sgGen();
                }
                else {
                    ssg.sSite = 0;
                }
                
                if (spsupport.p.dlsource == "conduit") {
                    ssg.sSite = 0;
                }
                
            }
        },
        
        isSrp: function() {
            var iu = spsupport.sites.inURL;
            if (iu('/sch/') || iu('deals.ebay') || iu('_nkw=')) {
                spsupport.p.pageType = 'SRP';
                return 1;
            }
            return 0;
        },
        
        su: function () {return 10;},
        
        fCn: function(nd, ccl) {   // find containing node (card of the product on SRP)
            var atCl = '';
            while (nd && nd.nodeName.toLowerCase() != 'body') {
                nd = nd.parentNode;
                atCl = nd.getAttribute('class');
                if (atCl && atCl.indexOf(ccl) > -1) {
                    return nd;
                }
            }
            return 0;
        },
        
        fTx: function(nd, cl) {    // fetch text. nd - node, ccl - class of container, cl - class of wanted node
            var iT = '';
            if (nd) {
                nd = cl ? spsupport.p.$('.' + cl, nd)[0] : nd;
                if (nd) {
                    iT = spsupport.api.getTextOfChildNodes(nd);
                }
            }
            return iT;

        },

        getRelText : function(node){
            if (node) {
                var relTxt = {
                    prodUrl: "",
                    iText: ""
                };                
                var spa = spsupport.api;
                var lNode = spa.getLinkNode(node, 5);
                var nd;
                relTxt.prodUrl = lNode ? lNode.href : '';
                relTxt.prodUrl = relTxt.prodUrl.indexOf('javascript:') > -1 ? '' : relTxt.prodUrl;
                var srp = document.location.href.indexOf('/sch/') > -1 ? 1 : 0; 
                if( srp && document.location.href.indexOf('&_dmd=1') > 10 ){    // eBay SRP, list view
                    node = this.fCn(node, 'card');
                    relTxt.iText = this.fTx(node, 'rslp-cd');                    
                }
                else if (srp && document.location.href.indexOf('&_dmd=2') > 10) {   // eBay SRP, table view
                    node = this.fCn(node, 'card');
                    if (!relTxt.prodUrl.length) {
                        nd = spsupport.p.$('.title a', node)[0];
                        if (!nd) {
                            nd = spsupport.p.$('a.ittl', node)[0];
                        }
                        relTxt.iText = nd ? this.fTx(nd) : this.fTx(node);
                        relTxt.prodUrl = nd ? nd.href : '';
                    }
                    else {
                        relTxt.iText = this.fTx(node);
                    }
                }
                else if (srp && document.location.href.indexOf('&_dmd=5') > 10) {   // eBay SRP, 2 halves view
                    node = this.fCn(node, 'tri-i');
                    relTxt.iText = this.fTx(node, 'ittl');
                    if (!relTxt.prodUrl.length) {
                        nd = spsupport.p.$('a.ittl', node)[0];
                        relTxt.prodUrl = nd ? nd.href : '';
                    }
                }
                else if (document.location.href.indexOf('/itm/') > -1 || document.location.href.indexOf('/ctg/') > -1) { // vi-ih-bc-label
                    if (!lNode) {
                        nd = spsupport.p.$('h1');
                        relTxt.iText = spsupport.api.getTextOfChildNodes(nd[0]);
                    }
                }
                if ((!relTxt.iText || !relTxt.iText.length) && lNode) {
                    relTxt.iText = spsupport.api.textFromLink(lNode, lNode.href);
                }
                return relTxt;
            }
            return 0;
        }

    }
};

        
            spsupport.txtSr = {
    wl: {},
    sent: 0,
    ext: '',
    del: '***',
    txts: [],
    txtsWl: [],
    reason: 0,
    t: '', // additional texts
    data: {
        'surfcanyon': {
            mn: 'Surfcanyon',
            q: '#trFor0',
            wrapper: '<tr><td class="position"></td><td>',
            wrappperClose: '</td></tr>',
            inp: '#searchbox_textfield',
            link: 'tr[id^="trFor"] .url'
        },
        'searchcompletion' : {
            mn: 'Searchcompletion',
            q: '#SF_TARGET',
            cssMain: 'padding-left: 12px;',
            inp: '#sbi',
            relpos: 'appendTo',
            container: '#SF_TARGET',
            link: '.results cite'
        },
        'widdit': {
            mn: 'Searchcompletion'
        },
        'autocompletepro': {
            mn: 'Searchcompletion'
        },
        'protectedsearch': {
            mn: 'Searchcompletion'
        },
        'certified-toolbar': {
            mn: 'Searchcompletion'
        }, 
        'brandthunder' : {
            mn: 'Surfcanyon',
            q: '#trFor0',
            wrapper: '<tr><td class="position"></td><td>',
            wrappperClose: '</td></tr>',
            inp: '#searchbox_textfield',
            txt: '.activeLink',
            link: 'tr[id^="trFor"] .url'
        },
        'bing': {
            mn: 'Bingtext',
            q: 'ul#wg0 li', //'#results .super',
            inp: '#sb_form_q',
            wrapper: '<li class="sa_wr">',
            wrappperClose: '</li>',
            num: 5,
            txt: '.sb_tlst a',
            link: '.sb_meta cite'
        },        
        'yahoo': {
            mn: 'Yahootext',
            q: 'ul.reducepx-spnslist li', //'#results .super',
            inp: '#yschsp',
            num: 7,
            link: '.eca, .url'
        },        
        'google': {
            sendLate: 1,
            mn: 'Googletext',
            q: '#trFor0',
            inp: '#gbqfq, #lst-ib',
            txt: 'li.g a.l, li.g h3.r',
            link: 'li.g .f cite'
        },
        'craigslist': {
            sendLate: 1,
            mn: 'Craigslist',
            q: '#trFor0',
            txt: 'h2'
        }
    },
     
    jAnc: [],
    
    siteInfo: function(domain) {
        var d = domain.split('.')[0];
        var sS = 0;
        if (this.data[d]) {
            sS = {
                imageURLPrefixes: '',
                merchantName: domain
            }
        }
        return sS;
    },
    
    ph2bi : function(){
        if(this.jAnc.length) {
            return 1;
        }
        return 0;
    },
    
    gu: function(str) {         // get url by google green string
        var s = str.split('›');
        return s[0];
    },
    
    gd: function(url) {         /* get domain by url */
        var dP = url.split(".");
        var len = dP.length;
        if ( len > 2 ){
            var co = ( dP[ len - 2 ] == "co" ? 1 : 0 );
            url = ( co ? dP[ len - 3 ] + "." : "" ) + dP[ len - 2 ] + "." + dP[ len - 1 ];
        }
        return url;
    },
    
    disableAll: function() {
        var sfb = superfish.b;
        sfb.icons = 0;
        sfb.inimg = 0;
        sfb.inimgSrp = 0;
        sfb.cpn[0] = 0;
    },
    
    searchget: function(d) {
        var ssg = superfish.sg;
        this.dt = this.data[d];
        if (ssg) {
            ssg.offset = 1;
            ssg.itemWidth = 94;
            ssg.cssMain = this.dt.cssMain ? this.dt.cssMain : '';
            ssg.cssTitle = 'display:block;padding-top: 3px;max-height:48px; overflow: hidden;';
            ssg.cssPrice = 'font-weight: bold;';
            ssg.cssStore = 'display:block; color:green;text-decoration: none; width: 90px; overflow: hidden;line-height:15px;';
            ssg.cssPrompt = 'top: 20px; right: -37px;';
            ssg.q = this.dt.q;
            if (this.dt.relpos) {
                ssg.relpos = this.dt.relpos;
            }
            ssg.pwrd = 0;
            ssg.container = this.dt.container || 0;
            ssg.wrapper = this.dt.wrapper ? this.dt.wrapper : '';
            ssg.wrapperClose = this.dt.wrapperClose ? this.dt.wrapperClose : '';
            ssg.cookie = '_' + d;                 
            if (spsupport.p.$(ssg.q).length) {
                ssg.sSite = this.dt.num || 8;
            }
            this.jAnc = spsupport.p.$(ssg.q);
            spsupport.sites.sgGen();
        }
    }, 
    
    useWl: function(isException) {
        var txts = this.getTxts(); // string with del
        var inp = spsupport.p.$(this.dt.inp);
        var term = inp.attr('value');
        var jSpell = spsupport.p.$('a.spell');
        if (jSpell.length) {
            term = jSpell.text();
        }
        if(isException)
            term = txts;
        var txtsArr = txts.split(this.del);
        // var wl = this.toSend(txtsArr);
        // this.txtsWl = this.txts;
        //if (this.dt && this.jAnc.length && (this.checkPip(txtsArr, term) && wl || wl)) {
        if (this.dt && this.jAnc.length && (this.checkPip(txtsArr, term) || this.toSend(txtsArr))) {
            this.sg(txtsArr, term);
        }
    },

    getTxts: function() {
        var tx = '';
        if (this.dt && this.dt.txt) {
            var jTx = spsupport.p.$(this.dt.txt);
            var del = this.del;
            var len = Math.min(jTx.length, 7);
            jTx.each(function(ind) {
                var tx1 = spsupport.p.$(this).text();
                if (ind < len && tx1.toLowerCase().indexOf('twitter') == -1) {
                    tx += tx1 + del;
                }
            });
        }
        return tx;
    },
    
    setPip: function(mBr, valReason) {
        var ws = spsupport.whiteStage;
        ws.pip = 1; 
        ws.validReason = ws.validReason || valReason;
        mBr = ws.arrUn(mBr);
        ws.matchedBrand =  mBr.join(" | ").replace(" | undefined","");
        spsupport.p.siteType = 'pip';
    },
    
    checkPip: function(txtsArr, term) {
        this.txts = [];
        var ws = spsupport.whiteStage;
        if (superfish.b.pipBrandInDomain && ws) {
            var pipBrandInDomain = "\\b"+ superfish.b.pipBrandInDomain.replace(/\|/g,"\\b|\\b") + "\\b";
            var rBrands = new RegExp(pipBrandInDomain, 'gi');
            var reason = '';
            var mBr = [], cmBr = [];
            if (txtsArr) {
                for (var i in txtsArr) { 
                    mBr = txtsArr[i].match(rBrands);
                    if (mBr != null && mBr.length > 0 ){
                        cmBr = cmBr.concat(mBr);
                        this.txts[this.txts.length] = txtsArr[i];
                        if (this.texts && this.texts.length == 3) {
                            break;
                        }
                    }                    
                }
            }
            
            if (this.txts.length) {
                reason = 'brands in texts';
            }
            
            if (term) {
                mBr = term.match(rBrands);
                if (mBr != null && mBr.length > 0 ){
                    cmBr = cmBr.concat(mBr);
                    reason += ' | brand in term';
                }
            }
            
            cmBr = ws.arrUn(cmBr);
            
            if (this.txts.length) {
                this.reason = 1;
                this.setPip(cmBr, reason);
                return 1;
            }
        }
        return 0;
    },
        
    addTxts: function(mBr, txts) {
        var a = txts.split(this.del);
        var len = Math.min(a.length, 8);
        var t = [];
        for (var i = 0; i< mBr.length; i++) {
            for (var j = 3; j < len; j++) {
                if(a[j].indexOf(mBr[i]) > -1) {
                    t[t.length] = a[j];
                }
            }            
        }
        if (spsupport.whiteStage) {
            t = spsupport.whiteStage.arrUn(t);
        }
        t = t.join(" | ");
        this.t = t.substring(0, 250);        
    },
    
    toSend: function(txtsArr) {
        this.txts = [];
        var ret = false;
        var urls = spsupport.p.$(this.dt.link);
        var tx = '', links; // del = '***';
        var del = this.del;
        urls.each(function() {
            tx += spsupport.p.$(this).text() + del;
        });
        links = tx.split(del);      // array of links
        var len = Math.min(links.length, 7);
        for (var i = 0; i < len; i++) {
            links[i] = links[i].replace(/https?:\/\//g, "");
            links[i] = links[i].split('/')[0];
            links[i] = this.gd(this.gu(links[i]));
            links[i] = spsupport.p.$.trim(links[i]);
            if (links[i] && links[i].indexOf('google') == -1 && links[i].indexOf('yahoo') == -1 && this.wl.supportedSitesMap[links[i]]) {
                ret = true;
                this.reason = 2;
                this.txts[this.txts.length] = txtsArr[i];                
            }
        }
        return ret;            
    },
    
    sg: function(txts, term) {       /* searchget for textual search: inputQuery, merchant name */
        var sp = spsupport.p;
        var compl = '';
        if (term && term.length) {			
            var ob = {
                userid: encodeURIComponent(sp.userid),
                merchantName: this.dt.mn,
                dlsource: sp.dlsource ,
                appVersion: sp.appVersion,
                documentTitle: this.txts[0] /* || this.txtsWl[0] */ || compl,
                imageURL: term, 
                imageTitle: this.txts[1] /* || this.txtsWl[1] */ || compl,
                imageRelatedText: (this.txts[2] /* || this.txtsWl[2] */ || compl),
                productUrl: ''
            };
            this.t = '';
            this.send(ob);
        }
    },
    
    send: function(ob) {
        if (superfish.util) {
            if (!this.sent) {
                superfish.util.prepareData(ob, 1, 8, 0, 0, 0);
                this.sent = 1;
            }
        }
        else {
            setTimeout(function() {
                spsupport.txtSr.send(ob);
            }, 500);
        }
    }           
}
        
           superfish.b.xdmsg_1 = {
    lastMsg : 0,
    timer: 0,
    postMsg : function( target, URL, param ){
        if( target != window ){
            try{
                var indexOfHash = URL.lastIndexOf("#");
                if(indexOfHash < 0)
                    indexOfHash = URL.length;
                var newLocation = URL.substring(0, indexOfHash) + "#sfmsg_" + param + "@@";
                if ( URL.length > 13 ){
                    target.location = newLocation;
                }
            }catch(e){}
        }
    },

    getMsg : function(callback){

        if(location.hash == "") {
            return;
        }
        try{
            var indexOfMsg = location.hash.lastIndexOf("sfmsg_");
            if( indexOfMsg > 0){
                var hash = location.hash;
                var endOfMsg = hash.lastIndexOf("@@");
                var msg = hash.substring( indexOfMsg + 6, endOfMsg );
                var origHash = hash.substring(0, indexOfMsg ) + hash.substring( indexOfMsg + 6 + msg.length + 2, hash.length );
                location.hash = ( origHash == "#" ) ? "#sf" : origHash;
                if(callback){
                    callback( msg );
                }
                return;
            }
        }catch(e){}
    },

    init: function(  func, interval ){
        var self = this;
        this.timer = setInterval( function(){
            self.getMsg( func )
        }, interval );
    },

    clear: function(  ){
        clearInterval( this.timer );
    }
};
           superfish.b.xdmsg_2 = {
    cbFunction: 0,

    postMsg : function( target, param ){
        if( target != window ){
            target.postMessage( param, "*" );
        }
    },

    getMsg : function(event){
        ( window.xdmsg ? xdmsg : superfish.b.xdmsg).cbFunction( event.data, event.origin );
    },

    init: function( cbFunc ){
        this.cbFunction = cbFunc;
        if( window.addEventListener ){
            window.addEventListener("message", this.getMsg, false );
        }else{
            window.attachEvent('onmessage', this.getMsg );
        }
    },

    kill: function (){
        if( window.removeEventListener ){
            window.removeEventListener("message", this.getMsg, false );
        }else{
            if (window.detachEvent) {
                window.detachEvent ('onmessage', this.getMsg );
            }
        }
    }
}
;
           if (spsupport.br.isIE7){
                superfish.b.xdmsg = superfish.b.xdmsg_1;
           }
           else {
                superfish.b.xdmsg = superfish.b.xdmsg_2;
           }
       
        
        


        superfish.utilities.sfWatcher.setState("start load bsi");
        superfish.utilities.sfWatcher.setDlsource(superfish.b.dlsource);
        superfish.utilities.sfWatcher.setVersion(superfish.b.appVersion);

  superfish.b.inj(window.document, superfish.b.site + "js/base_single_icon.js?ver=" + superfish.b.appVersion , 1);

        superfish.utilities.sfWatcher.setState("end load bsi");

            if (navigator.userAgent.toLowerCase().indexOf("msie") > -1){
                superfish.b.suggestToUpdateBHODate = (superfish.b.qsObj.suggestToUpdateBHODate || "");
                superfish.b.mostUpdatedBhoVersion = " 1.2.1.0 ";
            }
                spMsiSupport = {
    validateUpdate: function() {
        if (spsupport.p.isIE){
            if (!superfish.b.suggestToUpdateBHODate){
                superfish.b.suggestToUpdateBHODate = "20100101";
            }
            if (superfish.b.suggestToUpdateBHODate + 14 < spsupport.api.getDateFormated()){
                if( spsupport.api.isOlderVersion( superfish.b.mostUpdatedBhoVersion, spsupport.p.clientVersion ) ){
                    spsupport.api.sendMessageToExtenstion("SuperfishSaveSuggestToUpdateBHODateMessage", { date: spsupport.p.getDateFormated() } );
                    window.open(spsupport.p.sfDomain + "html/suggestToUpdateBHO.html?domain=" + spsupport.p.sfDomain,"Update","height=274,width=336");
                }
            }
        }
    }
}
            
           
            spsupport.share = {    
    prt: (window.location.protocol.indexOf( "https" ) > -1 ? "https://" : "http://"),
    domain: 'http://superfish.com/ws/',
    env: '/ws',
    
    init: function(d) {
        this.domain = d;
    },
    
    getBtnImage: function(type) {
        return this.domain+'/images/ws-share/'+(type == 'pin' ? 'pinit-btn-2.png' : 'fb_share.png'); //this.CONST.PRT + this.CONST.DOMAIN + this.CONST.CONTEXT_PATH + "/images/ws-share/"+(type == 'pin' ? 'pinit-btn-2.png' : 'fb_share.png');
    },
    
    getItemShareURL: function(item, searchURL, pos, type, clickSrc) {
        var path = item.imagePath;
        //searchURL = encodeURIComponent(escape(searchURL));
        searchURL = searchURL.replace(/[\'\"]/g, "");
        var shareURL = searchURL.replace('findByUrlSfsrp', 'shareURL').replace('findByUrl', 'shareURL');//TODO: use a serverside constant for shareUrl path instead of replace():
        var title = item.title;
        title = title.replace(/&amp;/g,'');
        title = title.replace(/&apos;/g, '\'');
        return shareURL +
            (clickSrc ? "&clickSrc="+clickSrc : '' )+
            "&shareType="+type+
            "&prodDesc="+encodeURIComponent(escape(item.merchantName))+
            "&prodTitle="+encodeURIComponent(escape(title))+
            "&prodImage="+( path.indexOf("http") == -1 ? superfish.b.iiu.replace( "*", inc.num() ) + path : path  );
    }
};
            superfish.inimgAllenby = inimg = {
    xdMsgDelimiter: superfish.b.xdMsgDelimiter,
    h: 71, // height
    hAdd: superfish.b.inimgDisplayBox == 4 || !superfish.b.inImageextands ? 0 : (superfish.b.inimgDisplayBox == 2 ? 24 : 7),
    iiExtands: superfish.b.inImageextands,
    iiRatio: superfish.b.inImageextands ? 1.5 : 3,
    iiExplore2Search: superfish.b.inimgExploreBecomeSearch,
    iiExploreSearchLink : "",
    iiExploreHoverReport : 0,
    extrSearchTO:0,
    y: [], /* y positions */
    view: [], // 0 - normal, 1 - without expl
    sminf: [],
    pad: [],
    iw: 61, // Item width
    pd: 4, // Padding between items
    inf: 40, // Width of panel buttons
    expl: 30,//superfish.b.inimgDisplayBox == 3 ? 16 : 30,
    itn: 0, // Number of items
    res: [], // Array of flags for Plugin stage
    ii: [], // In-Image node
    se: [], // search session
    itNum: [],
    iiInd: 0, // Index of image/item
    lai: [], // Array of icon data per image
    sm: 0, // Shift of image position
    dv: [], // array of DIV's
    htm: 0, // hover timer ()
    wakeupDiv: null,
    features: {},
    cssMain: '',
    rdc: 0,
    testBp: superfish.b.testBp,
    
    vh: function(imh) {
        var t = this, h = this.h*this.iiRatio;
        if (t.iiExtands) {return (imh >= h);}
        else {            
            if(imh < h) {
                var nh = parseInt(imh/this.iiRatio);
                if (nh < 40) {return false;}
                else {return true;}
            }            
            else {return true;}        
        }
    },
    
    // Validate image
    vi: function(imw, imh, all) {
        var t = this, h = this.h*this.iiRatio, sv = 0, add = 0;
        if (t.vh(imh) && !superfish.b.noIcon || superfish.b.noIcon) {
            var sp = imw - 15, smsp = imw - (t.inf + t.expl), iw = t.iw + t.pd;
            t.itn = parseInt(smsp/iw);
             if (t.itn > 2) {
                return t.itn;
            }
            t.itn = parseInt(sp/iw);
            if (t.itn && t.itn < 3) {
                sv = t.itn;
                add = Math.round(sp/6);
                sp = sp + add;
                t.itn = parseInt(sp/iw);
                t.sm = (t.itn > sv ? Math.round(add/2) : 0);
            }
            return t.itn;           
        }
        return 0;
    },

    // Create In-Image node
    cr: function(ht, b, ind, hd) {
        var t = this;
        var s = t.p.prodPage.p && t.p.prodPage.p.style ? t.p.prodPage.p.style.padding : 0;
        var pb = 0, pl = 0, pr = 0;
        if (s && s.length > 0) {
            s = s.split(' ');
            switch(s.length){
                case 1:
                    pb = pl = pr = parseInt(s[0]);
                    break;
                case 2:
                    pb = parseInt(s[0]);
                    pl = pr = parseInt(s[1]);
                    break;
                case 3:
                    pb = parseInt(s[2]);
                    pr = parseInt(s[1]);
                    break;
                case 4:
                    pb = parseInt(s[2]);
                    pr = parseInt(s[1]);
                    pl = parseInt(s[3]);
                    break;
            }
        }
        t.y[ind] = t.lai[ind].y + t.lai[ind].h - t.h;
        if (t.dv[ind] && t.iiExtands) {
            t.y[ind] = t.y[ind] + t.h;
        }
        if(!t.iiExtands) t.y[ind] -= t.h;
        this.w += (pl+pr);
        var prt = b.psuSupportedByText;
        if (t.w < 115) {
            var by = prt.indexOf('by ');
            if (by > -1)
            prt = prt.substring(by, prt.length);
        }
        var lft = this.lai[ind].x-this.pad[ind];
        var bs = 'position: absolute;';
        if (t.b.inimgDisplayBox != 3) {
        bs += 'height:'+ (this.h+this.hAdd + 3) + 'px;';
    }
        var as = 'border: none !important;';
        var sz = (this.w < 145 && b.psuSupportedByText.length > 25 ? 6 : 7);
        var color = (t.b.inimgDisplayBox == 4 ? '#DB2C4A' : '#777777');
        var color2 = (t.b.inimgDisplayBox == 4 ? '#C70361' : '#CCCCCC');        
        var ft = 'font-family: Helvetica,Arial !important;font-size:'+sz+'pt !important;color:'+color+' !important;text-decoration:none !important;';
        var ms =  bs +'width:'+ this.w +'px;background: transparent; overflow: visible; z-index: 12010 !important; left: '+ lft +'px !important; top: '+ this.y[ind] +'px;';
        ms += (hd ? 'display: none;' : '');
        ms += (b.inimgDisplayBox == 4 ? 'border:1px solid #C70361;':'');
        var stl = 'height: '+ (t.iw) +'px; float: left; margin-right: '+t.pd+'px;';
        var x = t.p.sfDomain + (t.iiExplore2Search? 'inimg/img/thinSearchButton.png' : 'inimg/img/explore_sm.png');
        var m = t.p.sfDomain + 'inimg/img/moretr.png';
        var expl = stl + ' margin-top:1px;width: ' + (t.expl - 4) + 'px; background: url('+x+') no-repeat '+(b.inimgDisplayBox == 0 ? 7 : 9)+'px 11px; border-top-left-radius: 5px; border-bottom-left-radius: 5px;';
        if (t.view[ind] > 0 || t.rdc) {
            expl += ' display: none;';
        }
        else {
            if(t.iiExplore2Search) t.sendiiStats("ii_explore_impression");
            expl += ' display: block;';
        }
        var moreW = t.sminf[ind]-2;
        var trPos = parseInt(moreW/2) - 6, trPosY = (t.iw - 19)/2 - 5;        
        var he = t.iw;
        var more = stl + ' width: '+t.sminf[ind]+'px; margin: 0; cursor:pointer; background-image: url('+m+'); display: block;';
        var moreMg = parseInt(t.iw/2) + 9;
        more = 'background-color: #FFFFFF; background-image: url('+m+'); background-position: ' + trPos + 'px '+trPosY+'px; background-repeat: no-repeat; text-align: center !important; border-top-right-radius: 5px; border-bottom-right-radius: 5px; cursor: pointer; display: block; float: left; height: '+he+'px !important; width: '+ moreW + 'px;';
        if (t.rdc) {
            more += 'position: relative;border-top: none !important;'; //top: -1px;';
        }
        else {
            more += 'margin-top: 1px;';
        }
        if (b.inimgDisplayBox == 0 || b.inimgDisplayBox == 4) {
            more += 'border: 1px solid #D4D4D4 !important;';
            expl += 'border: 1px solid #D4D4D4 !important;';
        }
        else {
            more += 'border:none;';
            expl += 'border:none;';
        }
        var gardientBg = 'background: -webkit-gradient( linear, left top, left bottom, color-stop(0.05, #FFFFFF), color-stop(1, #C9C9C9) );' +
            'background: -moz-linear-gradient( center top, #FFFFFF 5%, #C3C3C3 100% );' +
            '-ms-filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#FFFFFF\', endColorstr=\'#C3C3C3\');' +
            'filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#FFFFFF\', endColorstr=\'#C3C3C3\');';
        var vertTxt = '-webkit-transform:rotate(-90deg);-moz-transform:rotate(-90deg);-o-transform: rotate(-90deg);-ms-transform:rotate(-90deg);white-space:nowrap;'; 
        var suppurtedByPosSt = 'position:absolute;height: 10px !important; overflow: hidden; line-height:10px !important;';
        var noVert = t.p.isIEQ || t.p.isIE8;
        var posSt = (b.inimgDisplayBox == 2 ? 'top:3px;padding-left:2px;' : 'bottom:0px;left: 2px;');
        var infoStyle = "font-family: helvetica,arial,sans-serif; font-size:7pt !important; left:2px !important; top:-13px !important; "
//        if (b.inimgDisplayBox == 4 && (t.p.isIE8 || t.p.isIEQ)) {
//            vertTxt += 'filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);';
//            posSt = 'bottom:'+(t.p.isIEQ ? 0 : 60)+'px;left:0px;';
//        }
        suppurtedByPosSt += posSt;
        suppurtedByPosSt += 'background: #ffffff !important;padding: 1px 2px !important;font-size:7pt !important; ' + (b.inimgDisplayBox == 4 ? 'left: 3px !important; top:-13px !important;' : 'left:'+(t.transPad + 5)+'px !important; top:-12px !important;');
        var si = '15px';
        var c = 'cursor:pointer !important; margin:0 !important; padding:0 !important; font-size: 0 !important;';
        var xq = t.p.sfDomain + 'inimg/img/qButton.png';
        var trMP = 'padding-left:'+(t.transPad-2)+'px;';
        if (b.inimgDisplayBox == 6 || b.inimgDisplayBox == 3 || b.inimgDisplayBox == 1) {
            trMP = 'margin-left:'+(t.transPad-2)+'px;margin-right:'+(t.transPad-2)+'px;';
        }
        
        var hh = this.h+this.hAdd;
        if (b.inimgDisplayBox == 4) {
            hh += 3;
        }

         return (
            '<div id = "SF_IIAD_'+ ind +'" style = "'+ ms +'">' +
                '<div class = "SF_IIAD_TRANS" style = "height: '+ (hh) +'px;'+trMP+'z-index: -1;background: #ffffff; overflow: visible; opacity:0.9; filter: alpha(opacity=90);border-radius:5px;'+ (b.inimgDisplayBox == 0 || b.inimgDisplayBox == 4 ? 'border: none;' : 'border:1px solid #CCCCCC;')+'">' +
                (t.iiExplore2Search ? '<a target="_blank" href="'+t.iiExploreSearchLink+'" class="SF_II_TEXT_SEARCH" style="position:relative; display:block;'+expl+'" onclick="superfish.inimg.sendiiStats(\'ii_explore_click\');"> </a>' : '<div class="SF_IIAD_EXPL" style = "'+expl+'"></div>') +
                ht +
                '<div class="SF_IIAD_MORE" style = "'+more+'"><div style = "margin-top: '+moreMg+'px;color: #999999 !important; font-family: Arial,Helvetica,Verdana !important; font-size: 7pt !important;">More</div></div>' +
                '</div>' +
            	( b.psuSupportedBy ?
                     (b.inimgDisplayBox == 2 ? '<div style="z-index:1;width: 100%; height: 16px;position:absolute;top:' + (t.iw+22) +'px;border-bottom:1px solid #8D8D8D;text-align:left !important;' + gardientBg + '">' : '') +
                     (b.inimgSupportedByLink && b.inimgSupportedByLink.indexOf("javascript:")==-1 ?
                ('<a target = "_blank" title="' + b.psuSupportedByTitle + '"  onmouseover = "this.style.textDecoration = \'underline\';" onmouseout = "this.style.textDecoration = \'none\';" style="' + as + suppurtedByPosSt + ft + '" href="' + b.inimgSupportedByLink + '">' + prt + '</a>') :
                '<div id = "IIAD_PRT_INFO" title="Info"  onmouseover = "this.style.textDecoration = \'underline\';" onmouseout = "this.style.textDecoration = \'none\';" style="cursor:pointer; ' + as + suppurtedByPosSt + ft + '">' +
                    prt +
                    '</div>') +
                    (b.inimgDisplayBox == 2 ? '</div>' : '')
                    : '' )+  
                (b.inimgDisplayBox == 4 ? '<div id="qb" style="z-index:1;position:absolute;bottom:0px;right:0;height:'+ si +';width:'+ si +';background: url('+ xq +') 0px 0px no-repeat;'+ c +'"></div>' : '') +        
            '</div>'
            );
    },

    hov: function (node, event) {
        var t = this;
        var jItDet = t.p.$('.itemDetails', t.p.$(node));
        var jBrand = t.p.$('.brand', jItDet);
        if (event == 1) {
            jItDet.css({'top': '-80px'});        
            jBrand.css({'display': 'block'});
        }
        else {
            jItDet.css({'top': '-20px'});        
            jBrand.css({'display': 'none'});
        }
    },

    ih : function(it, i, ind) {
        if (it) {
            var t = this;
            if(i == 0 && this.iiExplore2Search){
                t.iiExploreSearchTitle = it.title;
                t.iiExploreSearchLink = "http://www.delta-search.com/?q="+encodeURIComponent(t.iiExploreSearchTitle)+"&babsrc=ext_sprfs1&affID=121785";
            }
            var tr = 'target = "_blank"';
            var l = 12;
            var pr = (it.price.length > 6 ? it.price.split('.')[0] : it.price);
            var tl = t.trw(it.title, 16);
            var is2 = (t.p.isIEQ ? t.iw - 6 : t.iw - 4);
            var is3 = 135;
            var arr = 14;
            var lip = parseInt((t.iw+t.pd)*i);
            if (this.view[ind] == 0) {
                lip = lip + this.expl;
            }
            var lp = parseInt((t.iw+t.pd)*i) + t.iw/2 - arr/2;
            var elp = t.transPad-4;
            var nfw = 185;
            var en = elp + nfw;
            var ar2 = lp + arr;
            var ribbons = t.p.sfDomain + 'images/ribbons.png';
            var stars = t.p.sfDomain + 'images/stars_y.png';
            var starsUrl = t.p.sfDomain + 'inimg/img/stars.png';
            var itmImg = t.p.sfDomain + 'inimg/img/itemImg2.png';
            var starsSmUrl = t.p.sfDomain + 'inimg/img/stars_sm.png';
            var smRibbon = t.p.sfDomain + 'inimg/img/iiRibbons.png';
            var pos = t.b.inimgDisplayBox == 0 || t.b.inimgDisplayBox == 4 ? 'top: 47px;' : 'bottom: 2px;';
            var pos2 = t.b.inimgDisplayBox == 0 || t.b.inimgDisplayBox == 4 ? 'top: 47px;' : 'bottom: 3px;';
            var stl1 = 'height: 13px;width: '+ t.iw +'px;position: absolute;'+pos+'left:'+(t.transPad + lip)+'px;text-align: left;overflow: hidden;background-color: #ffffff;border-top: solid 1px #b57634;border-right: solid 1px #b57634;border-bottom: solid 1px #b57634;';
            var stl3 = 'height: 10px;left: 6px;position: absolute;top: ' + (t.p.isIEQ ? 0 : 1) + 'px;width: 55px;background: url('+ starsUrl + ') 0 0 repeat;';
            var stl2 = 'border-color: transparent transparent transparent #B57634;border-style: solid;border-width: ' + (t.p.isIEQ ? '6px 0 6px 6px' : '8px 0 8px 6px') + ';position: absolute;top: ' + (t.p.isIEQ ? -1 : -2) + 'px;left:0;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl5 = 'border-color: transparent transparent transparent #ffffff;border-style: solid;border-width: ' + (t.p.isIEQ ? '5px 0 5px 5px' : '7px 0 7px 5px') + ';position: absolute;'+pos2+'left:'+(t.transPad + lip)+'px;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl11 = 'height: 16px;width: ' + (t.p.isIEQ ? 185 : 192 ) + 'px;position: absolute;top: 77px;left:132px;line-height: 20px;text-align: left;overflow: hidden;font-family: Helvetica !important;background-color: #ffffff;border-top: solid 2px #b57634;border-right: solid 2px #b57634;border-bottom: solid 2px #b57634;';
            var stl33 = 'height: 12px;left: 16px;position: absolute;top: ' + (t.p.isIEQ ? 0 : 1) + 'px;width: 65px;background: url('+ starsSmUrl + ') 0 0 repeat;';
            var stl22 = 'border-color: transparent transparent transparent #B57634;border-style: solid;border-width: ' + (t.p.isIEQ ? '8px 0 8px 8px' : '10px 0 10px 10px') + ';font-size: 0;height: 0;left: 2px;line-height: 0;position: absolute;top: ' + (-2) + 'px;width: 0;';
            var stl55 = 'border-color: transparent transparent transparent #F4F4F4;border-style: solid;border-width: ' + (t.p.isIEQ ? '8px 0 8px 8px' : '10px 0 10px 10px') + ';cursor: pointer;position: absolute;top: ' + (77) + 'px;left:132px;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl66 = 'color: #333333;position: absolute;top: ' + (t.p.isIEQ ? -5 : -2) + 'px;left: 90px; font-family: Helvetica;font-size: 10px;';
            var iidt = 'background-color:#999999; height:20px; width: 100%;';            
            var bg = t.isIEQor8 ? 'background-color: #454545; ' : 'background-color: rgba(70, 70, 70, 0.9); ';
            var curs = 'cursor: pointer;';
            var itemDetails = bg + 'display: inline-block;border-top-left-radius: 5px; border-top-right-radius: 5px; color: white; cursor: pointer; height: '+ (t.p.isIEQ ? 110 : 100) + 'px; position: relative; top: -20px; width: 100%;',
            brand = 'display: none; font-size: 14px; font-weight: bold; margin-bottom: 4px; margin-top: 2px; height: 18px; overflow: hidden;color: #ffffff;',
            merchData = 'height: 16px; overflow: hidden;color: #ffffff;',
            price = 'font-size: 12px; font-weight: bold; color: #ffffff;',
            store = 'font-size: 11px;color: #ffffff;',
            visitStore = 'color: #ffffff; border: 1px solid #81002B; border-radius: 4px 4px 4px 4px; box-shadow: 0 1px 1px rgba(255, 255, 255, 0.35); cursor: pointer; font-size: 12px; margin-top: 9px; margin-left: 0; padding: 2px; text-align: center; width: 65px; background: #b02641; filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#cc2d4c", endColorstr="#b02641"); background: -webkit-gradient(linear, left top, left bottom, from(#cc2d4c), to(#b02641)); background: -moz-linear-gradient(top,  #cc2d4c,  #b02641); ';
            if (t.isIEQor8) {
                visitStore = 'font-family:  Arial,Helvetica,Verdana !important; font-size: 7pt !important; border: 1px solid #81002B; border-radius: 4px 4px 4px 4px; cursor: pointer; font-size: 12px; margin-top: 9px; margin-left: 0; padding: 2px; text-align: center; width: 72px; background: #b02641; ';
            }
            var hf = (en > ar2 ? 0 : ar2 - en + 10);
            elp = elp + hf;
            var ilp = t.transPad + 26 + 5 + t.iw*(i+1) - t.iw/2 - nfw/2;
            if (this.view[ind]) {
                ilp = ilp - this.expl;
            }
            var st = t.trw(it.merchantName.split('.com')[0], 17);
            var bestPriceInimg = '';
            var bestPriceInimgItem = '';
            var ratingItem = '', ratingIi = '';
            var cpn = '', cpnIt = '';
            if(t.inimgBestPr.isBestPr && t.inimgBestPr.imagePath === it.imagePath && t.inimgBestPr.price == it.price){
            	bestPriceInimg = '<div style = "height:15px;width: 59px;background-color: #d90f6b;white-space: nowrap; overflow: hidden;font-size: 9px;font-weight: bolder;color: #FFFFFF;position: absolute;'+pos+'line-height: 15px;text-align: left;">'+
                    '<div style=" padding-left:1px;border-color: transparent transparent transparent #FFFFFF;border-style: solid;border-width: 7px 0 7px 7px;cursor: pointer;float: left;font-size: 0;height: 0;line-height: 0;width: 0;"></div>'+
                    'Best Price</div>';
                if (t.testBp) {
                    bestPriceInimg = '<div style = "width: 69px; height: 25px; background: url('+ smRibbon +') 0 0;position: absolute; top: 3px; left:'+(t.transPad + lip - 4)+'px;"></div>';
                }
	        bestPriceInimgItem = '<div style = "'+curs+'background-color: transparent; background-position: -98px 0; background-repeat: no-repeat;height: 98px;left: 14px;position: absolute;top: 22px;width: 98px; background-image: url('+ribbons+');"></div>';
                t.features.bp = 1;
            }

//            if (it.rating && bestPriceInimg === '') {
            if (it.rating) {
                var rt = Math.min(it.rating, 5);
                var w = rt * 11, w1 = rt * 13;
                var stl4 = 'height: 10px;left: 0;position: absolute;top: 0;width: '+w+'px;background: url('+ starsUrl + ') 0 -10px repeat;';
                var stl44 = 'height: 12px;left: 0;position: absolute;top: 0;width: '+w1+'px;background: url('+ t.p.sfDomain + ') 0 -12px repeat;';
                ratingIi = '<div style = "'+ stl1 +'">'+
                    '<div style = "'+ stl2 +'"></div>'+
                    '<div style = "'+ stl3 +'"><div style = "'+ stl4 +'"></div></div>' +
                    '</div>' +
                '<div style = "'+ stl5 +'"></div>';
                ratingItem = '<div class="rating" style="height: 36px;position: absolute;right: 17px;top: 29px;width: 90px;"><div class="greyStars" style="height: 11px; position: absolute; right: 3px; top: 1px; width: 55px; background: url('+stars+') repeat scroll 0 -11px transparent;"><div class="goldStars" style="width: '+(Math.min(it.rating, 5)*11)+'px;height: 11px; position: absolute; left: 0; top: 0; background: url('+stars+') repeat scroll 0 0 transparent;"></div></div>'+
                    (it.reviewsCount ? '<div class="reviews" style="background-color: #FFFFFF;color: #999999;font-family: Helvetica;font-size: 9px;padding-bottom: 1px;padding-left: 3px;position: absolute;right: 3px;top: 16px;">('+it.reviewsCount+')</div></div>' : '');
                t.features.rt = 1;
            }
            if (bestPriceInimg == '' && ratingIi && !t.testBp) {
                bestPriceInimg = ratingIi;
            }

            var freeSh = '';
            if (it.freeShipping) {
                var absP = 'position: absolute;left: '+(t.transPad + lip)+'px;top: '+t.iw+'px;';
                var col = t.b.inimgDisplayBox == 3 ? '#db277a' : '#333333';
                freeSh = '<div style = "color: '+col+' !important; position: relative; top: '+(t.b.inimgDisplayBox == 0 ? -12 : 1)+'px !important; left: 1px; '+ (t.p.isIEQ ? 'height: 11px !important;' : 'padding-top: 2px; height: 9px !important;')+' font-family: Arial,Helvetica !important;font-size: 9px !important;background-color: #ffffff !important;line-height: 9px !important; text-decoration: none !important; width: 58px;">Free Shipping</div>';
                t.features.fs = 1;
                if (bestPriceInimgItem) {
          	    bestPriceInimgItem = '<div style = "background-color: transparent; background-position: -196px 0; background-repeat: no-repeat;height: 98px;left: 14px;position: absolute;top: 22px;width: 98px; background-image: url('+ribbons+');"></div>';
                }
          	bestPriceInimgItem += '<div style = "'+curs+'background-color: transparent; background-position: 0 0; background-repeat: no-repeat;height: 98px;left: 14px;position: absolute;top: 22px;width: 98px; background-image: url('+ribbons+');"></div>';                
            } 

            if (t.b.inimgDisplayBox == 4 && it.freeShipping && bestPriceInimg === '') {
                bestPriceInimg = '<div style = "position: absolute;'+pos+'left:'+(t.transPad + lip+1)+'px;color: #333333 !important;font-family: Arial,Helvetica,Verdana !important;font-size: 9px !important;line-height: 11px !important; text-decoration: none !important; width: 59px; padding-bottom:1px;background-color: #ffffff !important;">Free Shipping</div>';
            }
            if(it.freeShipping && t.testBp && bestPriceInimg == '') {
                bestPriceInimg = '<div style = "width: 69px; height: 25px; background: url('+ smRibbon +') -69px 0;position: absolute; top: 3px; left:'+(t.transPad + lip - 4)+'px;"></div>';
            }
            
            
            var prMode5 = 'position: absolute; top: '+(t.p.isIEQ ? 51 : 52)+'px; width: 53px;margin: 0 4px;';
            var itemMrg = 'margin: 1px '+ t.pd +'px  0 0 !important;';
            var itemBrd = 'border:solid 1px #d4d4d4;';
            if (t.rdc) {
                prMode5 = 'position: relative; top: -13px; width:'+(t.iw-3)+'px; margin: 0 1px;';
                itemMrg = 'margin: 0 !important;';
                itemBrd = 'border-right:solid 1px #d4d4d4;border-bottom:solid 1px #d4d4d4;';
                if(i == 0) {
                    itemBrd += 'border-left:solid 1px #d4d4d4;';
                }
            }
            
            var bgGrey = t.p.isIEQ ? 'background-color: rgb(70, 70, 70);' : 'background-color: rgba(70, 70, 70, 0.9);';
            var prIii = (t.b.inimgDisplayBox == 4 ? '' : 'background: #ffffff;') + 'color: #111111; font-size: 9px !important; line-height: 9px !important; ';
            if (t.b.inimgDisplayBox == 3) {
                prIii = bgGrey +'border-top-left-radius: 4px;border-top-right-radius: 4px;color: #ffffff; font-size: 10px !important; line-height: 10px !important; ';
                if (t.rdc) {
                    prMode5 += 'top: -7px;';
                }
            }
            if ((t.b.inimgDisplayBox == 0 || t.b.inimgDisplayBox == 4) && !t.rdc) {
                prMode5 += 'top: 64px;';
            }
            
            if (t.p.isIEQ) {
                prIii += 'left: '+(t.transPad + lip)+'px;';
            }
            else {
                prIii += 'padding-top: 1px;';
            }

            var searchUrl = spsupport.api.getSrUrl(t.lai[ind],2);
            return(
                '<div id = "SF_IIAD_ITEM_'+ind +'_'+ i + '" class = "SF_IIAD_ITEM" style="position:static !important; overflow: visible !important; text-align: center !important; width: '+ t.iw +'px !important; display: block; float: left !important; vertical-align: top !important; font-family: arial,sans-serif !important; font-size: small !important; line-height: 1.2 !important;'+itemMrg+'">' +
                (t.rdc ? '' : bestPriceInimg) +
                (t.testBp ? ratingIi : '') +
                '<div class = "SF_IIAD_ITEM_INFO" style = "display: none; position: absolute; top:'+(t.iw+4)+'px; left: '+ ilp +'px; width: ' + nfw + 'px; height: 202px; background: url('+itmImg+'); margin: 0; margin-left: 2px; z-index:2;text-align: left !important;">' +
                '   <a class = "iiim" href="'+ it.merchURL + '&clickSrc=6" ' + tr + ' style="text-decoration: none !important; width: ' + (t.p.isIEQ ? 135 : 135) +'px; height: ' + (t.p.isIEQ ? 143 : 143) + 'px; margin: 35px 0 0 25px; cursor: pointer; background: #ffffff; float: left; cursor: pointer; display: block; overflow: hidden;">'+
                '       <img class="SF_IIADOV_IMG" '+ t.p.sfIcon.evl+ '="-1" sfnoicon="1"  style="width:' + is3 + 'px; height:' + is3 + 'px; display: none; border: none;" title="' + it.title + '" />'+
                '       <img id= "SF_II_LOADOV_' + ind +'_'+ i + '" src = "' + t.sp.src + '" style="width:'+ is3 +'px; height: '+ is3 +'px; display: inline-block; border: none;" />' +
         '<div class="itemDetails" style = "'+itemDetails+'">' +
         '<div style="margin-top: ' + (t.p.isIEQ ? 0 : 7) + 'px; margin-left: 7px;">' +
         '   <p class="brand" style = "'+brand+'">' + tl + '</p>' +
         '   <div class="merchData" style = "'+merchData+'">' +
         '       <span class="price" style = "'+price+'">' + pr + '</span>' +
         '       <span class="store" style = "'+store+'">' + st + '</span>' +
         '   </div>' +
         '   <p class="visitStore" style = "'+visitStore+'">Visit Store</p>' +
         '</div>' + 
        '</div>' +
 '</a>' +
  bestPriceInimgItem +
  ratingItem +
                '</div>' +
               
                '<a href="'+ it.merchURL + '&clickSrc=1" ' + tr + ' style = "display: block; width: '+ (t.b.inimgDisplayBox == 5 ? t.iw : t.iw-4) +'px; height: '+ (t.iw) +'px; padding: 0 1px;text-align: center; vertical-align: middle;'+itemBrd+'">' +
                '<img class="SF_IIAD_IMG" ' + t.p.sfIcon.evl+ '="-1" sfnoicon="1" style="width:'+ is2 +'px; height:'+ is2 +'px; border: none; display:none;" />' +
                '<img id= "SF_II_LOAD_' + ind +'_'+ i + '" src = "' + t.sp.src + '" style="width:'+ is2 +'px; height: '+ is2 +'px; display: inline-block; border: none; padding: 1px;" />' +
                '</a>' +
                '<a sfprice="1" href="'+ it.merchURL + '&clickSrc=4" '+ tr +' style = "border: none !important; height: 11px !important; display: block; font-family: Helvetica !important; overflow: hidden; text-align: center; text-decoration: none;'+ prIii + (prMode5)+'">' + pr + '</a>'+
                ((t.b.inimgDisplayBox == 4 || t.rdc || bestPriceInimg) /* t.b.inimgDisplayBox == 5 */ ? '' : freeSh) +   
                '</div>'
                );
                                        
        }
        else {
            return '';
        }
    },

    im: function(nd, sp) {  
        var t = this;
        var s = t.p.$('#' + sp, nd.parentNode)[0];
        t.p.$(nd).css({'opacity': '0'});
        if (s) {
            s.style.display = 'none';
        }
        nd.style.display = 'inline';
        t.p.$(nd).css({'opacity': '1',
                       'filter' : 'alpha(opacity=100)'
                    });
        t.p.$(nd).fadeIn(600, function(){});
    },

    bt: function(nd, e, bt, color, ob) { /* button: 1 - move, 2 - close */
        var t = this;
        var ind = (nd ? nd.parentNode.getAttribute('id') : 0);
        ind = (ind ? +(ind.split('SF_IIAD_')[1]) : -1);
        if (e == 2) {
            if (bt == 1) {
                var r = t.h - 10;
                if (t.up) {
                    t.mv((t.y[ind] + r), (t.h - r), 0, ind, ob);
                    nd.style.backgroundPosition = '-64px -13px';
                }
                else {
                    t.mv(t.y[ind], t.h, 1, ind, ob);
                    nd.style.backgroundPosition = '-64px -26px';
                }
            }
            else if( bt == 2) {
                this.u.closePopup();
                this.cl(ind, 1);
                this.u.fixDivsPos();
            }
        }
    },

    mv: function(tp, h, nu, ind, ob) { // Collapse / Expand
        var t = this;
        if (t.ii[ind]) {
            if (!nu) {
                t.ii[ind].style.overflow = 'hidden';
            }
            t.p.$(t.ii[ind]).animate({
                top: tp,
                height: h
            }, 800, null, function() {
                if (nu) {
                    t.ii[ind].style.overflow = 'visible';
                }
                t.up = nu;
            });
        }
    },

    cl: function(ind, click) { // Close
        var t = this;
        if (t.ii[ind]) {
                t.p.$(t.ii[ind]).remove();
            if (t.dv[ind]) {
                t.p.$(t.dv[ind]).remove();
            }
            if (t.ii[ind].img) {
                t.ii[ind].img.removeAttribute('sfnoicon');
            }
        }

        if (click) {
            setTimeout( function(){
                t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
                {
                    "action" : "inimg close",
                    "userid" : t.p.userid,
                    "sessionid" : t.u.currentSessionId
                } )
            }, 150);
        }
    },

    pl: function(nd) {  /* show plugin */
        var t = this;
        t.p.iiPlOn = 1;
        var ind = (nd ? nd.parentNode.parentNode.getAttribute('id') : 0);
        ind = (ind ? +(ind.split('SF_IIAD_')[1]) : -1);
        if (t.b.lp) {
            t.rfs();
            t.u.osr(t.lai[ind]);
        }
        else if (t.b.sfsrp) {
            t.rfs();
            t.u.sfsrp(t.lai[ind]);
        }
        else {
            if (!t.b.noIcon) {
                t.u.closePopup();
            }

            if (t.res[ind]) {       /* if result is rendered */
                t.u.sendRequest("{\"cmd\": 7 }");
                t.spl(ind);
            }
            else {
                if (t.ii[ind] && t.ii[ind].img) {
                    t.p.imPos = spsupport.api.getItemPos(t.ii[ind].img);
                }
                t.u.sendRequest("{\"cmd\": 6, \"iiInd\": "+ ind +", \"rqSrc\": 1 }");
            }
            setTimeout( function(){
                t.rfs();
            }, 1500);
        }

    },

    rfs: function() {
        var t = this;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "full slideup",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId
        } );
        if(t.p.presFt){
            this.rpf(t.p.presFt, "full UI");
        }
    },

    rpf: function(features, position) {
        return;
        var t = this;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "present features",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId,
            "features": features,
            "position": position
        });
    },

    spl: function(ind) {
        var t = this;
        var o = t.lai[ind];
        if (o) {
            var pp = t.u.bubble();
            var ps = t.u.getPosition(o.x, o.y, o.w, o.h);
            var itN = t.res[ind];
            t.u.updIframeSize(itN, 0, 0);
            t.u.openPopup(o, t.p.appVersion, 0);
            pp.style.top = ps.y + "px";
            pp.style.left = ps.x + "px";
            pp.style.position = 'absolute';
            this.p.$('#infoBtn').show();
        }
    },

    si: function(jIt, e) {  /* show info */
       var jInf = this.p.$('.SF_IIAD_ITEM_INFO', jIt);
       if (jInf.length) {
            if (e) {
                jInf[0].style.display = 'block';
            }
            else {
                jInf[0].style.display = 'none';
            }
       }
    },

    rs: function(it) {
        var t = this;
        var ps = +it.id.split('_')[4] + 1;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "inimg hover",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId,
            "position" : ps
        } )
    },

    pr: function(it, e) {  /* price button */
        var bt = this.p.$('div', this.p.$(it))[0];
        if (e) {
            bt.style.backgroundPosition = '-89px -1px';
        }
        else {
            bt.style.backgroundPosition = '-104px -1px';
        }
    },

    cn: function(ind, b) {
        var a = [], n = [];
        var s = '15px';
        var t = this;
        var trw = 17;
        var l = (this.iw + this.pd*2)*this.itNum[ind] + 20 + t.transPad;
        if (l + trw > this.w) {
            l = this.w - trw - 2;
        }
        var c = 'cursor:pointer !important; margin:0 !important; padding:0 !important; font-size: 0 !important;';
        var x = t.p.sfDomain + 'inimg/img/closeButton.png';
        var pos = t.b.inimgDisplayBox == 4 ? 'top:1px;right:1px;' : 'top:-5px;right:'+(t.transPad - 8)+'px;';
        a[0] = '<div title="' + t.ttls[3] + '" style="z-index:1;position:absolute;'+pos+'height:'+ s +';width:'+ s +';background: url('+ x +') 0px 0px no-repeat;'+ c +'"></div>';

        for (var i = 0; i < a.length; i++) {
            n[i] = t.p.$(a[i]).appendTo(t.ii[ind])[0];
        }
        t.mr = n[0];

        n[0].onclick = function(){
            t.p.$('#' + t.infoId).hide(); //to close info iframe
            t.bt(this, 2, 2, '#888888', n[0]);
        };
    },

   pi: function(d){ // post data to info iframe; d - data
       var t = this;
       var m = t.b.xdmsg;
        try{
            var cW = t.p.$('iframe', t.info.jInfo)[0].contentWindow;
            if (cW != top) {
                m.postMsg(cW, d);
            }
        }catch(e){
        }
    },

    oi: function(ind) {
        var t = this;
            var lf = parseInt(t.ii[ind].style.left);
        var tp = parseInt(t.ii[ind].style.top) - t.info.infoHt + t.h - 10;
        var fixedTop = 0;
        if(tp <= 0){
            fixedTop = 10 - tp; // must be above rewriting tp value !
            tp = 10;
            if(!superfish.inimg.info.isResized){
                superfish.inimg.info.isResized = 1;
                superfish.inimg.info.h = superfish.inimg.info.h - fixedTop ;
                superfish.inimg.info.ifrh = superfish.inimg.info.ifrh - fixedTop;
            }
        }
        t.info.ev({
            'position': 'absolute',
            'top': tp + 'px',
            'left': lf + 'px',
            'bottom': '',
            'right': ''
        }, 1, 1);
        t.pi("-9999" + t.xdMsgDelimiter + t.se[ind] + t.xdMsgDelimiter + fixedTop);
    },

    pdv: function(img, ind, hd) {    /* push div */
        var t = this;
        var h = t.h + t.hAdd + 2;
        var dsp;
        if(hd) {
            dsp = 'none';
        }
        else {
            if(t.p.$(img).parent().css('display') == 'inline') {
                dsp = 'inline';
            }
            else {
                dsp = 'block';
            }
        }
        var d = '<div style = "display: '+ dsp +'; width: 20px; height: '+ (h) +'px"></div>';
        t.dv[ind] = t.p.$(d).insertAfter(img)[0];
    },
    
    calcView: function(ind) {
        var t = this;
        var minInf = 20;
        t.view[ind] = 0;
        t.sminf[ind] = t.inf;
        t.pad[ind] = 0;
        t.w = t.lai[ind].w;
        if (!t.iiExtands) {
            var ih = t.lai[ind].h/t.iiRatio;
            if (ih < 57) {
                t.rdc = 1;
                t.h = ih+7;
                t.iw = ih;
                t.testBp = 0;
            }
            else {
                t.testBp = t.b.testBp;
            }
        }        
        var iw = t.iw;
        
        if (!t.rdc) {
            iw += t.pd;
            if (t.b.inimgDisplayBox == 3 || t.b.inimgDisplayBox == 6) {
                t.hAdd = 8;
            }
        }
        var sp = t.itNum[ind]*iw;
        var rest = t.lai[ind].w - sp;
        var extra = rest;
        if (!t.rdc) {
            extra = extra - t.expl;
        }
        if (extra < minInf) {
            t.pad[ind] = parseInt(t.lai[ind].w/12);
            t.w = t.lai[ind].w + t.pad[ind]*2;
            rest = t.w - t.itNum[ind]*iw;
            extra = rest - t.expl;
        }
        if (extra < minInf) {
            extra = rest;
            t.view[ind] = 1;
            if (extra < minInf) {
                t.w = t.w + (minInf - extra);
            }
        }
        t.sminf[ind] = Math.min(t.inf, extra);
        t.sminf[ind] = t.sminf[ind] - 4;
        t.transPad = 0;
                
        var itms = sp + t.sminf[ind];
        if (!t.rdc) { //t.b.inimgDisplayBox != 5) {
            itms += t.expl;
        }
        if (itms < t.w) {
            t.transPad = parseInt((t.w - itms)/2);
        }
                
        if(t.b.inimgDisplayBox == 4) {
            var byw = 10;
            if (t.transPad < byw) {                
                if (t.transPad*2 < byw) {                    
                    t.w += byw + 2;
                }
                t.transPad = byw;                
            }
        }
    },

    createSearchLink: function(){
        return ('<a onclick="superfish.inimg.sendiiStats(\'ii_explore_click\');" id="iiExplorer" target="blank" href="'+this.iiExploreSearchLink+'" style="color: #1A75CF;zoom:1;display:none; border: 1px solid #c6c6c6; height: 57px; width: 100px; background-color: white; cursor:pointer; left: '+(26 + this.transPad)+'px;top:2px; z-index: 100000; position: absolute; opacity: 1;border-top-right-radius: 5px; border-bottom-right-radius: 5px;"><div style="width:90px; height:48px;margin:5px 0 0 5px;overflow:hidden"><p style="color: #E0126C;font-size: 9px;line-height: 14px; padding: 0;margin:0 0 5px 0;text-decoration:underline!important;">search for</p><span id="iiSearchLink" style="color: #1A75CF;cursor: pointer;font-size: 11px;font-weight: bold;line-height: 14px;padding: 0;text-decoration: none;">'+this.iiExploreSearchTitle+'</span></div></a>');
    },

    info: superfish.info,
        trw: function(st, n, a, dl){   /* st - string, n - limit length, a - appender, dl - delimeter between words  (" ") */
        dl = (dl ? dl : ' ');
        if (!n || st.length < n) {
            return st;
        }
        else {
            var aw = st.split(dl);
            var rt = aw[0];
            for(var i = 1; i < aw.length; i++) {
                if (rt.length + dl.length + aw[i].length <= n) {
                    rt += dl + aw[i];
                }
                else {
                    break;
                }
            }
            if (!a && rt.length > n || a && rt.length >= n) {
                rt = rt.substring(0, rt.lastIndexOf(dl));
            }
            if (a && rt.length < st.length) {
                rt += a;
            }
            return rt;
        }
    }
,

    hideExtraSearch: function(jq){
        t = this;
        this.extrSearchTO=setTimeout(function(){
            t.iiExploreHoverReport = 0;
            jq.$("#iiExplorer").animate({width: "hide",paddingLeft: "hide",paddingRight: "hide",marginLeft: "hide",marginRight: "hide"},200);},100);
    },

    sendiiStats: function(action, extraData){
        var data = extraData || {};
        data.action = action;
        data.userid = data.userid || spsupport.p.userid;
        data.sessionid = data.sessionid || superfish.util.currentSessionId;
        spsupport.api.jsonpRequest( spsupport.p.sfDomain_ + spsupport.p.sessRepAct, data );
    },

    init: function(dt, ind, sfu, p, b, img, hd) {
        superfish.utilities.sfWatcher.setState("in image allenby start");
        if (img.getAttribute('nosudispl') == '1') {
            superfish.utilities.sfWatcher.complete("in image allenby complete");
            return;
        }
        var t = this;
        var i;

        //if( b.uc!='ES' && b.uc!='IT' )
            t.iiExplore2Search = 0;

        b.iiinfo = 1;
        t.iiInd = ind+1;
        t.p = p;
        t.u = sfu;
        t.b = b;
        t.isIE8 = t.p.isIE  && parseInt(t.p.$.browser.version, 10) === 8;
        t.isIEQor8 = t.p.isIEQ || t.isIE8;
        /* last active icon */
        t.lai[ind] = {};
        t.lai[ind].x = sfu.lastAIcon.x;
        t.lai[ind].y = sfu.lastAIcon.y;
        t.lai[ind].w = sfu.lastAIcon.w;
        t.lai[ind].h = sfu.lastAIcon.h;
        t.lai[ind].img = sfu.lastAIcon.img;
        t.se[ind] = t.p.inimgSess;
        t.ttls = [" Open " + b.shareMsgProd + " SlideUp ",
        " Put " + b.shareMsgProd + " SlideUp down ",
        " Close " + b.shareMsgProd + " ",
        " Close " + b.shareMsgProd + " SlideUp"];
        for (i in t.res) {
            t.res[i] = 0;
        }
        t.res[ind] = p.itemsNum;
        t.ic = p.prodPage.p.ni
        t.sp = new Image();
        t.sp.src = t.p.sfDomain + 'inimg/img/as.gif';
        //t.sp.src = superfish.b.cdn.getFileUrl('image', t.sp.src);
        var obj = t.p.$.parseJSON(dt);
        t.inimgBestPr = obj.inimgBestPr;
        var o = obj.items;
        if (!o) {
            superfish.utilities.sfWatcher.complete("in image allenby complete");
            return;
        }
        
        t.itNum[ind] = Math.min(t.itNum[ind], o.length);
        t.calcView(ind);
        
        if (t.b.iiinfo) {

            t.info.jInfo = t.p.$('#' + t.info.infoId);
            if (!t.info.jInfo || t.info.jInfo.length == 0) {
                t.info.jInfo = t.p.$(t.info.ci(t.p.sfDomain, t.b.dlsource, t.b.userid, t.b.CD_CTID)).appendTo(t.p.$('body'), t.b.appVersion, 2);
                t.info.jIfr = t.p.$('iframe', t.info.jInfo);
            }
            t.info.jIfr = t.p.$('#' + t.info.infoId + '_CONTENT', t.info.jInfo);
            t.p.$('.closeButton', t.info.jInfo).off().click(function(){
                 t.info.close();
            });
        }

        var im, im2;
        var ht = "";
        for (i = 0; i < t.itNum[ind]; i++) {
            ht += t.ih(o[i], i, ind);
        }

        if(superfish.inimg.iiExtands) t.pdv(img, ind, hd);
        t.ii[ind] = t.p.$(t.cr(ht, b, ind, hd))[0];
        t.ii[ind].img = img;
        img.sfInd = ind;
        t.p.$('body').append(t.ii[ind]);
        if(t.iiExplore2Search) t.p.$('.SF_IIAD_TRANS').append(t.createSearchLink());
        var ft = "";
        ft += (t.features.bp ? "bp," : "");
        ft += (t.features.fs ? "fs," : "");
        ft += (t.features.rt ? "rt," : "");
        ft += (t.features.cp ? "cp," : "");
        if (ft) {
            t.rpf(ft, "inImg");
        }
        t.features = {};
        img.setAttribute('nosudispl', '1');
        t.up = 1;

        var trn = t.p.$('.SF_IIAD_TRANS', t.p.$(t.ii[ind]));

        t.ii[ind].onmouseover = function () {
            trn.css({
                "opacity" : "1",
                "filter" : "alpha(opacity=100)"
                });
            t.p.$('#SF_IIAD_ADT').css("display", "block");

        };

        t.ii[ind].onmouseout = function () {
            trn.css({
                "opacity" : "0.9",
                "filter" : "alpha(opacity=90)"
                });
            t.p.$('#SF_IIAD_ADT').css("display", "none");
        };

        t.p.$('#IIAD_PRT_INFO', t.ii[ind]).off().click(function() {
            t.oi(ind);
        });

        t.p.$('#IIAD_PRT_INFO_CLOSE, #qb', t.ii[ind]).off().click(function() {
            t.oi(ind);
        });
        
        t.p.$('.SF_IIAD_MORE', t.ii[ind]).click(function(){
            t.pl(this);
        });


        t.cn(ind, b);
        if(t.iiExplore2Search){
            var explr = t.p.$(".SF_II_TEXT_SEARCH");
            if(explr){
                t.p.$(explr).hover(function(e){
                    clearTimeout(t.extrSearchTO);
                    if(!t.iiExploreHoverReport) {
                        t.sendiiStats("ii_explore_hover");
                        t.iiExploreHoverReport = 1 ;
                    }
                    t.p.$("#iiExplorer").animate({width: "show",paddingLeft: "show",paddingRight: "show",marginLeft: "show",marginRight: "show"},200);
                },function(e){
                    t.hideExtraSearch(t.p);
                });
                t.p.$("#iiExplorer").hover(function(e){
                    clearTimeout(t.extrSearchTO);
                },function(e){
                    t.hideExtraSearch(t.p);
                });
            }
        }
        var it, pr, txt, iim, sr;
        for (i = 0; i < t.itNum[ind]; i++) {
            it = t.p.$('#SF_IIAD_ITEM_'+ ind +'_'+i, t.p.$(t.ii[ind]))[0];
            if (it) {
                it.ind = i;
                if(!superfish.b.inimget){
                    t.p.$(it).hover(function (e) {
                        var th = this;
                        t.si(t.p.$(this), 1);
                        if (t.b.iiHv) {
                            t.htm = setTimeout (function() {
                                t.rs(th);
                            }, 1000);
                        }
                     }, function (e) {
                         t.si(t.p.$(this), 0);
                         if (t.b.iiHv) {
                             clearTimeout(t.htm);
                         }
                     });
                }

                iim = t.p.$('a.iiim', t.p.$(it));
                if (iim) {
                    iim.hover(function () {
                        t.hov(this, 1);
                    }, function () {
                        t.hov(this, 0)
                    });
                }
            }

            if (it) {
                im = t.p.$('img.SF_IIAD_IMG', t.p.$(it))[0];
                im2 = t.p.$('img.SF_IIADOV_IMG', t.p.$(it))[0];
            }
            sr = (window.location.protocol.indexOf( "https" ) > -1 ? o[i].imagePath.replace("http:", "https:") : o[i].imagePath);

            if (im) {
                im.onload = function(im, sp){
                    return function(){
                        t.im(im, sp);
                    }
                }(im, 'SF_II_LOAD_'+ind+'_'+i);

                im.src = sr;
            }
            if (im2) {
                im2.onload = function(im2, sp){
                    return function(){
                        t.im(im2, sp);
                    }
                }(im2, 'SF_II_LOADOV_'+ind+'_'+i);
                
                im2.src = sr;
            }
            
        }

       // insert wakeup bubble if flag is on
        if( img.sfwakeup ){
            var t = this,
                sp = spsupport.p;

            // wait for startDOMEnumeration to finish
            setTimeout(function(){
                var ssimUrl = spsupport.p.imgPath +'si0.png';
                // ssimUrl = superfish.b.cdn.getFileUrl('image', ssimUrl);
                var offset = spsupport.api.getImagePosition(img),
                    seeSimilar = '<span style="'+
                            'background: url('+ ssimUrl +') 0 0 no-repeat;'+
                            'display: inline-block;'+
                            'width: 95px;'+
                            'height: 25px;'+
                            '"></span>',
                    html = '<strong style="color:#081b45;">COMPARE and SAVE</strong>' +
                           '<p style="font-size:15px;margin-top:6px;">Click on the '+ seeSimilar +' button for instant price comparissons.</p>',
                    wakeupDiv;

                wakeupDiv = t.wakeupDiv = spsupport.p.$('<div/>', {
                    html: html,
                    css: {
                        width:              offset.w - 50 + 'px',
                        height:             '70px',
                        position:           'absolute',
                        top:                ( offset.y + offset.h - 180 ) + 'px',
                        left:               offset.x + 'px',
                        backgroundColor:    '#fff',
                        padding:            '15px 25px 30px',
                        font:               '15px/1.2 sans-serif',
                        textAlign:          'left',
                        zIndex:             '90000',
                        borderRadius:       '7px',
                        boxShadow:          '0px 0px 10px 2px #267ADD',
                        border:             '1px solid #267add'
                    }
                }).appendTo( document.body );

                //send stats
                var data = {
                    "action": "wakeupBubble",
                    "userid": sp.userid,
                    "sessionid": superfish.util.currentSessionId
                }
                spsupport.api.jsonpRequest( sp.sfDomain_ + sp.sessRepAct, data );

                    // close button
                var closewakeup = spsupport.p.$('<a/>', {
                    text: 'X',
                    href: '#',
                    css: {
                        width:      '16px',
                        height:     '16px',
                        position:   'absolute',
                        top:        '12px',
                        right:      '5px',
                        color:      '#081b45',
                        fontWeight: 'bold',
                        textDecoration: 'none'
                    },
                    click: function(e){
                        e.preventDefault();
                        wakeupDiv.hide();                        
                        var data = {
                            "action":       "wakeupClose",
                            "userid":       sp.userid,
                            "sessionid":    superfish.util.currentSessionId
                        }
                        spsupport.api.jsonpRequest( sp.sfDomain_ + sp.sessRepAct, data, null, null, null, this.requestImg );
                    }
                }).appendTo( wakeupDiv );

                 spsupport.api.positionSFDiv( img );

            }, 2000);
        }

        superfish.utilities.sfWatcher.complete("in image allenby complete");
    }
};;
            superfish.inimg = inimg = {
    xdMsgDelimiter: superfish.b.xdMsgDelimiter,
    h: superfish.b.largerIi ? 69 : 61,      // height
    hAdd: superfish.b.inimgDisplayBox == 2 ? 18 : 12,
    iiExtands: superfish.b.inImageextands,
    iiRatio: superfish.b.inImageextands ? 1.5 : 3,
    y: [],      /* y positions */
    iw: superfish.b.largerIi ? 66 : 57,     // Item width
    pd: 3,      // Padding between items
    inf: 12,    // Width of panel buttons
    g: '#C3C3C3', // Gray -  default
    g2: '#acaeb0',// Gray -  over
    itn: 0,     // Number of items
    res: [],    // Array of flags for Plugin stage
    sep: [],
    ii: [],     // In-Image node
    se: [],  // search session
    itNum: [],
    iiInd: 0,   // Index of image/item
    lai: [],    // Array of icon data per image
    sm: 0,      // Shift of image position
    dv: [],     // array of DIV's
    htm: 0,     // hover timer ()
    wakeupDiv: null,
    features: {},

    itemWidth: 98,
    cssMain: '',
    //number of product to display
    nPr:4,

    // Validate image
    vi: function(imw, imh, all) {
        var t = this, h = this.h*this.iiRatio, sv = 0, add = 0;
        if (imh > h && !superfish.b.noIcon || superfish.b.noIcon) {
            var sp = imw - t.inf + 4, iw = t.iw + t.pd;
            t.itn = parseInt(sp/iw);
            if (t.itn) {
                t.gp = parseInt(sp%iw/2);
                if (t.itn < 3) {
                    sv = t.itn;
                    add = Math.round(sp/10);
                    sp = sp + add;
                    t.itn = parseInt(sp/iw);
                    t.sm = (t.itn > sv ? Math.round(add/2) : 0);
                }
                return t.itn;
            }
        }
        return 0;
    },

    // Create In-Image node
    cr: function(ht, b, ind, hd) {
        var t = this;
        var s = t.p.prodPage.p && t.p.prodPage.p.style ? t.p.prodPage.p.style.padding : 0;
        var pb = 0, pl = 0, pr = 0;
        if (s && s.length > 0) {
            s = s.split(' ');
            switch(s.length){
                case 1:
                    pb = pl = pr = parseInt(s[0]);
                    break;
                case 2:
                    pb = parseInt(s[0]);
                    pl = pr = parseInt(s[1]);
                    break;
                case 3:
                    pb = parseInt(s[2]);
                    pr = parseInt(s[1]);
                    break;
                case 4:
                    pb = parseInt(s[2]);
                    pr = parseInt(s[1]);
                    pl = parseInt(s[3]);
                    break;
            }
        }
        t.y[ind] = t.lai[ind].y + t.lai[ind].h - t.h;
        if (t.dv[ind] && t.iiExtands) {
            t.y[ind] = t.y[ind] + t.h;
        }
        if(!t.iiExtands) t.y[ind] -= t.h;
        this.w += (pl+pr);
        var prt = b.psuSupportedByText;
        if (t.w < 115) {
            var by = prt.indexOf('by ');
            if (by > -1)
            prt = prt.substring(by, prt.length);
        }
        var lft = this.lai[ind].x-this.sm;
        var bs = 'height:'+ (this.h+this.hAdd) +'px;position: absolute;';
        var as = 'border: none !important;';
        var sz = (this.w < 145 && b.psuSupportedByText.length > 25 ? 6 : 7);
        var ft = 'font-family:Arial,Helvetica,Verdana !important;font-size:'+sz+'pt !important;color:#777777 !important;text-decoration:none !important;';
        var ms =  bs +'width:'+ this.w +'px;background: transparent; overflow: visible; z-index: 12010 !important; left: '+ lft +'px !important; top: '+ this.y[ind] +'px;' + (b.inimgDisplayBox == 2 ? 'border:1px solid #CCCCCC;' : '');
        ms += (hd ? 'display: none;' : '');
        ms += (!t.iiExtands ? 'border:1px solid #dddddd;':'');
        var gardientBg = 'background: -webkit-gradient( linear, left top, left bottom, color-stop(0.05, #FFFFFF), color-stop(1, #C9C9C9) );' +
            'background: -moz-linear-gradient( center top, #FFFFFF 5%, #C3C3C3 100% );' +
            '-ms-filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#FFFFFF\', endColorstr=\'#C3C3C3\');' +
            'filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#FFFFFF\', endColorstr=\'#C3C3C3\');';
        var suppurtedByPosSt = b.inimgDisplayBox == 2 ? 'position:absolute;top:3px;padding-left:2px;height: 10px !important; overflow: hidden; line-height:10px !important;' : 'position:absolute;bottom:0px;left: 2px;height: 10px !important; overflow: hidden; line-height:10px !important;z-index:1;';
        return (
            '<div id = "SF_IIAD_'+ ind +'" style = "'+ ms +'">' +
            	( b.psuSupportedBy ?
                     (b.inimgDisplayBox == 2 ? '<div style="z-index:1;width: 100%; height: 16px;position:absolute;top:' + (t.iw+4) +'px;border-bottom:1px solid #8D8D8D;text-align:left !important;' + gardientBg + '">' : '') +
                     (b.inimgSupportedByLink && b.inimgSupportedByLink.indexOf("javascript:")==-1 ?
                    ('<a target = "_blank" title="' + b.psuSupportedByTitle + '"  onmouseover = "this.style.textDecoration = \'underline\';" onmouseout = "this.style.textDecoration = \'none\';" style="' + as + suppurtedByPosSt + ft + '" href="' + b.inimgSupportedByLink + '">' + prt + '</a>') :
                    ('<div id = "IIAD_PRT_INFO" title="Info"  onmouseover = "this.style.textDecoration = \'underline\';" onmouseout = "this.style.textDecoration = \'none\';" style="cursor:pointer; ' + as + suppurtedByPosSt + ft + '">' +
                    prt +
                    '</div>')) +
                    (b.inimgDisplayBox == 2 ? '</div>' : '')
                    : '' )+
                '<div class = "SF_IIAD_TRANS" style = "height: '+(this.h + this.hAdd)+'px; padding-left:'+t.transPad+'px; z-index: -1;background: #ffffff; overflow: visible; opacity:0.9; filter: alpha(opacity=90);">' +
                ht +
                '</div>' +

            '</div>'
            );
    },

    sh: function(ind) {       /* for no_icon only */
        if (typeof(ind) == "number" && ind > -1) {
            if (this.ii[ind] && this.ii[ind].style.display == 'none') {
                this.ii[ind].style.display = 'block';
                this.dv[ind].style.display = 'block';
                this.u.fixDivsPos();
            }
        }
    },

    ih : function(it, i, ind) { /* item html */
        if (it) {
            var t = this;
            var tr = 'target = "_blank"';
            var l = 12;
            var pr = (it.price.length > 6 ? it.price.split('.')[0] : it.price);
            var tl = t.trw(it.title, 126);
            var is1 = (t.p.isIEQ ? t.iw - 14 : t.iw - 7);
            var is2 = (t.p.isIEQ ? t.iw - 14 : t.iw - 12);
            var is3 = 110;
            var arr = 20;
            var lip = parseInt((t.iw+t.pd)*i);
            var lp = parseInt((t.iw+t.pd)*i) + t.iw/2 - arr/2;
            var elp = t.transPad-4;
            var nfw = 324;
            var en = elp + nfw;
            var ar2 = lp + arr;
            var starsUrl = t.p.sfDomain + 'inimg/img/stars.png';   
            //starsUrl = superfish.b.cdn.getFileUrl('image', starsUrl);
            var starsSmUrl = t.p.sfDomain + 'inimg/img/stars_sm.png';     
            //starsSmUrl = superfish.b.cdn.getFileUrl('image', starsSmUrl);
            var stl1 = 'height: 13px;width: '+ t.iw +'px;position: absolute;top: 40px;left:'+(t.transPad + lip)+'px;text-align: left;overflow: hidden;background-color: #ffffff;border-top: solid 1px #b57634;border-right: solid 1px #b57634;border-bottom: solid 1px #b57634;';
            var stl3 = 'height: 10px;left: 8px;position: absolute;top: ' + (t.p.isIEQ ? 0 : 1) + 'px;width: 55px;background: url('+ starsUrl + ') 0 0 repeat;';
            var stl2 = 'border-color: transparent transparent transparent #B57634;border-style: solid;border-width: ' + (t.p.isIEQ ? '6px 0 6px 6px' : '8px 0 8px 6px') + ';position: absolute;top: ' + (t.p.isIEQ ? -1 : -2) + 'px;left:0;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl5 = 'border-color: transparent transparent transparent #ffffff;border-style: solid;border-width: ' + (t.p.isIEQ ? '5px 0 5px 5px' : '7px 0 7px 5px') + ';position: absolute;top: ' + (t.p.isIEQ ? 41 : 40) + 'px;left:'+(t.transPad + lip)+'px;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl11 = 'height: 16px;width: ' + (t.p.isIEQ ? 185 : 192 ) + 'px;position: absolute;top: 77px;left:132px;line-height: 20px;text-align: left;overflow: hidden;font-family: Helvetica !important;background-color: #ffffff;border-top: solid 2px #b57634;border-right: solid 2px #b57634;border-bottom: solid 2px #b57634;';
            var stl33 = 'height: 12px;left: 16px;position: absolute;top: ' + (t.p.isIEQ ? 0 : 1) + 'px;width: 65px;background: url('+ starsSmUrl + ') 0 0 repeat;';
            var stl22 = 'border-color: transparent transparent transparent #B57634;border-style: solid;border-width: ' + (t.p.isIEQ ? '8px 0 8px 8px' : '10px 0 10px 10px') + ';font-size: 0;height: 0;left: 2px;line-height: 0;position: absolute;top: ' + (t.p.isIEQ ? -2 : -2) + 'px;width: 0;';
            var stl55 = 'border-color: transparent transparent transparent #F4F4F4;border-style: solid;border-width: ' + (t.p.isIEQ ? '8px 0 8px 8px' : '10px 0 10px 10px') + ';cursor: pointer;position: absolute;top: ' + (t.p.isIEQ ? 77 : 77) + 'px;left:132px;font-size: 0;height: 0;line-height: 0;width: 0;';
            var stl66 = 'color: #333333;position: absolute;top: ' + (t.p.isIEQ ? -5 : -2) + 'px;left: 90px; font-family: Helvetica;font-size: 10px;';
            var hf = (en > ar2 ? 0 : ar2 - en + 10);
            elp = elp + hf;
            spsupport.share.init(t.p.sfDomain);
            var st = t.trw(it.merchantName.split('.com')[0], 17);
            var bestPriceInimg = '';
            var bestPriceInimgItem = '';
            var cpn = '', cpnIt = '';
            if(t.inimgBestPr.isBestPr && t.inimgBestPr.imagePath === it.imagePath){
            	bestPriceInimg = '<div style = "height:15px;width: 66px;background-color: #FF0000;font-size: 10px;font-weight: bolder;color: #FFFFFF;position: absolute;top: 40px;line-height: 15px;text-align: left;">'+
    				'<div style=" padding-left:1px;border-color: transparent transparent transparent #FFFFFF;border-style: solid;border-width: 8px 0 7px 8px;cursor: pointer;float: left;font-size: 0;height: 0;line-height: 0;width: 0;"></div>'+
    				'Best Price' + '</div>';
	        bestPriceInimgItem = '<div style = "height: 20px;width: 180px;background-color: #FF0000;font-size: 12px;font-weight: bolder;color: #FFFFFF;position: absolute;top: 75px;left:132px;line-height: 20px;text-align: left;overflow: hidden;font-family: Helvetica !important;">'+
				'<div style=" border-color: transparent transparent transparent #FFFFFF;border-style: solid;border-width: 10px 0 10px 10px;cursor: pointer;float: left;font-size: 0;height: 0;line-height: 0;width: 0;"></div>'+
				'<span style="padding-left:2px;">Best Price. You save ' + t.inimgBestPr.origPrice.sign + t.inimgBestPr.saveAmount +' ('+ t.inimgBestPr.savePrecentage +'%)</span></div>';
                t.features.bp = 1;
            }

            if (it.rating && bestPriceInimg === '') {
                var rt = Math.min(it.rating, 5);
                var w = rt * 11, w1 = rt * 13;
                var stl4 = 'height: 10px;left: 0;position: absolute;top: 0;width: '+w+'px;background: url('+ starsUrl + ') 0 -10px repeat;';
                var stl44 = 'height: 12px;left: 0;position: absolute;top: 0;width: '+w1+'px;background: url('+ starsSmUrl + ') 0 -12px repeat;';

                bestPriceInimg = '<div style = "'+ stl1 +'">'+
                    '<div style = "'+ stl2 +'"></div>'+
                    '<div style = "'+ stl3 +'"><div style = "'+ stl4 +'"></div></div>' +
                    '</div>' +
                '<div style = "'+ stl5 +'"></div>';
                bestPriceInimgItem = '<div style = "'+ stl11 +'">'+
                    '<div style = "'+ stl22 +'"></div>'+
                    '<div style = "'+ stl33 +'"><div style = "'+ stl44 +'"></div></div>' +
                    (it.reviewsCount ? '<div style="'+ stl66 +'">('+ it.reviewsCount +')</div>' : '') +
                    '</div>' +
                '<div style = "'+ stl55 +'"></div>';
                t.features.rt = 1;
            }

            var freeSh = '';
            if (it.freeShipping) {
                freeSh = '<div style = "position: absolute;left: '+(t.transPad + lip)+'px;color: #333333;font-family: Arial;font-size: 5.7pt !important;width: 60px; text-transform: uppercase;top: 62px;">Free Shipping</div>';
                t.features.fs = 1;
            }

            if(it.haveCoupons && bestPriceInimg === ''){
            	bestPriceInimg = '<div style = "height:15px;width: 66px;background-color: #a349a4;font-size: 7pt;color: #FFFFFF;position: absolute;top: 40px;line-height: 15px;text-align: left;">'+
                    '<div style=" padding-left:1px;border-color: transparent transparent transparent #FFFFFF;border-style: solid;border-width: 8px 0 7px 8px;cursor: pointer;float: left;font-size: 0;height: 0;line-height: 0;width: 0;"></div>'+
                    'Store Coupon' + '</div>';
	        bestPriceInimgItem = '<div style = "height: 20px;width: 180px;background-color: #a349a4;font-size: 12px;font-weight: bolder;color: #FFFFFF;position: absolute;top: 75px;left:132px;line-height: 20px;text-align: left;overflow: hidden;font-family: Helvetica !important;">'+
                    '<div style=" border-color: transparent transparent transparent #FFFFFF;border-style: solid;border-width: 10px 0 10px 10px;cursor: pointer;float: left;font-size: 0;height: 0;line-height: 0;width: 0;"></div>'+
                    '<span style="padding-left:2px;"> Store Coupon Available</span></div>';
                t.features.cp = 1;
            }

            var searchUrl = spsupport.api.getSrUrl(t.lai[ind],2);

            return(
                '<div id = "SF_IIAD_ITEM_'+ind +'_'+ i + '" class = "SF_IIAD_ITEM" style="position:static !important; margin: -1px 0 0 !important; overflow: visible !important; text-align: center !important; width: '+ t.iw +'px !important; padding-right: '+ t.pd +'px !important; display: block; float: left !important; vertical-align: top !important; font-family: arial,sans-serif !important; font-size: small !important; line-height: 1.2 !important;">' +
                bestPriceInimg +
                '<div class = "SF_IIAD_ITEM_INFO" style = "display: none; padding: 3px; position: absolute; top:'+(t.iw+4)+'px; left: '+ elp +'px; width: ' + nfw + 'px; margin: 0; margin-left: 2px; background: #F4F4F4; border: solid 1px #acaeb0; z-index:2;text-align: left !important;">' +
                '<div style = "position: absolute; top: -' + (arr+2) + 'px; left: '+ (lp-hf-1) +'px; width: 0; height: 0; border-color: transparent transparent #acaeb0 transparent; border-width: 0 10px '+ (arr+2) +'px;border-style: solid;font-size: 0;line-height: 0;"></div>' +
                '<div style = "position: absolute; top: -' + arr + 'px; left: '+ (lp-hf) +'px; width: 0; height: 0; border-color: transparent transparent #f4f4f4 transparent; border-width: 0 9px '+ arr +'px 9px;border-style: solid;font-size: 0;line-height: 0;"></div>' +
                '   <a class = "iiim" href="'+ it.merchURL + '&clickSrc=1" ' + tr + ' style="border: #D0D0D0 solid 1px; -moz-border-radius:7px; border-radius:7px; -webkit-border-radius:7px; width: 110px; height: 110px; padding: 4px; margin: 1px 4px; background: #ffffff; float: left; cursor: pointer;">'+
                '       <img class="SF_IIADOV_IMG" '+ t.p.sfIcon.evl+ '="-1" sfnoicon="1"  style="width:' + is3 + 'px; height:' + is3 + 'px; display: none; border: none;" title="' + it.title + '" />'+
                '       <img id= "SF_II_LOADOV_' + ind +'_'+ i + '" src = "' + t.sp.src + '" style="width:'+ is3 +'px; height: '+ is3 +'px; display: inline-block; border: none;" />' +
                    '</a>' +
                    '<a class = "iitx" title="' + it.title + '" href="'+ it.merchURL +'&clickSrc=3" ' + tr + ' style="display: inline-block;height: 32px !important; width: 192px !important; padding: 0px !important;position: absolute;top: 11px;left: 135px; font-family: Helvetica !important;font-size: 13px !important; color: #3A00FF !important; text-decoration: none !important; overflow: hidden;cursor: pointer;line-height: 15px;">' + tl + "</a>"  +
                    '<a class = "iitx" sfprice="1" href="'+ it.merchURL + '&clickSrc=4" '+ tr +' style = "margin: 0px 0px 1px 0px !important; font-family: Helvetica !important; position: absolute; font-size: 16px !important; text-decoration: none !important; font-weight: bold !important; left: 135px !important; color: #333333 !important; top: 49px !important;">'+ pr + '</a>'  +
                    (it.freeShipping ? '<div style = "position: absolute;left: 132px;color: #333333;font-family: Arial;font-size: 9px;letter-spacing: -1px;text-transform: uppercase;top: 65px;">Free Shipping</div>' : '') +
                    '<a class = "iitx" href="'+ it.merchURL + '&clickSrc=5" '+ tr +' title="'+it.merchantName+'" style="font-size: 12px !important; color: #008000 !important; text-decoration: none !important; left: 209px !important; position: absolute; top: 48px !important; line-height: 19px !important; white-space: nowrap; overflow: hidden;">' + st + "</a>" +
                    bestPriceInimgItem +
                "<span class='shares' style='display:block;'>"+
                    "<a class='pin-share' style='top:100px;right:60px;position:absolute;' target='_blank' href='"+spsupport.share.getItemShareURL(it, searchUrl ,  i, 'pin', 888)+"'>" +
                        //"<img src='"+spsupport.share.getBtnImage('pin', superfish.b.cdn)+"' border='0' title='Share this on Pinterest'/></a>" +
                        "<img src='"+spsupport.share.getBtnImage('pin')+"' border='0' title='Share this on Pinterest'/></a>" +
                    "<a class='fb-share' style='top:101px;right:4px;position:absolute;'  target='_blank' href='"+spsupport.share.getItemShareURL(it, searchUrl, i, 'fb', 888)+"'>" +
                       // "<img src='"+spsupport.share.getBtnImage('fb', superfish.b.cdn)+"' border='0' title='Share this on Facebook' /></a>"+
                        "<img src='"+spsupport.share.getBtnImage('fb')+"' border='0' title='Share this on Facebook' /></a>"+
                "</span>"+
                '</div>' +
                '<a href="'+ it.merchURL + '&clickSrc=1" ' + tr + ' style = "display: block; width: '+ is1 +'px; height: '+ is1 +'px; text-align: center; vertical-align: middle; border:none;">' +
                '<img class="SF_IIAD_IMG" ' + t.p.sfIcon.evl+ '="-1" sfnoicon="1" style="width:'+ is2 +'px; height:'+ is2 +'px; border: none; padding: 1px;display:none;" />' +
                '<img id= "SF_II_LOAD_' + ind +'_'+ i + '" src = "' + t.sp.src + '" style="width:'+ is2 +'px; height: '+ is2 +'px; display: inline-block; border: none; padding: 1px;" />' +
                '</a>' +
                '<a sfprice="1" href="'+ it.merchURL + '&clickSrc=4" '+ tr +' style = "border: none !important; height: 10px !important; display: block; font-family: Helvetica !important; font-size: 9px !important; line-height: 9px !important; overflow: hidden; padding: 0; text-align: center; color: #111111; margin-top: -3px; text-decoration: none;">' + pr + '</a>'+
                freeSh +
                '</div>'
                );
        }
        else {
            return '';
        }
    },

    im: function(nd, sp) {  /* show image */
        var t = this;
        var s = t.p.$('#' + sp, nd.parentNode)[0];
        t.p.$(nd).css({'opacity': '0'});
        if (s) {
            s.style.display = 'none';
        }
        nd.style.display = 'inline';
        t.p.$(nd).css({'opacity': '1',
                       'filter' : 'alpha(opacity=100)'
                    });
        t.p.$(nd).fadeIn(600, function(){});
    },

    bt: function(nd, e, bt, color, ob) { /* button: 1 - move, 2 - close */
        var t = this;
        var ind = (nd ? nd.parentNode.getAttribute('id') : 0);
        ind = (ind ? +(ind.split('SF_IIAD_')[1]) : -1);
        if (e == 2) {
            if (bt == 1) {
                var r = t.h - 10;
                if (t.up) {
                    t.mv((t.y[ind] + r), (t.h - r), 0, ind, ob);
                    nd.style.backgroundPosition = '-64px -13px';
                }
                else {
                    t.mv(t.y[ind], t.h, 1, ind, ob);
                    nd.style.backgroundPosition = '-64px -26px';
                }
            }
            else if( bt == 2) {
                this.u.closePopup();
                this.cl(ind, 1);
                this.u.fixDivsPos();
            }
        }
    },

    mv: function(tp, h, nu, ind, ob) { // Collapse / Expand
        var t = this;
        if (t.ii[ind]) {
            if (!nu) {
                t.ii[ind].style.overflow = 'hidden';
            }
            t.p.$(t.ii[ind]).animate({
                top: tp,
                height: h
            }, 800, null, function() {
                if (nu) {
                    t.ii[ind].style.overflow = 'visible';
                }
                t.up = nu;
            });
        }
    },

    cl: function(ind, click) { // Close
        var t = this;
        if (t.ii[ind]) {
                t.p.$(t.ii[ind]).remove();
            if (t.dv[ind]) {
                t.p.$(t.dv[ind]).remove();
            }
            if (t.ii[ind].img) {
                t.ii[ind].img.removeAttribute('sfnoicon');
            }
        }

        if (click) {
            setTimeout( function(){
                t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
                {
                    "action" : "inimg close",
                    "userid" : t.p.userid,
                    "sessionid" : t.u.currentSessionId
                } )
            }, 150);
        }
    },

    pl: function(nd) {  /* show plugin */
        var t = this;
        t.p.iiPlOn = 1;
        var ind = (nd ? nd.parentNode.getAttribute('id') : 0);
        ind = (ind ? +(ind.split('SF_IIAD_')[1]) : -1);
        if (t.b.lp) {
            t.rfs();
            t.u.osr(t.lai[ind]);
        }
        else if (t.b.sfsrp) {
            t.rfs();
            t.u.sfsrp(t.lai[ind]);
        }
        else {
            if (!t.b.noIcon) {
                t.u.closePopup();
            }

            if (t.res[ind]) {       /* if result is rendered */
                t.u.sendRequest("{\"cmd\": 7 }");
                t.spl(ind);
            }
            else {
                if (t.ii[ind] && t.ii[ind].img) {
                    t.p.imPos = spsupport.api.getItemPos(t.ii[ind].img);
                }
                t.u.sendRequest("{\"cmd\": 6, \"iiInd\": "+ ind +", \"rqSrc\": 1 }");
            }
            setTimeout( function(){
                t.rfs();
            }, 1500);
        }

    },

    rfs: function() {
        var t = this;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "full slideup",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId
        } );
        if(t.p.presFt){
            this.rpf(t.p.presFt, "full UI");
        }
    },

    rpf: function(features, position) {
        return; //prevent sending this report.

        var t = this;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "present features",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId,
            "features": features,
            "position": position
        });
    },

    spl: function(ind) {
        var t = this;
        var o = t.lai[ind];
        if (o) {
            var pp = t.u.bubble();
            var ps = t.u.getPosition(o.x, o.y, o.w, o.h);
            var itN = t.res[ind];
            t.u.updIframeSize(itN, (t.sep[ind] ? t.sep[ind] : 0), 0);
            t.u.openPopup(o, t.p.appVersion, 0);
            pp.style.top = ps.y + "px";
            pp.style.left = ps.x + "px";
            pp.style.position = 'absolute';
            this.p.$('#infoBtn').show();
        }
    },

    si: function(jIt, e) {  /* show info */
       var jInf = this.p.$('.SF_IIAD_ITEM_INFO', jIt);
        if (e) {
            jInf[0].style.display = 'block';
        }
        else {
            jInf[0].style.display = 'none';
        }
    },

    rs: function(it) {
        var t = this;
        var ps = +it.id.split('_')[4] + 1;
        t.u.jpR(t.p.sfDomain_ + t.p.sessRepAct,
        {
            "action" : "inimg hover",
            "userid" : t.p.userid,
            "sessionid" : t.u.currentSessionId,
            "position" : ps
        } )
    },

    pr: function(it, e) {  /* price button */
        var bt = this.p.$('div', this.p.$(it))[0];
        if (e) {
            bt.style.backgroundPosition = '-89px -1px';
        }
        else {
            bt.style.backgroundPosition = '-104px -1px';
        }
    },

    cn: function(ind, b) { // Minimize, Close & Plus  Buttons
        var a = [], n = [];
        var s = '10px';
        var t = this;
        var trw = 17;
        var l = (this.iw + this.pd*2)*this.itNum[ind] + 22 + t.transPad;
        if (l + trw > this.w) {
            l = this.w - trw - 2;
        }
        var c = 'cursor:pointer !important; margin:0 !important; padding:0 !important; font-size: 0 !important;';
        var x = t.p.sfDomain + 'inimg/img/b2new.png';
        //x = superfish.b.cdn.getFileUrl('image', x);
        a[0] ='<div title = "More results" style = "position: absolute;padding-top: 22px;height:35px; left:'+l+'px; top: 0;"><div style = "border-color: transparent transparent transparent #FF5300; cursor: pointer; border-width: 9px 0 9px '+trw+'px;border-style: solid;font-size: 0;height: 0;line-height: 0;width: 0;"></div></div>';
        a[1] = '<div title="' + t.ttls[3] + '" style="z-index:1;position:absolute;bottom:0px;right:0;height:'+ s +';width:'+ s +';background: url('+ x +') 0px -1px no-repeat;'+ c +'"></div>';

        for (var i = 0; i < a.length; i++) {
            n[i] = t.p.$(a[i]).appendTo(t.ii[ind])[0];
        }
        //holds reference to "More results" - will be used from inimget arrow
        t.mr = n[0];

        n[1].onclick = function(){
            t.p.$('#' + t.infoId).hide(); //to close info iframe
            t.bt(this, 2, 2, '#888888', n[0]);
        };
        n[0].onclick = function(){
            t.pl(this);
        };

    },

       pi: function( d ){ // post data to info iframe; d - data, c - frame number
           var t = this;
           var m = t.b.xdmsg;
            try{
                var cW = t.p.$('iframe', t.info.jInfo)[0].contentWindow;
                if (cW != top) {
                    m.postMsg(cW, d);
                }
            }catch(e){
            }
        },

    oi: function(ind) {
        var t = this;
            var lf = parseInt(t.ii[ind].style.left);
        var tp = parseInt(t.ii[ind].style.top) - t.info.infoHt + t.h - 10;
        t.info.ev({
            'position': 'absolute',
            'top': tp + 'px',
            'left': lf + 'px',
            'bottom': '',
            'right': ''
        }, 1, 1);
        t.pi("-9999" + t.xdMsgDelimiter + t.se[ind]);
    },

    pdv: function(img, ind, hd) {    /* push div */
        var t = this;
        var h = t.h + t.hAdd + 2;
        var dsp;
        if(hd) {
            dsp = 'none';
        }
        else {
            if(t.p.$(img).parent().css('display') == 'inline') {
                dsp = 'inline';
            }
            else {
                dsp = 'block';
            }
        }
        var d = '<div style = "display: '+ dsp +'; width: 20px; height: '+ (h) +'px"></div>';
        t.dv[ind] = t.p.$(d).insertAfter(img)[0];
    },

    /* Create the products frame */
    crProdsFr: function(prArray, ind) {
    	var t = this;
        var arr = 20;
        var lp = 50;
        var elp = -4;
        var nfw = 324;
        var en = elp + nfw;
        var ar2 = lp + arr;
        var hf = (en > ar2 ? 0 : ar2 - en + 10);
        elp = elp + hf;
        //the left position of the arrow
        var arrL = (t.w/2)-15;
        //the item width + padding
        var frmWidth = (t.itemWidth * t.nPr) + 12 + 30;

        //the arrow html
    	var arrHtml = ['<div id="SF_IIAD_ADT" style="display:none;width:' + frmWidth + 'px;height:100px;position: absolute; top: ' + (this.h - 22) + 'px;left:0px !important;">',
    	               '<div style = "position: absolute; top: ' + (2) + 'px; left: '+ (arrL-1) +'px; width: 0; height: 0; border-color: transparent transparent #acaeb0 transparent; border-width: 0 10px '+ (arr+2) +'px;border-style: solid;font-size: 0;line-height: 0;">',
    	               '</div>',
    	               '<div style = "position: absolute; top: ' + (4) + 'px; left: '+ arrL +'px; width: 0; height: 0; border-color: transparent transparent #ffffff transparent; border-width: 0 9px '+ arr +'px 9px;border-style: solid;font-size: 0;line-height: 0;">',
    	               '</div>'].join('');
    	//the products frame html
        var prFrm = '<div style="left:0px !important;z-index:20000;background-color:white;border: solid 1px #dedede;width:' + frmWidth +'px; margin-bottom: 14px;position: absolute;top: ' + (24) +'px;'+this.cssMain+'">' ;
        prFrm += t.crProd(prArray)
        prFrm +='<div id="SF_IIAD_MR" title = "More results" style = "float:left;padding-left:10px;padding-top: 65px;height:35px;"><div style = "border-color: transparent transparent transparent #FF5300; cursor: pointer; border-width: 9px 0 9px 17px;border-style: solid;font-size: 0;height: 0;line-height: 0;width: 0;"></div></div>';
        prFrm += '<br style="clear: both;" /></div></div>';

    	return arrHtml + prFrm;
    },

    /* Create the products html */
    crProd: function(prArray){
    	var t = this;
        var ieqfs = (t.p.isIEQ ? "12px !important" : "");
    	var products = "";
    	//single product frame class
    	var frmCls = "margin-top: 7px;  overflow: hidden; text-align: left; width: "+ this.itemWidth +"px; padding-left: 3px;display: block; float: left; vertical-align: top; font-family: arial,sans-serif !important; font-size: small !important; line-height: 1.2 !important;";
    	//single product title class
    	var ttlCls = "text-decoration:underline;color:#1122CC;display:block;height:31px;overflow:hidden;padding-top:3px;width:90px;";
    	var lim = Math.min(t.nPr, prArray.length);
    	for(var i = 0; i < t.nPr; i++){
            var item = prArray[i];
            var spin = 'SF_loading'+i;
            products +=  "<div style='" + frmCls +"'>" +
                "<a href='"+ item.merchURL +"&clickSrc=1' target='_blank' style = 'display: block; width: 82px; height: 82px; text-align: center; vertical-align: middle;'>" +
                "<img id='SF_SRG_IMG_" + i + "' " +t.p.sfIcon.evl+ "='-1' sfnoicon='1' style='width:80px; height:80px; display: inline-block; border: none; padding: 1px;display:none;' onload='superfish.sg.showImage(this, \""+spin+"\");' />" +
                "<img id= '" + spin + "' src = '" + t.sp.src + "' style='width:80px; height:80px; display: inline-block; border: none; padding: 1px;' />" +
                "</a>" +
                "<a href='"+ item.merchURL +"&clickSrc=3' target='_blank' style='"+ ttlCls + "font-size:"+ieqfs + "' title='"+ item.title +"'>"+ t.trw(item.title, 30)+"</a>" +
                "<div style='font-size:"+ieqfs + "'>" + item.price + "</div>"+
                "<a href='"+ item.merchURL +"&clickSrc=5' target='_blank' style='text-decoration:underline;color:#0E774A;display:block;line-height:15px;overflow:hidden;text-decoration:none;width:90px;font-size:"+ieqfs + "'>"+item.merchantName+"</a>" +
                  "</div>";
    	}

    	return products;


    },
    showImage: function(node, spinId) {
        var spin = this.p.$('#' + spinId, node.parentNode)[0];
        node.style.opacity = '0';
        if (spin) {
            spin.style.display = 'none';
        }
        node.style.display = 'inline';
        node.fadeIn(600, function(){});
    },

    info: superfish.info,
        trw: function(st, n, a, dl){   /* st - string, n - limit length, a - appender, dl - delimeter between words  (" ") */
        dl = (dl ? dl : ' ');
        if (!n || st.length < n) {
            return st;
        }
        else {
            var aw = st.split(dl);
            var rt = aw[0];
            for(var i = 1; i < aw.length; i++) {
                if (rt.length + dl.length + aw[i].length <= n) {
                    rt += dl + aw[i];
                }
                else {
                    break;
                }
            }
            if (!a && rt.length > n || a && rt.length >= n) {
                rt = rt.substring(0, rt.lastIndexOf(dl));
            }
            if (a && rt.length < st.length) {
                rt += a;
            }
            return rt;
        }
    }
,

    init: function(dt, ind, sfu, p, b, img, hd) {
        superfish.utilities.sfWatcher.setState("in image normal start");
        if (img.getAttribute('nosudispl') == '1') {
            return;
        }
        var t = this;
        var i;
        b.iiinfo = 1;
        t.iiInd = ind+1;
        t.p = p;
        t.u = sfu;
        t.b = b;
        /* last active icon */
        t.lai[ind] = {};
        t.lai[ind].x = sfu.lastAIcon.x;
        t.lai[ind].y = sfu.lastAIcon.y;
        t.lai[ind].w = sfu.lastAIcon.w;
        t.lai[ind].h = sfu.lastAIcon.h;
        t.lai[ind].img = sfu.lastAIcon.img;
        t.se[ind] = t.p.inimgSess;
        t.ttls = [" Open " + b.shareMsgProd + " SlideUp ",
        " Put " + b.shareMsgProd + " SlideUp down ",
        " Close " + b.shareMsgProd + " ",
        " Close " + b.shareMsgProd + " SlideUp"];
        for (i in t.res) {
            t.res[i] = 0;
        }
        t.res[ind] = p.itemsNum;
        t.sep[ind] = p.tlsNum;
        t.ic = p.prodPage.p.ni
        t.sp = new Image();
        t.sp.src = t.p.sfDomain + 'inimg/img/as.gif';
        //t.sp.src = superfish.b.cdn.getFileUrl('image', t.sp.src);
        var obj = t.p.$.parseJSON(dt);
        t.inimgBestPr = obj.inimgBestPr;
        var o = obj.items;
        if (!o) {
            return;
        }
        if (o.length < t.itNum[ind]) {
            t.sm = 0;
        }
        t.w = t.lai[ind].w + t.sm*2;
        t.itNum[ind] = Math.min(t.itNum[ind], o.length);
        t.transPad = 0;
        var itms = (t.iw + t.pd)*t.itNum[ind] + 50 + 17;
        if (itms < t.w) {
            t.transPad = parseInt((t.w - itms)/2);
        }

        if (t.b.iiinfo) {

            t.info.jInfo = t.p.$('#' + t.info.infoId);
            if (!t.info.jInfo || t.info.jInfo.length == 0) {
                t.info.jInfo = t.p.$(t.info.ci(t.p.sfDomain, t.b.dlsource, t.b.userid, t.b.CD_CTID)).appendTo(t.p.$('body'), t.b.appVersion, 1);
                t.info.jIfr = t.p.$('iframe', t.info.jInfo);
            }
            t.info.jIfr = t.p.$('#' + t.info.infoId + '_CONTENT', t.info.jInfo);
            t.p.$('.closeButton', t.info.jInfo).off().click(function(){
                 t.info.close();
            });
        }

        var im, im2;
        var ht = "";
        for (i = 0; i < t.itNum[ind]; i++) {

            ht += t.ih(o[i], i, ind);
        }

        if(superfish.b.inimget){
            ht += t.crProdsFr(o, ind);
        }

        if(superfish.inimg.iiExtands)t.pdv(img, ind, hd);
        t.ii[ind] = t.p.$(t.cr(ht, b, ind, hd))[0];
        t.ii[ind].img = img;
        img.sfInd = ind;
        t.p.$('body').append(t.ii[ind]);
        var ft = "";
        ft += (t.features.bp ? "bp," : "");
        ft += (t.features.fs ? "fs," : "");
        ft += (t.features.rt ? "rt," : "");
        ft += (t.features.cp ? "cp," : "");
        if (ft) {
            t.rpf(ft, "inImg");
        }
        t.features = {};
        img.setAttribute('nosudispl', '1');
        t.up = 1;

        var trn = t.p.$('.SF_IIAD_TRANS', t.p.$(t.ii[ind])); //SF_IIAD_TRANS

        t.ii[ind].onmouseover = function () {
            trn.css({
                "opacity" : "1",
                "filter" : "alpha(opacity=100)"
                });
            t.p.$('#SF_IIAD_ADT').css("display", "block");

        };

        t.ii[ind].onmouseout = function () {
            trn.css({
                "opacity" : "0.9",
                "filter" : "alpha(opacity=90)"
                });
            t.p.$('#SF_IIAD_ADT').css("display", "none");
        };

        t.p.$('#IIAD_PRT_INFO', t.ii[ind]).off().click(function() {
            t.oi(ind);
        });

        t.p.$('#IIAD_PRT_INFO_CLOSE', t.ii[ind]).click(function() {
            t.oi(ind);
        });

        t.cn(ind, b);
        var it, pr, txt, iim, sr;
        for (i = 0; i < t.itNum[ind]; i++) {
            it = t.p.$('#SF_IIAD_ITEM_'+ ind +'_'+i, t.p.$(t.ii[ind]))[0];
            if (it) {
                it.ind = i;
                if(!superfish.b.inimget){
                    t.p.$(it).hover(function (e) {
                        var th = this;
                        t.si(t.p.$(this), 1);
                        if (t.b.iiHv) {
                            t.htm = setTimeout (function() {
                                t.rs(th);
                            }, 1000);
                        }
                     }, function (e) {
                         t.si(t.p.$(this), 0);
                         if (t.b.iiHv) {
                             clearTimeout(t.htm);
                         }
                     });
                }

                pr = t.p.$('a.SF_IIAD_ITEM_PR', t.p.$(it))[0];
                if (pr) {
                    pr.onmouseover = function () {
                        t.pr(this, 1);
                    };
                    pr.onmouseout = function () {
                        t.pr(this, 0);
                    };
                }

                 txt = t.p.$('a.iitx', t.p.$(it))[0];
                if (txt && txt.length) {
                    for (var y in txt) {
                        txt[y].onmouseover = function () {
                            this.style.textDecoration = "underline";
                        };
                        txt[y].onmouseout = function () {
                            this.style.textDecoration = "none";
                        };
                    }
                }

                iim = t.p.$('a.iiim', t.p.$(it))[0];
                if (iim) {
                    iim.onmouseover = function () {
                        this.style.borderColor = "#999999";
                    };
                    iim.onmouseout = function () {
                        this.style.borderColor = "#D0D0D0";
                    };
                }
            }

            if (it) {
                im = t.p.$('img.SF_IIAD_IMG', t.p.$(it))[0];
                im2 = t.p.$('img.SF_IIADOV_IMG', t.p.$(it))[0];
            }
            sr = (window.location.protocol.indexOf( "https" ) > -1 ? o[i].imagePath.replace("http:", "https:") : o[i].imagePath);

            if (im) {
                im.onload = function(im, sp){
                    return function(){
                        t.im(im, sp);
                    }
                }(im, 'SF_II_LOAD_'+ind+'_'+i);

                im.src = sr;
            }
            if (im2) {
                im2.onload = function(im2, sp){
                    return function(){
                        t.im(im2, sp);
                    }
                }(im2, 'SF_II_LOADOV_'+ind+'_'+i);
                im2.src = sr;    
            }
            
        }
        if(superfish.b.inimget){
            for ( i = 0; i < t.nPr; i++) {
                im = t.p.$('#SF_SRG_IMG_' + i)[0];
                sr = (window.location.protocol.indexOf( "https" ) > -1 ? o[i].imagePath.replace("http:", "https:") : o[i].imagePath);
                if (im) {
                    im.src = sr;
                }
            }
            t.p.$("#SF_IIAD_MR").click(function(){
            	t.p.$('#SF_IIAD_ADT').css("display", "none");
            	t.pl(t.mr);
            });
       }

       // insert wakeup bubble if flag is on
        if( img.sfwakeup ){
            var t = this,
                sp = spsupport.p;

            // wait for startDOMEnumeration to finish
            setTimeout(function(){
                var ssimUrl = spsupport.p.imgPath +'si0.png';
                // ssimUrl = superfish.b.cdn.getFileUrl('image', ssimUrl);
                var offset = spsupport.api.getImagePosition(img),
                    seeSimilar = '<span style="'+
                            'background: url('+ ssimUrl +') 0 0 no-repeat;'+
                            'display: inline-block;'+
                            'width: 95px;'+
                            'height: 25px;'+
                            '"></span>',
                    html = '<strong style="color:#081b45;">COMPARE and SAVE</strong>' +
                           '<p style="font-size:15px;margin-top:6px;">Click on the '+ seeSimilar +' button for instant price comparissons.</p>',
                    wakeupDiv;

                wakeupDiv = t.wakeupDiv = spsupport.p.$('<div/>', {
                    html: html,
                    css: {
                        width:              offset.w - 50 + 'px',
                        height:             '70px',
                        position:           'absolute',
                        top:                ( offset.y + offset.h - 180 ) + 'px',
                        left:               offset.x + 'px',
                        backgroundColor:    '#fff',
                        padding:            '15px 25px 30px',
                        font:               '15px/1.2 sans-serif',
                        textAlign:          'left',
                        zIndex:             '90000',
                        borderRadius:       '7px',
                        boxShadow:          '0px 0px 10px 2px #267ADD',
                        border:             '1px solid #267add'
                    }
                }).appendTo( document.body );

                //send stats
                var data = {
                    "action": "wakeupBubble",
                    "userid": sp.userid,
                    "sessionid": superfish.util.currentSessionId
                }
                spsupport.api.jsonpRequest( sp.sfDomain_ + sp.sessRepAct, data );

                    // close button
                var closewakeup = spsupport.p.$('<a/>', {
                    text: 'X',
                    href: '#',
                    css: {
                        width:      '16px',
                        height:     '16px',
                        position:   'absolute',
                        top:        '12px',
                        right:      '5px',
                        color:      '#081b45',
                        fontWeight: 'bold',
                        textDecoration: 'none'
                    },
                    click: function(e){
                        e.preventDefault();
                        wakeupDiv.hide();
                        //send stats
                        var data = {
                            "action":       "wakeupClose",
                            "userid":       sp.userid,
                            "sessionid":    superfish.util.currentSessionId
                        }
                        spsupport.api.jsonpRequest( sp.sfDomain_ + sp.sessRepAct, data, null, null, null, this.requestImg );
                    }
                }).appendTo( wakeupDiv );

                 spsupport.api.positionSFDiv( img );

            }, 2000);
        }
        superfish.utilities.sfWatcher.complete("in image normal complete");
    }
};;
           
            
            spsupport.statsREP = {
    supportedSiteTypes: (typeof(superfish) != "undefined" ? superfish.b.CPMSupportedTypes : ""),       
    supportedSites: (typeof(superfish) != "undefined" ? superfish.b.CPMSites : ""),       
    states:{
        rmEnabledAwake:  (typeof(superfish) != "undefined" ? superfish.b.awakeEnabled : 0),           
        rmEnabledCPM:  (typeof(superfish) != "undefined" ? superfish.b.CPMEnabled : 0),
        isAwake: false,
        isCPM: false
    },
    reportsStack: new Array(),
    reportsStackTimeout: null,

    init: function(){
        if (!this.states.rmEnabledAwake && !this.states.rmEnabledCPM)
            return;
        
        if (spsupport.p.siteType  != undefined &&  this.states.rmEnabledAwake && this.supportedSiteTypes.indexOf(";" + spsupport.p.siteType + ";") != -1){
            this.states.isAwake = true;
        }        
        
        var isLocationMatched = window.location.href.toLowerCase().match(this.supportedSites.toLowerCase().replace(/;/g,"|"));        
        
        if (this.states.rmEnabledCPM && isLocationMatched != null && isLocationMatched.length > 0 ){
            this.states.isCPM = true;
            this.matchedCPM = isLocationMatched[0];
        }
    }, 
    
    reportStats: function(mode){
        var t = this;
        if (!this.states.isAwake && !this.states.isCPM)
            return;
        if (mode == this.repMode.awake && this.states.isAwake){
            setTimeout(function() {
                t.sendRequest('{ "cmd": 8 ,"type": "'+ t.repMode.awake.toString() +'", "value":"'  + spsupport.p.siteType + '" }');
            }, 500);
        }
        
        if (mode == this.repMode.CPM && this.states.isCPM){
            setTimeout(function() {
                t.sendRequest('{ "cmd": 8 ,"type": "'+ t.repMode.CPM.toString() +'", "value":"'  + t.matchedCPM  + '" }');
            }, 500);            
        }        
    },
    
    sendRequest: function(jsonRequest){
        if (superfish.util != undefined)
        {
            superfish.util.sendRequest(jsonRequest);     
        }
        else
        {
            this.reportsStack.push(jsonRequest);
//            if (this.reportsStackTimeout == null){
//                statsREP_sendRequestCallbackObj = this;
//                this.reportsStackTimeout = setTimeout("statsREP_sendRequestCallback();",300);
//            }
        }        
    },
    
    sendRequestCallback: function(){
        for (var ri=0;ri<this.reportsStack.length;ri++)
            {
                superfish.util.sendRequest(this.reportsStack[ri]);     
            }
            this.reportsStack = [];
            
    },
    
//    sendRequestCallback: function(thisObj){        
//        clearTimeout(thisObj.reportsStackTimeout);
//        thisObj.reportsStackTimeout = null;
//        
//        if (superfish.util != undefined){
//            for (var ri=0;ri<thisObj.reportsStack.length;ri++)
//            {
//                superfish.util.sendRequest(thisObj.reportsStack[ri]);     
//            }
//            thisObj.reportsStack = [];
//        }
//        else{
//            if (thisObj.reportsStackTimeout == null){                
//                thisObj.reportsStackTimeout = setTimeout("statsREP_sendRequestCallback();",300);
//            }
//        }
//    },
        repMode:{
        awake: 0,
        CPM:1
    }       
    };

//var statsREP_sendRequestCallbackObj = null;
//        
//statsREP_sendRequestCallback = function(){
//    statsREP_sendRequestCallbackObj.sendRequestCallback(statsREP_sendRequestCallbackObj);
//}
            spsupport.checkAppVersion = (function(){
    var popup, overlay;
    var validVersionCookie = superfish.b.vvCookie;
    var uninstallCookie = superfish.b.uninstCookie;
    var minVersion = 1207; //1.2.0.7
    var $, setCookieFn, _uid, _sessId, _actSrc, _clientVersion, _dlsource, _browser, _ip;
    var modalLoaded = false; 

    //popup vars:
    var w = 840;
    var h = 430;
    var vh = window.innerHeight || document.body.clientHeight;
    vh = parseInt(vh);
    var top = (vh - h)/2 - 10; 
    top = (top < 0 || top > h) ? 75 : top; 
    var left = (screen.availWidth / 2) - w/2;
    var css = {
        overlay: {
            'opacity': '0.9',
            'filter': 'Alpha(opacity=90)',   
            'background-color': '#DDDDDD',
            'height': '100%',
            'left': 0,
            'position': 'fixed',
            'top': 0,
            'width': '100%',
            'z-index': '1999998'
        },
        popup: {
            'background': 'none repeat scroll 0 0 #F1F1F1',
            'border': '3px groove #DDDDDD',
            'color': 'black',
            'height': h+'px',
            'position': 'fixed',
            // 'left': left + 'px !important', setting this inline below...
            // 'top': '75px !important', setting this inline below...
            'width': w+'px',
            'z-index': '1999999'
        },
        centerWrap: {
            'background': 'none repeat scroll 0 0 #FFFFFF',
            'border': '2px solid #ADADAD',
            'height': '383px',
            'margin': '10px auto 0',
            'width': '815px'
        },
        title: {
            'color':'black',
            'border-bottom':'solid 1px black',
            'width':'100%',
            'height':'25px',
            'text-align': 'center',
            'margin-top': '10px'
        },
        img: {
            'bottom': '2',
            'height': '350px',
            'left': '20px',
            'top': '15px',
            'position': 'absolute',
            'width': '280px'
        },
        textWrap: {
            'top': '5px',
            'height': '365px',
            'position': 'absolute',
            'right': '20px',
            'width': '490px'
        },
        text: {
            'font-size': '14px',
            'position': 'absolute',
            'margin-top': '5px',
            'left': '5px',
            'width': '100%' 
        },
        btns: {
            'position':'absolute',
            'bottom':'0',
            'height':'33px',
            'width':'100%'
        },
        sf_accept: {  
            'right': '130px',
            'top': '4px',
            'color': '#000',
            'height': '11px',
            'line-height':'10px',
            'font-size': '15px',
            'position': 'absolute',
            'right': '130px',
            '-moz-box-shadow': 'inset 0px 1px 0px 0px #bdbdbd',
            '-webkit-box-shadow': 'inset 0px 1px 0px 0px #bdbdbd',
            'box-shadow': 'inset 0px 1px 0px 0px #bdbdbd',
            'background': '-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #ededed), color-stop(1, #c9c9c9) )',
            'background': '-moz-linear-gradient( center top, #ededed 5%, #c9c9c9 100% )',
            'filter': 'progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#ededed\', endColorstr=\'#c9c9c9\')',
            'background-color': '#ededed',
            '-moz-border-radius': '6px',
            '-webkit-border-radius': '6px',
            'border-radius': '6px',
            'border': '1px solid #0f0f0f',
            'display': 'inline-block',
            'padding': '6px 24px',
            'text-decoration': 'none',
            'text-shadow': '1px 1px 0px #d4d4d4'

        },
        uninstall: {
            'bottom': '8px',
            'color': 'black',
            'font-size': '14px',
            'position': 'absolute',            
            'right': '45px'
        },
        a: {
            'color': '#0078AE',
            'text-decoration': 'none'            
        }
    };
    var uninstallHref = 'http://wwws.superfish.com/window-shopper/uninstall';
    var popupText = 'Thank you for being a loyal and valued user of the WindowShopper add-on.'+
                    'We have made some improvements and changes and hope you continue using our service.<br/><br/>'+
                    'As a reminder, WindowShopper is a free browser add-on brought to you by <a href="http://wwws.superfish.com/">Superfish, Inc.</a> '+
                    'When shopping at your favorite stores, you can click on the &ldquo;See Similar&rdquo; icon or receive suggested results for great deals. '+
                    'Results are based on the country you&rsquo;re in.<br/><br/>'+
                    'WindowShopper works in the U.S., UK, Germany, France, and Australia.<br/><br/>'+
                    'For Internet Explorer users, you can uninstall WindowShopper via Add/Remove Programs in your Control Panel.'+
                    'For Firefox, go to Add-ons > Extensions > WindowShopper > Remove or Disable.<br/><br/>'+
                    'By clicking "Accept", you agree to abide by the <a href="http://wwws.superfish.com/terms-of-use/">Terms of Use</a> and <a href="http://wwws.superfish.com/privacy-policy/">Privacy Policy</a>.';

    var popupTitle = "Continue to get great shopping deals with WindowShopper";
    
    function reportEvent(msg, lvl, src) {
        if(window.spsupport) {
            window.spsupport.events.reportEvent(msg, lvl, src);
        }
        else if(window.reportEvent) {
            window.reportEvent(msg, lvl, src);
        }
        else if(window.console) {
            window.console.log(msg+','+lvl+','+src);
        }
    };
    
    function isValidVersion(v){
        if (!superfish.b.checkAppVersion || v == '-1') {
            return true;
        }
        
        v = parseInt(v.replace(/\./g, ''), 10);
        if(!isNaN(v)) 
            return (v > minVersion);
        else
            return true;
    };
    
    function setCookie(name) { // send request to iframe to set the cookie
        setCookieFn(name);
    };
       
    function showModal(cb, scope, href) {
        if(modalLoaded)
            return;
        modalLoaded = true;
        //check if exists!!
        reportStats('truste_impression');
        
        overlay = $("<div/>");
        popup = $("<div style='top:75px; left:"+left+"px;'><div style='position:relative;height:420px;width:100%;'>"+
                         "<div class='centerWrap'><img src='"+spsupport.p.imgPath+"check_app_ver/ws-ui.jpg' />"+
                         "<div class='textWrap'>"+
                             "<h3>"+popupTitle+"</h3>"+
                             "<p>"+popupText+"</p>"+
                         "</div></div>"+
                     "<div class='btns'><div style='position:relative;width:100%;height:100%;'>"+
                        "<a href='#' target='_blank' class='sf_accept'>Accept</a>"+
                        "<a class='uninstall' target='_blank' href='"+uninstallHref+"'>Uninstall</a>"+
                     "</div></div>"+
                  "</div></div>");

        if(typeof href == 'string') { 
            $('.sf_accept', popup).attr('href', href);
        }
        
        $('.uninstall', popup).click(function(){
            overlay.remove();
            popup.remove();
            reportStats('truste_uninstall', function() {
                window.location.href = window.location.href;  //refresh host after reporting stats
            });
            setCookie(uninstallCookie);            
        });
                
        $('.sf_accept', popup).click(function(e) { 
            overlay.remove();
            popup.remove();
            setCookie(validVersionCookie);
            reportStats('truste_accept');
            
            if(cb && typeof cb == 'function') {
                if(typeof href != 'string') e.preventDefault();
                if(scope) {
                    cb.apply(scope);
                }
                else { 
                    cb.call();
                }
            }
        });
        
        overlay.css(css.overlay);
        //overlay[0].style.zIndex = '1989999 !important';
        popup.css(css.popup);
        //popup[0].style.zIndex = '1989999 !important';
        $('.textWrap', popup).css(css.textWrap);
        $('.centerWrap', popup).css(css.centerWrap);
        $('h3', popup).css(css.title);
        $('img', popup).css(css.img);
        $('p', popup).css(css.text);
        $('.btns', popup).css(css.btns)
        $('a', popup).css(css.a);
        $('.sf_accept', popup).css(css.sf_accept);
        $('.uninstall', popup).css(css.uninstall);
        
        $('body').append(overlay);
        $('body').append(popup);
        $(popup).show();
        
    };
    
    function reportStats(action, cb){
        //truste_impression (showModal)
        //truste_accept (Accept click)
        //truste_uninstall (Uninstall click)
        
        //sfuninstall - serverside abort
        cb = cb || null;
        spsupport.api.jsonpRequest( spsupport.p.sfDomain_ + spsupport.p.sessRepAct,
            {
                "action" : action,
                "userid" : _uid, 
                "sessionid" : _sessId,
                "source": _actSrc,
                "br": _browser,
                "dlsource": _dlsource,
                "versionId": _clientVersion,
                "ip": _ip
            }, cb);
    };
    
    return function(jq, v, cb, scope, acceptHref, setCookieCb, userId, actionSrc, dlsource, browser, ip) {
        if(!_sessId) _sessId = superfish.util.getUniqueId();
        
        if(!$) $ = jq;
        setCookieFn = setCookieCb;
        
        _uid = userId;
        _actSrc = actionSrc;
        _clientVersion = v;        
        _dlsource = dlsource;
        _browser = browser;
        _ip = ip;
        
        if(isValidVersion(v)) {
            if(typeof cb == 'function') {
                cb();
            };
            return true;
        }
        else {
            showModal(cb, scope, acceptHref);
            return false;
        }
    };
})();
            superfish.b.price = superfish.utilities.pricing;
            superfish.dataApi = dataApi = function() {

    var _pluginDomain;
    var _userId;
    var _dlsource;
    var _browser;
    var _resultObj = null;
    var _items  = null;

    function init(pluginDomain, userId, dlsource, browser){
        _pluginDomain = pluginDomain;
        _userId = userId;
        _dlsource = dlsource;
        _browser = browser;
    }

    function setSearchResult(resultObj){
        if (resultObj == undefined || resultObj == "")
            return;

        resultObj = resultObj;
        parseResultObj(resultObj);
        if (isFunction(window.superfishDataCallback))
            window.superfishDataCallback(resultObj);
    }

    function click(itemId){
        if (_items == null || _resultObj == null || _items == undefined || _items[itemId] == undefined)
            return;

        var item= _items[itemId];
        var clickUrl = _pluginDomain + "offerURL.action" + "?" +
            "rt=7&itemId=" + item.result.internalId +
            (_userId? "&userid=" + _userId: "" ) +
            "&sessionid=" + _resultObj.sessionId +
            "&dlsource=" + _dlsource +
            "&merchantName=" + item.result.merchantName +
            "&price=" + item.result.price +
            "&identical=" + (item.isIdentical?"1":"0") +
            "&br=" +  _browser;
        window.open(clickUrl);
    }

    function parseResultObj(resultObj){
        if (resultObj == undefined || resultObj == "" || resultObj.products == undefined )
            return;

        _items = new Array();
        var productLength = resultObj.products.length;
        var isIdentical;
        var offersLength, offersIterator, offerArray;
        var itemObject;
        for (var productsIterator = 0; productsIterator < productLength; productsIterator++){
            isIdentical = resultObj.products[productsIterator].identical;
            offerArray = resultObj.products[productsIterator].offers;
            offersLength = offerArray.length;
            for (offersIterator = 0; offersIterator < offersLength; offersIterator++){
                if (_items[offerArray[offersIterator].internalId] != undefined)
                    continue;
                itemObject = new Object();
                itemObject.isIdentical = isIdentical;
                itemObject.result = offerArray[offersIterator];
                _items[itemObject.result.internalId] = itemObject;
            }
        }
    }

    function isFunction(functionObj){
        return (functionObj && Object.prototype.toString.call(functionObj) === '[object Function]');
    }

    return {
      init: init,
      setSearchResult: setSearchResult,
      click: click
    };
}();


;
}

}());
