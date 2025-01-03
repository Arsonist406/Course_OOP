#pragma once
#include "card.h"
#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cstring> 
#include <algorithm>

using std::string;
using std::vector;
using std::unordered_map;

class __declspec(dllexport) CombinationSearcher {
private:
    vector<Card> playing_cards;
    unordered_map<std::string, int> values_order = {
            {"2", 2}, {"3", 3}, {"4", 4}, {"5", 5}, {"6", 6}, {"7", 7}, {"8", 8},
            {"9", 9}, {"10", 10}, {"jack", 11}, {"queen", 12}, {"king", 13}, {"ace", 14}
    };
    int comb_score = 0;
    bool has_ace = NULL;

public:
    CombinationSearcher(const vector<Card>& table, const vector<Card>& hand);

    int getCombScore() const;

    string execute();

protected:
    bool isThereAnAce();

    bool isRoyalFlush();

    bool isStraightFlush();

    bool isFourOfAKind();

    bool isFullHouse();

    bool isFlush();

    bool isStraight();

    bool isThreeOfAKind();

    bool isTwoPair();

    bool isPair();

    string highCard();

    // Функція для підрахунку кількості карт одного рангу в playing_cards
    void valueCounter(unordered_map<string, int>& value_count);

    // Функція для розділення карт в playing_cards по масті
    void divideBySuit(unordered_map<string, vector<int>>& suit_map);

};