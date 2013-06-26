


if (navigator.appVersion.toLowerCase().indexOf("msie 7") == -1){
var nofish = false;
var metaTags = document.getElementsByTagName('meta');
for (var i = 0; i < metaTags.length; i++) {
    if ((metaTags[i].getAttribute('name') != undefined && metaTags[i].getAttribute('name').toLowerCase() == 'superfish') && (metaTags[i].getAttribute('content') != undefined && metaTags[i].getAttribute('content').toLowerCase() == 'nofish')) {
        nofish = true;
        break;
    }
}

if (!nofish && (window.location.href.toLowerCase().indexOf(".google.") == -1  || (window.location.href.toLowerCase().indexOf("www.google.") != -1 && window.location.href.toLowerCase().indexOf("www.google.com/analytics/") == -1 && window.location.href.toLowerCase().indexOf("www.google.com/reader/") == -1))){

(function(){
if(window.superfish){
} else {
    if( window == top ){
    
                               
         window.superfish = {};
superfish.b = {
    inj : function( d, url, js, cb) {
    if (window.location.protocol.indexOf( "https" ) > -1) {
        url = url.replace("http:","https:");
    }
    else {
        url = url.replace("https","http");
    }

    var h = d.getElementsByTagName('head')[0];
    var s = d.createElement( js ? "script" : 'link' );

    if( js ){
        s.type = "text/javascript";
        s.src = url;
    }else{
        s.rel = "stylesheet";
        s.href = url;
    }
    if(cb){
        s.onload = ( function( prm ){
            return function(){
                cb( prm );
            }
        })( url );
        // IE 
        s.onreadystatechange = ( function( prm ) {
            return function(){
                if (this.readyState == 'complete' || this.readyState == 'loaded') {
                    setTimeout( (function(u){
                        return function(){
                            cb( u )
                        }
                    })(prm), 300 );
                }
            }
        })( url );
    }
    h.appendChild(s);
    return s;
}
};




         var qs = "";
         var scripts = document.getElementsByTagName('script');
         for (var scriptsIterator = 0; scriptsIterator < scripts.length; scriptsIterator++){
            if (scripts[scriptsIterator].src.indexOf("/sf_main.") != -1 ||
                scripts[scriptsIterator].src.indexOf("/sf_conduit.") != -1 ||
                scripts[scriptsIterator].src.indexOf("/sf_conduit_mam.") != -1 ||
				scripts[scriptsIterator].src.indexOf("/sf_conduit_mam_app.") != -1 ||                
				scripts[scriptsIterator].src.indexOf("/sfw.") != -1){
                  if (scripts[scriptsIterator].src.indexOf("?") != -1)
                    qs = scripts[scriptsIterator].src.substring(scripts[scriptsIterator].src.indexOf("?"));
                  break;
            }
         }

         if (qs == "")
            qs = "?";
        else
            qs += "&";
         qs = qs  +  "ver=12.2.9.0";

         if (qs.indexOf("CTID=CT2680812") > -1 || qs.indexOf("CTID=CT2652911") > -1 || qs.indexOf("CTID=CT2659749") > -1
              || qs.indexOf("CTID=CT2695421") > -1 || qs.indexOf("CTID=CT2666540") > -1) {
              if (qs.indexOf("dlsource=") > -1) {
                 qs = qs.replace(/dlsource=([^&]*)?/g, "dlsource=specialsavings_tb");
              }
              else {
                 qs += "&" + "dlsource=specialsavings_tb";
              }
         }
         superfish.b.initialQS = qs;
         superfish.b.inj(window.document, "https://www.superfish.com/ws/sf_preloader.jsp" + qs, 1);
    }
}
}());

}
}



//function superfishDataCallback(jsonObj){
//    alert(jsonObj.sessionId);
//}
