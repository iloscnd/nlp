import random
import math


def sequence_generator(n, p1, p2, p_fake):
    fake = False

    observations = []
    states = [False]

    for _ in range(n):
        if not fake:
            if random.random() < p1:
                fake = True
        else:
            if random.random() < p2:
                fake = False

        states.append(fake)
        if not fake:
            observations.append(random.randint(1,6))
        else:
            if random.random() < p_fake:
                observations.append(6)
            else:
                observations.append(random.randint(1,5))
    return observations, states


def heuristic_predictor(observations, p1, p2, p_fake):

    expected_state_length = min(int(1/p1), int(1/p2), 2*int(1/p_fake) + 2)

    ##look at future of expected 
    states = [False]
    for i,obs in enumerate(observations):
        count = 0
        for k in range(i, min(i+expected_state_length, len(observations))):
            if observations[k] == 6:
                count += 1
        if count/expected_state_length > 1/12 + p_fake/2 and obs == 6:
            states.append(True)
        elif count/expected_state_length < 1/12 + p_fake/2 and obs != 6:
            states.append(False)
        else:
            states.append(states[-1])

    return states



def hmm_predictor(observations, p1, p2, p_fake):
    #alpha_i (t) = prawdopodobienstwo iteracji
    alpha = [ (1, 0) ]

    fake_dist = [ (1-p_fake)/5 for _ in range(5)]
    fake_dist.append(p_fake)

    for obs in observations:
        obs_if_true = alpha[-1][0] * 1/6 * (1-p1) + alpha[-1][1] * fake_dist[obs-1] * p2
        obs_if_false = alpha[-1][0] * 1/6 * p1 + alpha[-1][1] * fake_dist[obs-1] * (1-p2)
        alpha.append((obs_if_true, obs_if_false))
        

    beta = [(1,1)]

    for obs in reversed(observations):
        tail_if_true = 1/6 * ( (1-p1)*beta[-1][0] + p2*beta[-1][1] )
        tail_if_fals = fake_dist[obs-1] * ( p1*beta[-1][0] + (1-p2)*beta[-1][1] )
        beta.append((tail_if_true, tail_if_fals))

    states = []
    for i, b in enumerate(reversed(beta)):
        p_true = alpha[i][0] * b[0]
        p_false = alpha[i][1] * b[1]

        states.append(p_true < p_false)



    return states




def string_states(states):
    return "".join( ['1' if fake else '0' for fake in states] )


def main():
    p1 = 0.04
    p2 = 0.05
    
    p_fake = 0.5
    
    n = 100

    obs, states = sequence_generator(n, p1, p2, p_fake)
    states_predict_heur = heuristic_predictor(obs, p1, p2, p_fake)
    states_predict_hmm  = hmm_predictor(obs, p1, p2, p_fake)

    print(string_states(states))
    print(string_states(states_predict_heur))
    print(string_states(states_predict_hmm ))
    print("Heur Good prediction: {}/{}".format(sum([states[i] == states_predict_heur[i] for i in range(n)]), n))
    print("HMM Good prediction: {}/{}".format(sum([states[i] == states_predict_hmm[i] for i in range(n)]), n))


if __name__ == "__main__":
    main()