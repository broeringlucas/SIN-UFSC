#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>
#include <unordered_map>

// Definindo a classe do autômato finito determinístico
class Dfa
{
private:
    // Definição dos atributos do autômato finito determinístico
    std::vector<std::string> states;
    std::vector<std::string> alphabet;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> transaction_function;
    std::string start_state;
    std::vector<std::string> accept_states;

    // Método para verificar se o input é válido
    bool checkInput(const std::string &input)
    {
        for (int i = 0; i < input.length(); i++)
        {
            std::string symbol(1, input[i]);
            bool valid_symbol = false;

            for (int i = 0; i < alphabet.size(); i++)
            {
                if (symbol == alphabet[i])
                {
                    valid_symbol = true;
                    break;
                }
            }

            if (!valid_symbol)
            {
                return false;
            }
        }

        return true;
    }

    // Método para exbir mensagem de erro caso o input contenha símbolos inválidos
    void displayAlphabetErrorMessage()
    {
        printf("\nInvalid input!!\n");
        printf("Input symbols should be from the following alphabet:\n");
        printf("- ");
        for (int i = 0; i < alphabet.size(); i++)
        {
            printf("%s ", alphabet[i].c_str());
        }
        printf("\n\n");
    }

public:
    // Construtor da classe
    Dfa(std::vector<std::string> states,
        std::vector<std::string> alphabet,
        std::unordered_map<std::string,
                           std::unordered_map<std::string, std::string>>
            transaction_function,
        std::string start_state, std::vector<std::string> accept_states)
    {
        this->states = states;
        this->alphabet = alphabet;
        this->transaction_function = transaction_function;
        this->start_state = start_state;
        this->accept_states = accept_states;
    }

    // Método para verificar se o autômato aceita a string de entrada
    void isAccept(std::string input)
    {
        std::string current_state = start_state;

        // Verifica se a string de input é válida
        bool valid_input = checkInput(input);

        // Caso a string de input seja válida, o autômato é percorrido, caso contrário, uma mensagem de erro é exibida
        if (valid_input)
        {
            // Esse for pega cada símbolo do input e vai "percorrendo" os estados do autômato
            for (int i = 0; i < input.length(); i++)
            {
                std::string symbol(1, input[i]);

                // Atualiza o estado atual do autômato
                current_state = transaction_function[current_state][symbol];

                printf("\n%s -> %s", symbol.c_str(), current_state.c_str());
            }

            // Verifica se o estado atual é um estado de aceitação
            for (int i = 0; i < accept_states.size(); i++)
            {
                if (current_state == accept_states[i])
                {
                    printf("\n\nAccepted\n");
                }
                else
                {
                    printf("\n\nRejected\n");
                }
            }
        }
        else
        {
            displayAlphabetErrorMessage();
        }
    }

    // Funcão para exibir o autômato
    void displayDfa()
    {
        printf("----- States -----\n");
        printf("-");
        for (int i = 0; i < states.size(); i++)
        {
            printf(" %s ", states[i].c_str());
        }
        printf("\n");

        printf("\n----- Alphabet -----\n");
        printf("-");
        for (int i = 0; i < alphabet.size(); i++)
        {
            printf(" %s ", alphabet[i].c_str());
        }
        printf("\n");

        printf("\n----- Transition Function -----\n");
        for (int i = 0; i < states.size(); i++)
        {
            for (int j = 0; j < alphabet.size(); j++)
            {
                printf(" %s -> %s -> %s\n", states[i].c_str(), alphabet[j].c_str(), transaction_function[states[i]][alphabet[j]].c_str());
            }
            printf("\n");
        }

        printf("----- Start State -----\n");
        printf("- %s\n\n", start_state.c_str());

        printf("----- Accept States -----\n");
        printf("-");
        for (int i = 0; i < accept_states.size(); i++)
        {
            printf(" %s", accept_states[i].c_str());
        }
        printf("\n");

        printf("\n--------------------------\n");
    }
};
