// Para compilar g++ main.cpp -o main

#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <unordered_map>
#include "dfa.h"

int main()
{
    // Instanciando um autômato finito determinístico
    std::vector<std::string> states = {"0", "1", "2", "3"};
    std::vector<std::string> alphabet = {"a", "b"};
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> transaction_function;
    transaction_function["0"]["a"] = "1";
    transaction_function["0"]["b"] = "0";
    transaction_function["1"]["a"] = "1";
    transaction_function["1"]["b"] = "2";
    transaction_function["2"]["a"] = "1";
    transaction_function["2"]["b"] = "3";
    transaction_function["3"]["a"] = "1";
    transaction_function["3"]["b"] = "0";
    std::string start_state = "0";
    std::vector<std::string> accept_states = {"3"};

    Dfa dfa(states, alphabet, transaction_function, start_state, accept_states);

    std::string input;
    std::cout << "Enter the input string: ";
    std::cin >> input;

    // Se descomentar essa linha o autômato será exibido
    dfa.displayDfa();

    dfa.isAccept(input);

    return 0;
}