/* function to display how to play information */

text = ["The main aim of the game is to find a webpage, for which an image is displayed on the left. Clicking on this image shows an enlarged screenshot of the page.",
    "You have 3 minutes to find as many pages as you can. Points are awarded for getting a page in the top 8 results. You can earn bonus points if you don't skip pages!",
    "Enter a word or phrase into the text box (highlighted in green)",
    "Then click either the 'Fetch' button to submit that query and rack up some points, or click 'throw' to skip that page (warning this will loose your non-skip bonus!",
    "Once the results from the three search engines have been collected by the game, they shall be displayed below the querying section of the page.",
    "The results are colour-coded, with red representing a URL that does not match the page URL, blue suggests that the link belongs to the same domain and does not exactly match, and green if the URL matches the desired URL."];
count = 0;




function goForward(){
    if (count <4)
    count += 2;
    changeText();
}

function goBack(){
    if (count > 0)
        count -= 2;
    changeText();
}


function changeText(){
    if (count == 0){
        document.getElementById('topText').innerHTML = text[0];
        document.getElementById('middleImage').height = "369";
        document.getElementById('middleImage').width = "522";
        document.getElementById('middleImage1').height = "0";
        document.getElementById('middleImage1').width = "0";

        document.getElementById('bottomText').innerHTML = text[1];
    }
    if (count == 2){
        document.getElementById('topText').innerHTML = text[2];
        document.getElementById('middleImage').height = "0";
        document.getElementById('middleImage').width = "0";
        document.getElementById('middleImage1').height = "369"
        document.getElementById('middleImage1').width = "522";
        document.getElementById('middleImage2').height = "0";
        document.getElementById('middleImage2').width = "0";
        document.getElementById('bottomText').innerHTML = text[3];
    }
    if (count == 4){
        document.getElementById('topText').innerHTML = text[4];
        document.getElementById('middleImage1').height = "0";
        document.getElementById('middleImage1').width = "0";
        document.getElementById('middleImage2').height = "369";
        document.getElementById('middleImage2').width = "522";
        document.getElementById('bottomText').innerHTML = text[5];
    }

}