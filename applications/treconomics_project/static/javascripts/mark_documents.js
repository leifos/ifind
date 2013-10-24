(function(docid){$.get("/trecdo/saved/"+docid+"&judge=1", function(data){ alert(data); }); });



function markAsRelevant(docid) {
    console.log("Marking document for" + docid);
    $.ajax({type: "GET",
            url: "/trecdo/saved/?doc="+docid+"&judge=1",
            dataType: "json",
            timeout: 5000,
            success: function(){
                $('p.marked'').replaceWith('<p id="marked">Relevant</p>');                
            },
    });
    return false; // prevent page reloading
  }