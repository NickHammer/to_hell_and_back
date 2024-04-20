let deck = [];
let player1Hand = [];
let player2Hand = [];
let cardSheet; // This will hold the spritesheet image
let cardsData = {}; // This will store card data extracted from XML

function setup() {
    createCanvas(800, 600);
}

function draw() {
    background(220);
    drawCard('Ace_of_Hearts', 50, 50); // Draw Ace of Hearts at position (50, 50)
}

function drawCard(cardName, posX, posY) {
    if (cardsData[cardName]) {
        let card = cardsData[cardName];
        image(cardSheet, posX, posY, card.width, card.height, card.x, card.y, card.width, card.height);
    }
}

function drawDeck() {
    fill(0, 100, 0); // Dark green for the deck
    rect(width - 120, height - 300, 100, 140); // Draw deck at fixed position
}

function drawHand(hand, y) {
    let x = 20; // Starting x position for cards
    for (let card of hand) {
        let cardName = card.rank + '_of_' + card.suit; // Ensure this matches the naming convention in the XML
        drawCard(cardName, x, y);
        x += 30; // Increment x position for next card
    }
}

function createDeck() {
    const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
    const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'];
    const newDeck = [];
    
    for (let suit of suits) {
        for (let rank of ranks) {
            newDeck.push({ rank, suit });
        }
    }
    return newDeck;
}

function shuffleDeck(deck) {
    for (let i = deck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]]; // ES6 array destructuring swap
    }
}

function dealCards(roundNumber) {
    let handSize = roundNumber;
    player1Hand = [];
    player2Hand = [];

    for (let i = 0; i < handSize; i++) {
        player1Hand.push(deck.pop());
        player2Hand.push(deck.pop());
    }
}

function preload() {
    cardSheet = loadImage('assets/playingCards.png'); // Load the spritesheet
    loadXML('assets/playingCards.xml', loadedXML, loadError); // Load the XML and process it
}

function loadedXML(xml) {
    let elements = xml.getElementsByTagName('SubTexture'); // Assuming XML structure used by TexturePacker or similar
    for (let i = 0; i < elements.length; i++) {
        let name = elements[i].getAttribute('name');
        let x = parseInt(elements[i].getAttribute('x'));
        let y = parseInt(elements[i].getAttribute('y'));
        let width = parseInt(elements[i].getAttribute('width'));
        let height = parseInt(elements[i].getAttribute('height'));
        cardsData[name] = { x, y, width, height };
    }
}

function loadError() {
    console.error('Error loading XML');
}

function mousePressed() {
    // Example of detecting a click within the first card of player1Hand
    if (player1Hand.length > 0) {
        let card = player1Hand[0];
        let cardData = cardsData[card.rank + '_of_' + card.suit];
        let x = 20, y = 100; // Assuming the first card's position
        if (mouseX > x && mouseX < x + cardData.width && mouseY > y && mouseY < y + cardData.height) {
            console.log('Clicked on:', card.rank, 'of', card.suit);
            // Add logic here to play the card or highlight it
        }
    }
}
