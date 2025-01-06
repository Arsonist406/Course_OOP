#include "card.h"
#include "comb_search.h"

// Реалізація методів класу CombinationSearcher
CombinationSearcher::CombinationSearcher(const vector<Card>& table, const vector<Card>& hand) {
    playing_cards.reserve(table.size() + hand.size());
    playing_cards.insert(playing_cards.end(), table.begin(), table.end());
    playing_cards.insert(playing_cards.end(), hand.begin(), hand.end());
}

int CombinationSearcher::getCombScore() const {
    return comb_score;
}

string CombinationSearcher::execute() {
    has_ace = CombinationSearcher::isThereAnAce();

    if (CombinationSearcher::isRoyalFlush()) {
        return "Royal flush";
    }
    if (CombinationSearcher::isStraightFlush()) {
        return "Straight flush";
    }
    if (CombinationSearcher::isFourOfAKind()) {
        return "Four of a kind";
    }
    if (CombinationSearcher::isFullHouse()) {
        return "Full house";
    }
    if (CombinationSearcher::isFlush()) {
        return "Flush";
    }
    if (CombinationSearcher::isStraight()) {
        return "Straight";
    }
    if (CombinationSearcher::isThreeOfAKind()) {
        return "Three of a kind";
    }
    if (CombinationSearcher::isTwoPair()) {
        return "Two pair";
    }
    if (CombinationSearcher::isPair()) {
        return "Pair";
    }
    return CombinationSearcher::highCard();
}

bool CombinationSearcher::isThereAnAce() {
    for (const auto& card : playing_cards) {
        if (card.getValue() == "ace") {
            return true;
        }
    }
    return false;
}

bool CombinationSearcher::isRoyalFlush() {
    vector<int> royal_flush_values = { 10, 11, 12, 13, 14 };

    unordered_map<string, vector<int>> suit_map;
    divideBySuit(suit_map);

    // Перевірка, чи є 5 карт однієї масті
    for (const auto& pair : suit_map) {
        const vector<int>& values = pair.second;
        if (values.size() >= 5) {
            bool is_royal_flush = true;

            // Перевірка, чи є royal_flush_values підмножиною values
            for (const int& royal_value : royal_flush_values) {
                // std::find поверну values.end(), якщо не знайде royal_value в values
                if (std::find(values.begin(), values.end(), royal_value) == values.end()) {
                    is_royal_flush = false;
                    break;
                }
            }
            // Якщо всі royal_flush_values знайдені, це Royal Flush
            if (is_royal_flush) {
                return true;
            }
        }
    }
    // Якщо жодна масть не відповідає умовам
    return false;
}

bool CombinationSearcher::isStraightFlush() {
    unordered_map<string, vector<int>> suit_map;
    divideBySuit(suit_map);

    // Перевірка, чи є 5 карт однієї масті
    for (const auto& pair : suit_map) {
        const vector<int>& values = pair.second;
        if (values.size() >= 5) {
            vector<int> plc_values(values);

            if (has_ace) {
                plc_values.push_back(1);  // Якщо є туз, додає 1 для розрахунку можливої низької комбінації (ace, 2, 3, 4, 5)
            }

            std::sort(plc_values.begin(), plc_values.end());

            // Перевіряємо чи є послідовність п'яти карт
            for (size_t i = 0; i < plc_values.size() - 4; ++i) {
                if (plc_values[i] == plc_values[i + 1] - 1 && plc_values[i + 1] == plc_values[i + 2] - 1 && plc_values[i + 2] == plc_values[i + 3] - 1 && plc_values[i + 3] == plc_values[i + 4] - 1) {
                    comb_score = 0;
                    for (size_t j = i; j < i + 5; ++j) {
                        comb_score += plc_values[j];
                    }
                    return true;
                }
            }
        }
    }
    return false;
}

bool CombinationSearcher::isFourOfAKind() {
    unordered_map<string, int> value_count;
    valueCounter(value_count);

    // Перевірка, чи є 4 карти одного рангу
    for (const auto& pair : value_count) {
        const string& value = pair.first;
        int count = pair.second;

        if (count == 4) {
            comb_score = values_order[value] * 4;
            return true;
        }
    }
    return false;
}

bool CombinationSearcher::isFullHouse() {
    unordered_map<string, int> value_count;
    valueCounter(value_count);

    vector<int> counts;
    for (const auto& pair : value_count) {
        counts.push_back(pair.second);
    }

    std::sort(counts.begin(), counts.end());

    // Якщо 1 3 3 - знаходить, який з 3 має сильніший ранг і його множить на 3 під час розрахунку comb_score
    if (counts == vector<int>{1, 3, 3}) {
        vector<int> temp;
        for (const auto& pair : value_count) {
            if (pair.second == 3) {
                temp.push_back(values_order[pair.first]);
            }
        }

        std::sort(temp.begin(), temp.end());
        comb_score = temp[0] * 2 + temp[1] * 3;
        return true;
    }
    // Якщо 2 2 3 - знаходить, який з 2 має сильніший ранг і його множить на 2 під час розрахунку comb_score
    else if (counts == vector<int>{2, 2, 3}) {
        int three = 0;
        vector<int> temp;
        for (const auto& pair : value_count) {
            if (pair.second == 3) {
                three = values_order[pair.first];
            }
            else {
                temp.push_back(values_order[pair.first]);
            }
        }

        std::sort(temp.begin(), temp.end());
        comb_score = temp[1] * 2 + three * 3;
        return true;
    }
    // Якщо 1 1 2 3 - знаходить 2 і 3 і їх використовує під час розрахунку comb_score
    else if (counts == vector<int>{1, 1, 2, 3}) {
        int two_value = 0;
        int three_value = 0;

        for (const auto& pair : value_count) {
            if (pair.second == 3) {
                three_value = values_order[pair.first];
            }
            else if (pair.second == 2) {
                two_value = values_order[pair.first];
            }
        }

        comb_score = two_value * 2 + three_value * 3;
        return true;
    }
    return false;
}

