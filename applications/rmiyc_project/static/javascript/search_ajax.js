var button_available=true;

$(function()
{
    initiate_game();
    var timeoutID;
    window.onbeforeunload = confirmExit;
    function confirmExit()
    {
        return 'Are you sure you want to quit the game?';
    }
    $(window).resize(function()
     {
        var search_div_width =$('#search-div').width();
        $('#query').width(search_div_width -20);
     });

    $(document).keypress(function(event)
    {
        if(event.ctrlKey && event.which == 13)
        {
            skip_button_click(event);
        }
        else if(event.which == 13)
        {
           search_button_click(event);
        }
    });

    $('#search-button').click(function(event)
    {
        search_button_click(event);
    });

    $('#skip-button').click(function(event)
    {
        skip_button_click(event);
    });
});

function search_success(data, textStatus, jqXHR)
{
    $('body').css({'cursor':'auto'});
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.location ="/rmiyc/game_over";
        window.onbeforeunload= null;
        return false;
    }
    var obj_list = jQuery.parseJSON(obj.results);
    var html_string = "";
    $(obj_list).each(function()
        {
            if (this.link != obj.url_to_find)
            {
                html_string+= "<Li><strong>" + this.title + "</strong></Li>";
            }
            else
            {
                html_string+= "<Li class='text-warning'><strong>" + "Page was retrieved in this rank" + "</strong></Li>";
            }
        }
    );
    $('#search-results-ol').html(html_string);

    var game_updates_html =  "<tr><td><h4> current score :</h4></td><td><h4>"+ obj.current_score +"</h4></td></tr>"+
                             "<tr><td><h4> round no :</h4></td><td><h4>"+ obj.no_round +"</h4></td></tr>" +
                             "<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
                             "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" +obj.no_of_queries_issued_for_current_page+ "</h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    $('#score-div').html("<Strong>score :" + obj.score + "</strong>");
    $('#avatar-div').html("<h3>" + obj.avatar + "</h3>")
    if(obj.score != 0)
    {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> take points");
        $('#skip-button').removeClass("btn-error").addClass("btn-success");
        $('#search-button').html('<i class="icon-search icon-white"></i> search again');
        $('#content-div').removeClass("alert-error").addClass("alert-success");
    }
    else
    {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
        $('#skip-button').removeClass("btn-success").addClass("btn-danger");
        $('#search-button').html('<i class="icon-search icon-white"></i> search');
        $('#content-div').removeClass("alert-success").addClass("alert-error");
    }
    adjust_body_divs_height();
    button_available=true;
    $('#search-button').removeAttr("disabled");
}

function display_next_page_success(data, textStatus, jqXHR)
{
    $('#query').val("");
    $('#query').focus();
    $('#content-div').removeClass("alert-success");
    $('#content-div').addClass("alert-error");
    $('#skip-button').removeClass("btn-success").addClass("btn-danger");
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.onbeforeunload= null;
        window.location ="/rmiyc/game_over";
        return false;
    }
    var game_updates_html =  "<tr><td><h4> current score :</h4></td><td><h4>"+ obj.current_score +"</h4></td></tr>"+
                             "<tr><td><h4> round no :</h4></td><td><h4>"+ obj.no_round +"</h4></td></tr>" +
                             "<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
                             "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" +obj.no_of_queries_issued_for_current_page+ "</h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    $('#search-results-ol').html("");
    $('#score-div').html("");
    $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
    $('#search-button').html('<i class="icon-search icon-white"></i> search');
    $('#image-box').hide();
    $('#image-div').html("<image src= '" + obj.screenshot + "' height='1000' width='1000'> </image>");
    adjust_body_divs_height();
}

function adjust_header_divs_height()
{
    var highestCol = Math.max($('#statistics-div').height(),$('#header-div').height());
    $('#statistics-div').height(highestCol);
    $('#header-div').height(highestCol);
}

function adjust_body_divs_height()
{
    var search_div_height =$('#search-div').height();
    var content_div_height = $('#content-div').height();
    var search_div_margin =$('#search-div').css("margin-bottom");
    var variable =search_div_height + content_div_height;
    var highestCol = Math.max($('#image-div').height(),variable);
    if (highestCol < 650)
    {
        highestCol=650;
    }
    $('#image-div').height(highestCol);
    $('#content-div').height(highestCol - search_div_height - 35);
}

function adjust_search_input_width()
{
    var search_div_width =$('#search-div').width();
    $('#query').width(search_div_width -20);
}

