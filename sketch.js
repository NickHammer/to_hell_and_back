let deck = [];
let player1Hand = [];
let player2Hand = [];
let player1Score = 0;
let player2Score = 0;
let cardSheet; // Holds the spritesheet image
let cardsData = {}; // Stores card data extracted from XML
let roundNumber = 1; // Start at round 1
let gameCanvas, scoreCanvas;
let scoreWidth = 200;
let trumpCard;

function setup() {
    // Score Canvas
    scoreCanvas = createGraphics(scoreWidth, 600);
    scoreCanvas.position(0, 0); // Position it on the left
    updateScoreCanvas(); // Draw the initial score canvas content
    
    // Game Canvas
    gameCanvas = createCanvas(800, 600);
    gameCanvas.position(scoreWidth, 0); // Position it to the right of the score canvas

    loadCardAssets();
}

async function loadCardAssets() {
    cardSheet = loadImage('assets/playingCards.png'); // Load the spritesheet
    await loadAndParseXML(); // Load and parse the XML
    startRound(roundNumber); // Start round 1
}

async function loadAndParseXML() {
    try {
        const response = await fetch('assets/playingCards.xml'); // Ensure the path is correct
        const text = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(text, "text/xml");
        const subTextures = xmlDoc.getElementsByTagName('SubTexture');

        for (let i = 0; i < subTextures.length; i++) {
            const element = subTextures[i];
            const name = element.getAttribute('name').replace('.png', ''); // Normalize the name by removing '.png'
            const x = parseInt(element.getAttribute('x'), 10);
            const y = parseInt(element.getAttribute('y'), 10);
            const width = parseInt(element.getAttribute('width'), 10);
            const height = parseInt(element.getAttribute('height'), 10);
            cardsData[name] = { x, y, width, height };
        }
    } catch (err) {
        console.error("Error loading or parsing XML:", err);
    }
}

function draw() {
    background(255);

    // Handle game drawing
    if (trumpCard) { // Check if the trump card is set and draw it
        drawCard(trumpCard, width - 140, height / 2 - 95);
    }
    drawPlayerHands();

    // Draw the score canvas
    image(scoreCanvas, 0, 0, scoreWidth, height);
}

function drawPlayerHands() {
    // Player 1's hand at the bottom
    for (let i = 0; i < player1Hand.length; i++) {
        drawCard(player1Hand[i], (width / 2) - (player1Hand.length * 70 / 2) + i * 70, height - 200);
    }
    // Player 2's hand at the top
    for (let i = 0; i < player2Hand.length; i++) {
        drawCard(player2Hand[i], (width / 2) - (player2Hand.length * 70 / 2) + i * 70, 10);
    }
}

function drawCard(cardName, posX, posY) {
    if (cardsData[cardName]) {
        let card = cardsData[cardName];
        image(cardSheet, posX, posY, card.width, card.height, card.x, card.y, card.width, card.height);
    } else {
        console.error("Card data not found for:", cardName);
    }
}

function startRound(round) {
    createDeck(); // Create the deck
    shuffleDeck(); // Shuffle the deck
    dealCards(round); // Deal the correct number of cards for the round
}

function updateScoreCanvas() {
    scoreCanvas.background(240); // Light gray background for the score canvas
    scoreCanvas.fill(0); // Black text
    scoreCanvas.textSize(16);
    scoreCanvas.text("Round: " + roundNumber, 10, 20);
    scoreCanvas.text("Player 1 Score: " + player1Score, 10, 50);
    scoreCanvas.text("Player 2 Score: " + player2Score, 10, 80);
    // ... any other score information
}

function createDeck() {
    const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
    const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    deck = [];
    for (let suit of suits) {
        for (let rank of ranks) {
            let cardName = `card${suit.charAt(0) + suit.slice(1)}${rank}`; // Format card names as seen in XML
            deck.push(cardName);
        }
    }
    console.log("Deck created with " + deck.length + " cards");
}

function shuffleDeck() {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]]; // ES6 array destructuring swap
    }
    console.log("Deck shuffled");
}

function dealCards(numCards) {
    if (deck.length < numCards * 2 + 1) {
        console.error("Not enough cards in deck to deal");
        return;
    }
    player1Hand = [];
    player2Hand = [];
    for (let i = 0; i < numCards; i++) {
        player1Hand.push(deck.pop());
        player2Hand.push(deck.pop());
    }
    trumpCard = deck.pop(); // Set the trump card from the top of the deck
    console.log("Trump card:", trumpCard);
}