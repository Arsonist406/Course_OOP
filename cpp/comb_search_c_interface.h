#pragma once
#include "comb_search.h" 

// ���������, �� ������� CtypesCard �� python
struct CtypesCard {
    const char* suit;
    const char* value;
};

// ��������� ��� �����䳿 � CombinationSearcher
extern "C" {
    __declspec(dllexport) CombinationSearcher* CombinationSearcher_create(const CtypesCard* table, int table_size, const CtypesCard* hand, int hand_size);

    __declspec(dllexport) void CombinationSearcher_destroy(CombinationSearcher* obj);

    __declspec(dllexport) const char* CombinationSearcher_execute(CombinationSearcher* obj);

    __declspec(dllexport) int CombinationSearcher_getCombScore(CombinationSearcher* obj);

    __declspec(dllexport) void free_string(const char* str);
}