#pragma once
#include <string>

using std::string;

class __declspec(dllexport) Card {
public:
    string suit;
    string value;

    Card(const string& suit, const string& value);

    string getSuit() const;

    string getValue() const;

    void setSuit(string new_suit);

    void setValue(string new_value);
};