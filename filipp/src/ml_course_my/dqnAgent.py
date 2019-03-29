import numpy
import agent

import sys
sys.path.append("..")

#import libs.libs_dqn_python.dqn as libs_dqn
import libs.libs_dqn_python_cpu.dqn as libs_dqn

class DQNAgent(agent.Agent):
    #config súbor s nastaveniami pre neural network
    #epsilon_decay je rate, ako rýchlo klesá hodnota epsilonu počas učenia (aby sieť zo začiatku viac preskúmavala a rýchlejšie sa učila)
    def __init__(self, environment, network_config_filename, epsilon_training = 0.35, epsilon_testing = 0.35, epsilon_decay = 1.0):
        super().__init__(environment)

        #                     ---> a1
        # ---> Neural network ---> a2
        #                     ---> a3
        #                       an = akcie dostupné v hre
        # state_geometry = stavový vektor
        #                  nepoužívame stavy, lebo to je uniform (nerozsekané)

        state_geometry = libs_dqn.sGeometry()
        state_geometry.w = self.environment.get_width()
        state_geometry.h = self.environment.get_height()
        state_geometry.d = self.environment.get_depth()

        self.deep_q_network = libs_dqn.DQN(network_config_filename, state_geometry, self.environment.get_actions_count()) #meanwhile toto je cca. 38000 C++ riadkov kódu

        self.epsilon_training = epsilon_training
        self.epsilon_testing = epsilon_testing
        self.epsilon_decay = epsilon_decay

    def main(self):
        if self.isBestRunEnabled():
            epsilon = self.epsilon_testing
        else:
            epsilon = self.epsilon_training
            self.epsilon_training *= self.epsilon_decay #decay je usually okolo 0.99998 a tak

        #do NN teraz napcháme stav a vypýtame si od nej Q hodnoty pre všetky
        #akcie, ktoré môžeme vykonať = výstupy NN

        state = self.environment.get_observation() #literally obrázok or stuff (celé dáta, nespracuvávame to)

        #prerobiť observation na C++ vektor floatov (napr. farebné hodnoty pixelov na floaty v intervale <0, 1>)
        state_vector = libs_dqn.VectorFloat(self.environment.get_size())
        for i in range(0, state_vector.size()):
            state_vector[i] = state[i] #just some python<-->C++ hackery

        self.deep_q_network.compute_q_values(state_vector) #math heavy C++ operation
        qValues = self.deep_q_network.get_q_values() #výstup = Q hodnoty pre každú akciu v danom stave

        self.action = self.selectAction(qValues, epsilon)
        self.environment.do_action(self.action) #thats actually important xddd

        self.reward = self.environment.get_reward()

        #Q(S, a) <- R(S, a) + gamma * max(Q(S', a'))
        #Q hodnota stavu S pre akciu a
        #R = reward pre stav a akciu
        #
        #pri neural net sa nesmú pchať do nej stavy postupne (correlated)
        #solution: experience replay buffer (od konca a pomiešané S, R a a)

        #keď má environment nastavený terminal state flag na true; teda keď hra skončila
        #plnenie rôznych stavov do buffera siete
        #aby sieť vedela, kde je koniec hry
        if self.environment.is_done():
            #keď je koniec hry
            self.deep_q_network.add_final(state_vector, qValues, self.action, self.reward)
        else:
            #keď hra prebieha
            self.deep_q_network.add(state_vector, qValues, self.action, self.reward)

        #keď je buffer plný a sme v tréningovom móde
        if self.deep_q_network.is_full() and not self.isBestRunEnabled():
            self.deep_q_network.learn()

    #ukladanie a načítavanie dát, just in case sieť je natrénovaná dobre
    #a upratovačka vytiahne kábel od servera or something
    def save(self, file_name_prefix):
        self.deep_q_network.save(file_name_prefix)

    def load(self, file_name):
        self.deep_q_network.load_weights(file_name)

    #Neurónové siete:
    #fc = full connected
    #   navzájom prepojené neuróny
    #relu = "dióda" activation function
    #   if x < 0 return 0 else return x --> tak vyzerá akt. funkcia
    #leaky relu = viac real "dióda"
    #   if x < 0 return 0.01*x else return x
    #
    #relu je filtračná aktivačná funkcia basically; tiež sa ale učí, ale iba pre kladné čísla
    #ostatné (záporné) hodnoty vynuluje
    #
    #output = výstup siete
    #   network geometry sa vypočíta v tomto frameworku automaticky podľa
    #   toho, koľko akcií máme
    #
    #fc + relu filter sa berú ako jedna vrstva
    #
    #Shallow neural network (machine learning):
    # --> fc (3 neuróny) --> relu (jedno prepojenie(vstup)) --> output (celé poprepájané)
    #
    #Deep neural network (deep learning):
    # --> fc (256) --> relu --> fc (64) --> relu --> fc (2)
    #
    #Plytvanie výkonom:
    # relu --> relu --> output
    #
    #Nemá to zmysel:
    # 1000 vstupov (1000-rozmerný priestor) --> fc (256) (hľadáme 256 rovín v 1000-rozmernom priestore) --> fc (256)
    #   keď nájdeme 256 rovín, tak v ďalšej vrstve hľadáme to isté a náš program
    #   sa učí pomalšie a plytvá výkonom = zbytočne
    #
    #Example:
    #rozpoznávanie 1000x1000 čiernobieleho obrázka na 2 druhy ovocia
    #1000000 vstupov do jedného neurónu (1000x1000x1)
    #fc (2)
    #a 2 výstupy
    #
    # = crap, nemá to logiku + dataset by musel byť obrovský (v 10 mil. obrázkov, ...)
    #
    #Example 2:
    #rozpoznávanie X od O
    #1000x1000 obrázok ako vstup
    #1000x1000x2 obrázky ako výstup (maska, kde sú X/O)
    #10^6 * 2 * 10^6 = 2 000 000 000 000 kusov tréningových dát = crap
    #
    #obrázok rozsekáme na menšie 5x5 sekcie a urobíme 25x25 tabuľku
    #v nich čísla spočítame a izi menej dát
    #
    #na rozpoznávanie obrázkov je dnes najlepšia voľba konvolučná sieť
    #teda napíšeme v tomto frameworku do config súboru "conv"
