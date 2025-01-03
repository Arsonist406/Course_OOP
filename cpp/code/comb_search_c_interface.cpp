#include "comb_search_c_interface.h" 

// ��������� ��� �����䳿 � CombinationSearcher
extern "C" {
    __declspec(dllexport) CombinationSearcher* CombinationSearcher_create(const CtypesCard* table, int table_size, const CtypesCard* hand, int hand_size) {
        // ������������ CtypesCard -> Card ��� table
        std::vector<Card> table_vec;
        for (int i = 0; i < table_size; ++i) {
            table_vec.emplace_back(std::string(table[i].suit), std::string(table[i].value)); // ������������ char* � std::string
        }

        // ������������ CtypesCard -> Card ��� hand
        std::vector<Card> hand_vec;
        for (int i = 0; i < hand_size; ++i) {
            hand_vec.emplace_back(std::string(hand[i].suit), std::string(hand[i].value)); // ������������ char* � std::string
        }

        return new CombinationSearcher(table_vec, hand_vec);
    }

    __declspec(dllexport) void CombinationSearcher_destroy(CombinationSearcher* obj) {
        delete static_cast<CombinationSearcher*>(obj);
    }

    __declspec(dllexport) const char* CombinationSearcher_execute(CombinationSearcher* obj) {
        auto result = static_cast<CombinationSearcher*>(obj)->execute();
        // ��������� ���������� ����� ��� ���������� ����������
        char* c_result = new char[result.length() + 1];
        strcpy_s(c_result, result.length() + 1, result.c_str());
        return c_result;
    }

    __declspec(dllexport) int CombinationSearcher_getCombScore(CombinationSearcher* obj) {
        return static_cast<CombinationSearcher*>(obj)->getCombScore();
    }

    __declspec(dllexport) void free_string(const char* str) {
        delete[] str;
    }
}