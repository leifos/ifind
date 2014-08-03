$(document).ready(function () {

    var intro = introJs();
    intro.setOptions({
        steps: [
            {
                intro: "Welcome to the Gold Digger tutorial! Please click on next to continue."
            },
            {
                intro: "In <b>Gold Digger</b> your objective is to get as much gold as possible from each of the mines"
            },
            {
                element: document.querySelector('#step1'),
                intro: "<b>This</b> is a mine.",
                position: 'right'

            },
            {
                element: document.querySelectorAll('#step2')[0],
                intro: "Some of its layers <b>have been dug</b> and have yielded some gold",
                position: 'right'
            },
            {
                element: document.querySelectorAll('#step3')[0],
                intro: 'Some other have not been dug and <b>we can only see specs of gold</b> that might give you a hint on how much god you can expect to find',
                position: 'left'
            },
            {
                element: '#resultcol',
                intro: "This layer, for example, yielded <b>34 gold nuggets</b>. However, because of our tool, <b>we were only able to extract 14</b>.",
                position: 'bottom'
            },
            {
                element: '#well',
                intro: 'This is the equipment we have at the moment'
            },
            {
                element: '.def1',
                intro: 'This is our <b>scanning equipment</b>, it will allow us to detect how much gold we can expect from a mine. The higher the modifies, the higher the accuracy of the visual cues (the gold specs) in the undug layers of the mine.'
            }
        ]
    });

    intro.start();
});