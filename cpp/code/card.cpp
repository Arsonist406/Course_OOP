#include "card.h"

// Реалізація методів класу Card
Card::Card(const string& suit, const string& value) : suit(suit), value(value) {}

string Card::getSuit() const {
    return suit;
}

string Card::getValue() const {
    return value;
}

void Card::setSuit(string new_suit) {
    suit = new_suit;
}

void Card::setValue(string new_value) {
    value = new_value;
}