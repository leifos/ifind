console.log("trip started");
var trip2 = new Trip([
    {
        sel: $("#California_landscape"),
        content: 'Hello and welcome to the <b>Gold Digger tutorial!</b> You can click on next or use the arrow keys to go forward (and back)',
        position: "s"
//        animation: "fadeInDown"

    },
    {
        sel: $("#California_landscape"),
        content: 'In <b> Gold Digger </b> our objective is to <u>gather as much gold as possible</u>.',
        position: "s"

    },
    {
        sel: $("#step1"),
        content: "To to this we have to dig through <b>mines</b>, like this one.",
        position: "n",
        expose: true
    },
    {
        sel: $("#ten"),
        content: "Each mine has <b>ten layers</b>, each <u>yielding a certain amount of gold</u>",
        position: "n"
    },
    {
        sel: $("#step2"),
        content: "This layer of the mine <b>has been dug</b> yielding a certain amount of nuggets.",
        position: "n"
    },
    {
        sel: $("#step3"),
        content: "Whereas this layer has not been dug and <b>we can only see some gold flecks</b> that suggest us <u>how much gold we can expect to find in this particular layer.</u>",
        position: "n"

    },
    {
        sel: $("#step3"),
        content: "Depending on the <b>scanning equipment</b> we have, the gold flecks we can see,<u> will represent more or less accurately the <b>actual</b> amount of gold in a particular layer</u>.",
        position: "n"
    },
    {
        sel: $("#step3"),
        content: "Our scanning equipment also determines <u>how many layers of the mine will show us cues</u>.",
        position: "n"
    },
    {
        sel: $("#empty"),
        content: "For example, we don't know anything about this layer, since <u>our scanning equipment only allows us to see 5 layers down the mine</u>.",
        position: "n"
    },
    {
        sel: $("#step4"),
        content: "Here we can see how many gold nuggets we found in this particular layer. If we had a better tool <b>we probably would have extracted more</b>",
        position: "s"
    },

    {
        sel: $("#eq"),
        content: "This is the equipment we have at the moment",
        position: "n"

    },
    {
        sel: $("#equip"),
        content: "Our <b>Scanning Equipment</b> right now is the <b>Sonar</b>. With this object equipped, as our scanning equipment, we will have <b>an accuracy of 50%</b> in identifying gold specks.",
        position: "e"

    },
     {
        sel: $("#equip"),
        content: "Furthermore, the <b>scanning equipment</b> will only allow us to see up to a certain number of layers. In this case, <b>five</b>",
        position: "e"

    },
    {
        sel: $("#digbutton_1"),
        content: "If we click on the dig button and we still have enough units of time, well'be able to <b>dig through one more layer</b> of the mine",
        position: "e"

    },
    {
        sel: $("#tool"),
        content: "Our <b>Tool</b> at the moment is a 'Golden Shovel', it allows us to get <b>40%</b> of the gold in each layer of the mine.",
        position: "e"
    },
    {
        sel: $("#digbutton_1"),
        content: "Our tool also <b>modifies the cost of digging</b> on each layer of the mine, with a <b>'Golden Shovel'</b> the cost of digging is 5 units of time",
        position: "s"
    },
    {
        sel: $("#vehicle"),
        content: "This is our <b>Vehicle</b>, it allows us to move in between mines at a given cost",
        position: "e"
    },
    {
        sel: $("#controls"),
        content: "For example, the cost of moving with a truck is 5 units of time",
        position: "s"

    },
    {
        sel: $("#controls"),
        content: "Every time you move <b>you'll be presented with a new mine</b> with all its layer undug",
        position: "s"

    },
    {
        sel: $("#mineno"),
        content: "Today, for instance, we have moved through 5 different mines",
        position: "e"
    },
    {
        sel: $("#prog"),
        content: "Here we can see <b>how much time we have left</b> before the end of the day, in this case we have 60 units of time left. Still a lot of digging can be done!",
        position: "e"
    },
    {
        sel: $("#prog"),
        content: "When the day is over, we will be able to decide if to continue mining in the same mine for another day, or move to a new mine, in another location. There are mines in 6 different locations and each of them has a different cost to be dug into",
        position: "e"
    },
    {
        sel: $("#Cali"),
        content: "Right now, we are in <b>California</b>, the starting mine. This mine is the cheapest, but also the one that yields the least gold. There are other 5 to choose from: <b>Yukon, Brazil, Scotland, South Africa and Victoria</b> (Australia).",
        position: "e"
    },
    {
        sel: $("#tot"),
        content: "Here we can see <b>how much gold we have accumulated in total</b>. This Gold can be used to <b>access other mines</b> in the location selection screen or to <b>buy new equipment</b>. But be careful, if you spend all your gold, it's <b>Game Over!</b>",
        position: "s"
    },
    {
        sel: $("#currentgold"),
        content: "This is your <b>Current Gold</b> the gold you managed to harvest today. The more you get in a single mine, the more you'll rise through the leaderboards",
        position: "e"

    },
    {
        sel: $("#golddigger"),
        content: "If you want to <b>go back to the Home screen</b> you can click here.",
        position: "e"
    },
    {
        sel: $("#username"),
        content: "To access <b>your profile</B> you just need to click on your username",
        position: "s"
    },
    {
        sel: $("#logout"),
        content: "Finally, to <b>logout</b>, click here, but I guess that was pretty obvious, wasn't it?",
        position: "s"
    },
    {
        sel: $("#123"),
        content: "This is pretty much all you need to know about <b>Gold Digger</b> now click on 'Play!' if you're logged in, or go back to the main page to register and <b>start digging!</b>"
    }


], {
    tripTheme: "yeti",
    animation: "bounceInDown",
    showNavigation: true,
    showCloseBox: true,
    delay: -1

}); // details about options are listed below

$(document).ready(function () {
    trip2.start();
});
