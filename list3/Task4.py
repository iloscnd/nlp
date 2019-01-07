import random
import math
import sys

def string_states(states):
    return "".join( ['1' if fake else '0' for fake in states] )

def sequence_generator(n, a, b, pi):

    observations = []
    states = [random.random() > pi]

    for _ in range(n):

        observations.append( random.choices(range(6), b[states[-1]])[0] )
        states.append(random.random() > a[states[-1]][0])
    
    return observations, states


def hmm_predictor(observations, a, b, pi, states):
    ### a[i][j] = p-stwo przejscia z i do j
    ### b[i][o] = p-stwo wyemiotwania obs o w stanie i
    ## alpha_t (i) = P(o_1 ... o_t−1, X_t = i|model)
    ## beta_t (j) = P(o_t . . . o_T |X_t = i, model)
    ## dzeta_t (i, j) = P(q_t = i, q_t+1 = j|O, model)
    ## gamma_t (i) = P(q_t = i | O, model)
    ##
    ## dzeta_t (i, j) = (alpha_t(i) * a_ij * b_io_t+1 * beta_t+1 (j))/P(O|model)

    T = len(observations)

    alpha = [ [pi, 1-pi] ]
    c = []
    for obs in observations:
        c.append( sum([b[state][obs] * alpha[-1][state] for state in states] ) )    
        alpha.append([0,0])
        for state in states:
            alpha[-1][state] = sum([ alpha[-2][prev] * b[prev][obs] * a[prev][state] for prev in states] )/c[-1]

    beta = [[1,1]]
    for t, obs in zip( range(T-1, -1, -1), reversed(observations)):
        beta.append([0,0])
        for state in states:
            beta[-1][state] = sum( [b[state][obs] *  a[state][nxt] * beta[-2][nxt]  for nxt in states] ) /c[t]
    beta = beta[::-1]

    gamma = []
    for i, bt in enumerate(beta):
        p_true = alpha[i][0] * bt[0]
        p_false = alpha[i][1] * bt[1] 
        gamma.append([p_true , p_false])

    
    dzeta = []
    for i,obs in enumerate(observations):
        dzeta.append([])
        for s1 in states:
            dzeta[-1].append([])
            for s2 in states:
                dzeta[-1][-1].append( alpha[i][s1] * a[s1][s2] * b[s1][obs] * beta[i+1][s2] )
    #print(dzeta)
    #print(dzeta[0])

    states = []
    for gm in gamma:
        states.append(gm[0]<gm[1])

    return alpha, beta, gamma, dzeta, states


def remodel(alpha, beta, gamma, dzeta, observations, states, possible_obs):

    #print(gamma)
    pi = gamma[0][0]
    a = []
    for s1 in states:
        a.append([])
        m = sum([ dz[s1][s2] for s2 in states for dz in dzeta ])
        for s2 in states:
            a[-1].append( sum([ dz[s1][s2] for dz in dzeta ])/m )
    b = []
    for s in states:
        b.append([])
        m = sum([gm[s] for gm in gamma])
        for pobs in possible_obs:
            b[-1].append(0)
            for i,obs in enumerate(observations):
                if obs == pobs:
                    b[-1][-1] +=  gamma[i][s]
            b[-1][-1] /= m

    return a, b, pi



def init(states, possible_obs):
    #a = [[0.96, 0.04], [0.05,0.95]]
    a = []

    sigma = (1/len(states))**2

    for _ in states:
        rest = 1.
        a.append([])
        n_states = len(states)
    
        for _ in states:
            mod = random.normalvariate(0, sigma)
            chance = max(0, 1/n_states + mod)
            chance = min(chance, rest)
            rest -= chance
            a[-1].append(chance)
            
    b = []
    sigma = (1/len(possible_obs))**2
    for _ in states:
        rest = 1.
        b.append([])
        n_obs = len(possible_obs)
        for _ in possible_obs:
            mod = random.normalvariate(0, sigma)
            chance = max(0, 1/n_obs + mod)
            chance = min(chance, 1)
            rest -= chance
            b[-1].append(chance)

    
    pi = random.normalvariate(0.5, (1/len(states))**2 )


    return a, b, pi

def EM(observations, iters, states, possible_obs, debug=False):
    a, b, pi = init(states, possible_obs)
    if debug:
        print(a,b, pi, sep="\n")
    for _ in range(iters):
        alpha, beta, gamma, dzeta, prediction = hmm_predictor(observations, a, b, pi, states)
        a,b,pi = remodel(alpha, beta, gamma, dzeta, observations, states, possible_obs)

        if debug:
            #print(string_states(prediction))
            #print(dzeta)
            print(a)
            print(b)
            print(pi)



    return a, b, pi, prediction





def main():


    if len(sys.argv) < 2:
        n = 10000

        a = [[0.96, 0.04], [0.05,0.95]]
        b = [[1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
            [1/10, 1/10, 1/10, 1/10, 1/10, 1/2]]
        pi = 1

        states = [0,1]
        possible_obs = list(range(6))

        obs, true_states = sequence_generator(n, a, b, pi)
        
        a_pred, b_pred, pi_pred, states_predict = EM(obs, 1000, states, possible_obs, False)
        
        print(a_pred, b_pred, pi_pred, sep="\n")
        #print(string_states(states))
        #print(string_states(states_predict_hmm ))
        print("HMM Good prediction: {}/{}".format(sum([true_states[i] == states_predict[i] for i in range(n)]), n))

    else:
        states = [0,1]
        possible_obs = list(range(6))


        obs = []
        for line in open(sys.argv[1]):
            obs += [int(k) - 1 for k in line[:-1]]


        for i in range(1,5):
            print("Wyniki dla prefiksu długości ", min(10**i, len(obs) ))


            a_pred, b_pred, pi_pred, states_predict = EM(obs[:10**i], 1000, states, possible_obs, False)
            print("a")
            for state in a_pred:
                print(state)

            print("b")
            for state in b_pred:
                print(state)

            print("pi = ", pi_pred)


#            print(a_pred, b_pred, pi_pred, sep="\n")



##


if __name__ == "__main__":
    main()