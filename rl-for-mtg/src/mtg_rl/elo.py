
def update_elo(r1, r2, score1, K=32):
    e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
    r1_new = r1 + K * (score1 - e1)
    r2_new = r2 + K * ((1 - score1) - (1 - e1))
    return r1_new, r2_new
