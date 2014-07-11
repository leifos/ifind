function showThrobber() {
         document.getElementById('progress').style.visibility='visible';
         setTimeout("document.getElementById('progress').style.visibility='hidden'", 5000);
    }