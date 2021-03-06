from coconut.scheme import *
import time

def test_threshold_authority():
    q = 7 # number of attributes
    private_m = [10] * 2 # private attributes
    public_m = [3] * 1 # public attributes
    t, n = 8, 10 # threshold parameter and number of authorities
    params = setup(q)
    (d, gamma) = elgamal_keygen(params) # El-Gamal keypair

    # generate commitment and encryption
    Lambda = prepare_blind_sign(params, gamma, private_m, public_m=public_m)

    # generate key
    (sk, vk) = ttp_keygen(params, t, n)

    # aggregate verification keys
    vk[6] = None
    aggr_vk = agg_key(params, vk)

    # bind sign
    sigs_tilde = [blind_sign(params, ski, gamma, Lambda, public_m=public_m) for ski in sk]

    # unblind
    sigs = [unblind(params, sigma_tilde, d) for sigma_tilde in sigs_tilde]

    # aggregate credentials
    sigs[0] = sigs[5] = None
    sigma = agg_cred(params, sigs)

    # randomize credentials and generate any cryptographic material to verify them
    Theta = prove_cred(params, aggr_vk, sigma, private_m)

    # verify credentials
    begin = time.time()
    if verify_cred(params, aggr_vk, Theta, public_m=public_m):
        print("Success")
    end = time.time()
    print(end-begin)


'''def test_multi_authority():
    q = 7 # number of attributes
    private_m = [10] * 2 # private attributes
    public_m = [3] * 1 # public attributes
    n = 3 # number of authorities
    params = setup(q)
    (d, gamma) = elgamal_keygen(params) # El-Gamal keypair

    # generate commitment and encryption
    Lambda = prepare_blind_sign(params, gamma, private_m, public_m=public_m)

    # generate key
    keys = [keygen(params) for _ in range(n)]
    (sk, vk) = zip(*keys)

    # aggregate verification keys
    aggr_vk = agg_key(params, vk, threshold=False)

    # bind sign
    sigs_tilde = [blind_sign(params, ski, gamma, Lambda, public_m=public_m) for ski in sk]

    # unblind
    sigs = [unblind(params, sigma_tilde, d) for sigma_tilde in sigs_tilde]

    # aggregate credentials
    sigma = agg_cred(params, sigs, threshold=False)

    # randomize credentials and generate any cryptographic material to verify them
    Theta = prove_cred(params, aggr_vk, sigma, private_m)

    # verify credentials
    assert verify_cred(params, aggr_vk, Theta, public_m=public_m)
    '''


test_threshold_authority()