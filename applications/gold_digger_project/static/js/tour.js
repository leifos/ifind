console.log("Tour");
var tour = new Tour({
  steps: [
  {
    element: ".provatour",
    title: "Prova",
    content: "This is a test"
  }

]});

// Initialize the tour
tour.init();

// Start the tour
tour.start();