function avatar()
{
        $('#search-div').fadeTo(0,0);
        $('#content-div').fadeTo(0,0);
        $('#image-div').fadeTo(0,0);
        $('#avatar-div').html("<h3> Ready? </h3>")
        timeoutID = window.setTimeout(avatar1, 2000);
}

function avatar1()
{
        timeoutID = window.setTimeout(avatar1, 2000);
        $('#search-div').fadeTo(1500,1);
        $('#content-div').fadeTo(1500,1);
        $('#image-div').fadeTo(1500,1);
        $('#avatar-div').html("<h3> if you retrieve the page, you can have the points!  </h3>")
        window.clearTimeout(timeoutID);
}

function initiate_game()
{
         var game_updates_html =  "<tr><td><h4> score :</h4></td><td><h4> 0 </h4></td></tr>"+
                                  "<tr><td><h4> round no :</h4></td><td><h4> 1 </h4></td></tr>" +
                                  "<tr><td><h4> remaining rounds :</h4></td><td><h4> 3 </h4></td></tr>"+
                                  "<tr><td><h4> queries issued for this page :</h4></td><td><h4> 0 </h4></td></tr>";
         $('#game_updates-div').html(game_updates_html);
         avatar();
         adjust_header_divs_height();
         adjust_body_divs_height();
         adjust_search_input_width();
}

function search_button_click(event)
{
    var opts = {
      lines: 13, // The number of lines to draw
      length: 20, // The length of each line
      width: 10, // The line thickness
      radius: 20, // The radius of the inner circle
      corners: 1, // Corner roundness (0..1)
      rotate: 0, // The rotation offset
      direction: 1, // 1: clockwise, -1: counterclockwise
      color: '#000', // #rgb or #rrggbb
      speed: 1, // Rounds per second
      trail: 60, // Afterglow percentage
      shadow: false, // Whether to render a shadow
      hwaccel: false, // Whether to use hardware acceleration
      className: 'spinner', // The CSS class to assign to the spinner
      zIndex: 2e9, // The z-index (defaults to 2000000000)
      top: 'auto', // Top position relative to parent in px
        left: 'auto' // Left position relative to parent in px
    };
    var target = document.getElementById('score-div');
    var spinner = new Spinner(opts).spin(target);
    if(button_available==true)
    {
        event.preventDefault();
        button_available= false;
        $('#search-button').attr("disabled","disabled");
        $(this).css({'cursor':'wait'});
        $.ajax
        ({
            type: "GET",
            url: "/rmiyc/search/",
            data:
            {
                'query' : $('#query').val()
            },
            success: search_success,
            dataType: 'html'
        });
    }
}

function skip_button_click(event)
{
    event.preventDefault();
    $.ajax
    ({
        type: "GET",
        url: "/rmiyc/display_next_page/",
        success: display_next_page_success,
        dataType: 'html'
    });
}

/**
 * Created with PyCharm.
 * User: arazzouk
 * Date: 30/07/2013
 * Time: 18:04
 * To change this template use File | Settings | File Templates.
 */
//fgnass.github.com/spin.js#v1.3

/**
 * Copyright (c) 2011-2013 Felix Gnass
 * Licensed under the MIT license
 */