bool CombinationSearcher::isFlush() {
    unordered_map<string, vector<int>> suit_map;
    divideBySuit(suit_map);

    // Перевірка, чи є 5 карт однієї масті
    for (const auto& pair : suit_map) {
        const vector<int>& values = pair.second;
        if (values.size() >= 5) {
            vector<int> temp(values);
            std::sort(temp.begin(), temp.end());

            // Підраховує comb_score для останнніх 5 елементів
            comb_score = 0;
            for (int i = 0; i < 5; ++i) {
                comb_score += temp[temp.size() - 1 - i];
            }
            return true;
        }
    }
    return false;
}

bool CombinationSearcher::isStraight() {
    // Записує в plc_values які ранги є в playing_cards
    vector<int> plc_values; // playing_cards_values
    for (const auto& card : playing_cards) {
        int card_value = values_order[card.getValue()];
        if (std::find(plc_values.begin(), plc_values.end(), card_value) == plc_values.end()) {
            plc_values.push_back(card_value);
        }
    }

    if (has_ace) {
        plc_values.push_back(1);  // Якщо є туз, додає 1 для розрахунку можливої низької комбінації (ace, 2, 3, 4, 5)
    }

    std::sort(plc_values.begin(), plc_values.end());

    // Перевірка, чи є послідовність п'яти карт
    bool comb_found = false;
    for (size_t i = 0; i < plc_values.size() - 4; ++i) {
        if (plc_values[i] == plc_values[i + 1] - 1 && plc_values[i + 1] == plc_values[i + 2] - 1 && plc_values[i + 2] == plc_values[i + 3] - 1 && plc_values[i + 3] == plc_values[i + 4] - 1) {
            comb_found = true;
            comb_score = 0;
            for (size_t j = i; j < i + 5; ++j) {
                comb_score += plc_values[j];
            }
        }
    }
    return comb_found;
}

bool CombinationSearcher::isThreeOfAKind() {
    unordered_map<string, int> value_count;
    valueCounter(value_count);

    // Перевірка, чи є три карти одного рангу
    for (const auto& pair : value_count) {
        if (pair.second == 3) {
            comb_score = values_order[pair.first] * 3;
            return true;
        }
    }
    return false;
}

bool CombinationSearcher::isTwoPair() {
    unordered_map<string, int> value_count;
    valueCounter(value_count);

    // Розрахунок кількості пар
    vector<string> pairs;
    for (const auto& pair : value_count) {
        if (pair.second == 2) {
            pairs.push_back(pair.first);
        }
    }

    // Перевірка на дві пари
    if (pairs.size() == 2) {
        comb_score = values_order[pairs[0]] * 2;
        comb_score += values_order[pairs[1]] * 2;
        return true;
    }
    // Якщо є три пари - знаходить дві з найзначущими рангами
    else if (pairs.size() == 3) {
        vector<int> temp = {
            values_order[pairs[0]], values_order[pairs[1]], values_order[pairs[2]]
        };
        std::sort(temp.begin(), temp.end(), std::greater<int>());
        comb_score = temp[0] * 2;
        comb_score += temp[1] * 2;
        return true;
    }
    return false;
}

bool CombinationSearcher::isPair() {
    unordered_map<string, int> value_count;
    valueCounter(value_count);

    // Перевірка, чи є пара в value_count
    for (const auto& pair : value_count) {
        if (pair.second == 2) {
            comb_score = values_order[pair.first] * 2;
            return true;
        }
    }
    return false;
}

string CombinationSearcher::highCard() {
    // Знаходить найзначущу карту
    int biggest_score = 0;
    for (const auto& card : playing_cards) {
        int score = values_order[card.getValue()];
        if (score > biggest_score) {
            biggest_score = score;
        }
    }

    comb_score = biggest_score;
    return "High";
}

// Функція для підрахунку кількості карт одного рангу в playing_cards
void CombinationSearcher::valueCounter(unordered_map<string, int>& value_count) {
    for (const auto& card : playing_cards) {
        value_count[card.getValue()] += 1;
    }
}

// Функція для розділення карт в playing_cards по масті
void CombinationSearcher::divideBySuit(unordered_map<string, vector<int>>& suit_map) {
    for (const auto& card : playing_cards) {
        suit_map[card.getSuit()].push_back(values_order[card.getValue()]);
    }
}