(function(root, factory) {

  /* CommonJS */
  if (typeof exports == 'object')  module.exports = factory()

  /* AMD module */
  else if (typeof define == 'function' && define.amd) define(factory)

  /* Browser global */
  else root.Spinner = factory()
}
(this, function() {
  "use strict";

  var prefixes = ['webkit', 'Moz', 'ms', 'O'] /* Vendor prefixes */
    , animations = {} /* Animation rules keyed by their name */
    , useCssAnimations /* Whether to use CSS animations or setTimeout */

  /**
   * Utility function to create elements. If no tag name is given,
   * a DIV is created. Optionally properties can be passed.
   */
  function createEl(tag, prop) {
    var el = document.createElement(tag || 'div')
      , n

    for(n in prop) el[n] = prop[n]
    return el
  }

  /**
   * Appends children and returns the parent.
   */
  function ins(parent /* child1, child2, ...*/) {
    for (var i=1, n=arguments.length; i<n; i++)
      parent.appendChild(arguments[i])

    return parent
  }

  /**
   * Insert a new stylesheet to hold the @keyframe or VML rules.
   */
  var sheet = (function() {
    var el = createEl('style', {type : 'text/css'})
    ins(document.getElementsByTagName('head')[0], el)
    return el.sheet || el.styleSheet
  }())

  /**
   * Creates an opacity keyframe animation rule and returns its name.
   * Since most mobile Webkits have timing issues with animation-delay,
   * we create separate rules for each line/segment.
   */
  function addAnimation(alpha, trail, i, lines) {
    var name = ['opacity', trail, ~~(alpha*100), i, lines].join('-')
      , start = 0.01 + i/lines * 100
      , z = Math.max(1 - (1-alpha) / trail * (100-start), alpha)
      , prefix = useCssAnimations.substring(0, useCssAnimations.indexOf('Animation')).toLowerCase()
      , pre = prefix && '-' + prefix + '-' || ''

    if (!animations[name]) {
      sheet.insertRule(
        '@' + pre + 'keyframes ' + name + '{' +
        '0%{opacity:' + z + '}' +
        start + '%{opacity:' + alpha + '}' +
        (start+0.01) + '%{opacity:1}' +
        (start+trail) % 100 + '%{opacity:' + alpha + '}' +
        '100%{opacity:' + z + '}' +
        '}', sheet.cssRules.length)

      animations[name] = 1
    }

    return name
  }

  /**
   * Tries various vendor prefixes and returns the first supported property.
   */
  function vendor(el, prop) {
    var s = el.style
      , pp
      , i

    if(s[prop] !== undefined) return prop
    prop = prop.charAt(0).toUpperCase() + prop.slice(1)
    for(i=0; i<prefixes.length; i++) {
      pp = prefixes[i]+prop
      if(s[pp] !== undefined) return pp
    }
  }

  /**
   * Sets multiple style properties at once.
   */
  function css(el, prop) {
    for (var n in prop)
      el.style[vendor(el, n)||n] = prop[n]

    return el
  }

  /**
   * Fills in default values.
   */
  function merge(obj) {
    for (var i=1; i < arguments.length; i++) {
      var def = arguments[i]
      for (var n in def)
        if (obj[n] === undefined) obj[n] = def[n]
    }
    return obj
  }

  /**
   * Returns the absolute page-offset of the given element.
   */
  function pos(el) {
    var o = { x:el.offsetLeft, y:el.offsetTop }
    while((el = el.offsetParent))
      o.x+=el.offsetLeft, o.y+=el.offsetTop

    return o
  }

  // Built-in defaults

  var defaults = {
    lines: 12,            // The number of lines to draw
    length: 7,            // The length of each line
    width: 5,             // The line thickness
    radius: 10,           // The radius of the inner circle
    rotate: 0,            // Rotation offset
    corners: 1,           // Roundness (0..1)
    color: '#000',        // #rgb or #rrggbb
    direction: 1,         // 1: clockwise, -1: counterclockwise
    speed: 1,             // Rounds per second
    trail: 100,           // Afterglow percentage
    opacity: 1/4,         // Opacity of the lines
    fps: 20,              // Frames per second when using setTimeout()
    zIndex: 2e9,          // Use a high z-index by default
    className: 'spinner', // CSS class to assign to the element
    top: 'auto',          // center vertically
    left: 'auto',         // center horizontally
    position: 'relative'  // element position
  }

  /** The constructor */
  function Spinner(o) {
    if (typeof this == 'undefined') return new Spinner(o)
    this.opts = merge(o || {}, Spinner.defaults, defaults)
  }

  // Global defaults that override the built-ins:
  Spinner.defaults = {}

  merge(Spinner.prototype, {

    /**
     * Adds the spinner to the given target element. If this instance is already
     * spinning, it is automatically removed from its previous target b calling
     * stop() internally.
     */
    spin: function(target) {
      this.stop()

      var self = this
        , o = self.opts
        , el = self.el = css(createEl(0, {className: o.className}), {position: o.position, width: 0, zIndex: o.zIndex})
        , mid = o.radius+o.length+o.width
        , ep // element position
        , tp // target position

      if (target) {
        target.insertBefore(el, target.firstChild||null)
        tp = pos(target)
        ep = pos(el)
        css(el, {
          left: (o.left == 'auto' ? tp.x-ep.x + (target.offsetWidth >> 1) : parseInt(o.left, 10) + mid) + 'px',
          top: (o.top == 'auto' ? tp.y-ep.y + (target.offsetHeight >> 1) : parseInt(o.top, 10) + mid)  + 'px'
        })
      }

      el.setAttribute('role', 'progressbar')
      self.lines(el, self.opts)

      if (!useCssAnimations) {
        // No CSS animation support, use setTimeout() instead
        var i = 0
          , start = (o.lines - 1) * (1 - o.direction) / 2
          , alpha
          , fps = o.fps
          , f = fps/o.speed
          , ostep = (1-o.opacity) / (f*o.trail / 100)
          , astep = f/o.lines

        ;(function anim() {
          i++;
          for (var j = 0; j < o.lines; j++) {
            alpha = Math.max(1 - (i + (o.lines - j) * astep) % f * ostep, o.opacity)

            self.opacity(el, j * o.direction + start, alpha, o)
          }
          self.timeout = self.el && setTimeout(anim, ~~(1000/fps))
        })()
      }
      return self
    },

    /**
     * Stops and removes the Spinner.
     */
    stop: function() {
      var el = this.el
      if (el) {
        clearTimeout(this.timeout)
        if (el.parentNode) el.parentNode.removeChild(el)
        this.el = undefined
      }
      return this
    },

    /**
     * Internal method that draws the individual lines. Will be overwritten
     * in VML fallback mode below.
     */
    lines: function(el, o) {
      var i = 0
        , start = (o.lines - 1) * (1 - o.direction) / 2
        , seg

      function fill(color, shadow) {
        return css(createEl(), {
          position: 'absolute',
          width: (o.length+o.width) + 'px',
          height: o.width + 'px',
          background: color,
          boxShadow: shadow,
          transformOrigin: 'left',
          transform: 'rotate(' + ~~(360/o.lines*i+o.rotate) + 'deg) translate(' + o.radius+'px' +',0)',
          borderRadius: (o.corners * o.width>>1) + 'px'
        })
      }

      for (; i < o.lines; i++) {
        seg = css(createEl(), {
          position: 'absolute',
          top: 1+~(o.width/2) + 'px',
          transform: o.hwaccel ? 'translate3d(0,0,0)' : '',
          opacity: o.opacity,
          animation: useCssAnimations && addAnimation(o.opacity, o.trail, start + i * o.direction, o.lines) + ' ' + 1/o.speed + 's linear infinite'
        })

        if (o.shadow) ins(seg, css(fill('#000', '0 0 4px ' + '#000'), {top: 2+'px'}))

        ins(el, ins(seg, fill(o.color, '0 0 1px rgba(0,0,0,.1)')))
      }
      return el
    },

    /**
     * Internal method that adjusts the opacity of a single line.
     * Will be overwritten in VML fallback mode below.
     */
    opacity: function(el, i, val) {
      if (i < el.childNodes.length) el.childNodes[i].style.opacity = val
    }

  })


  function initVML() {

    /* Utility function to create a VML tag */
    function vml(tag, attr) {
      return createEl('<' + tag + ' xmlns="urn:schemas-microsoft.com:vml" class="spin-vml">', attr)
    }

    // No CSS transforms but VML support, add a CSS rule for VML elements:
    sheet.addRule('.spin-vml', 'behavior:url(#default#VML)')

    Spinner.prototype.lines = function(el, o) {
      var r = o.length+o.width
        , s = 2*r

      function grp() {
        return css(
          vml('group', {
            coordsize: s + ' ' + s,
            coordorigin: -r + ' ' + -r
          }),
          { width: s, height: s }
        )
      }

      var margin = -(o.width+o.length)*2 + 'px'
        , g = css(grp(), {position: 'absolute', top: margin, left: margin})
        , i

      function seg(i, dx, filter) {
        ins(g,
          ins(css(grp(), {rotation: 360 / o.lines * i + 'deg', left: ~~dx}),
            ins(css(vml('roundrect', {arcsize: o.corners}), {
                width: r,
                height: o.width,
                left: o.radius,
                top: -o.width>>1,
                filter: filter
              }),
              vml('fill', {color: o.color, opacity: o.opacity}),
              vml('stroke', {opacity: 0}) // transparent stroke to fix color bleeding upon opacity change
            )
          )
        )
      }

      if (o.shadow)
        for (i = 1; i <= o.lines; i++)
          seg(i, -2, 'progid:DXImageTransform.Microsoft.Blur(pixelradius=2,makeshadow=1,shadowopacity=.3)')

      for (i = 1; i <= o.lines; i++) seg(i)
      return ins(el, g)
    }

    Spinner.prototype.opacity = function(el, i, val, o) {
      var c = el.firstChild
      o = o.shadow && o.lines || 0
      if (c && i+o < c.childNodes.length) {
        c = c.childNodes[i+o]; c = c && c.firstChild; c = c && c.firstChild
        if (c) c.opacity = val
      }
    }
  }

  var probe = css(createEl('group'), {behavior: 'url(#default#VML)'})

  if (!vendor(probe, 'transform') && probe.adj) initVML()
  else useCssAnimations = vendor(probe, 'animation')

  return Spinner

}));