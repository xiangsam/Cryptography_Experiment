import sys
sys.path.append('../..')
from MyCrypto.util.inverse_mod import inverse_mod
from MyCrypto.RSA.rsa import quick_Decrypt, decrypt
import math

def n2s(n):
    nbits = n.bit_length()
    nbytes = (nbits + 7) >> 3
    return n.to_bytes(nbytes, 'big').decode('utf-8')

def Transform(up, down):
    """
    use list to present continued fraction
    """
    lst = []
    while down:
        lst.append(up // down)
        up, down = down, up % down
    return lst

def Progressive_fraction(sub_lst):
    up, down = 1, 0
    for frac in sub_lst[::-1]:
        down, up = up, frac * up + down
    return down, up

def get_All_Pro(up, down):
    """
    get all Progressive_fraction
    """
    lst = Transform(up, down)
    for i in range(1, len(lst)):
        yield Progressive_fraction(lst[0:i])

def wienerAttack(e, N):
    for (d, k) in get_All_Pro(e, N):
        if k == 0 or (e*d-1)%k != 0:
            continue
        phi_N = (e*d-1)//k
        add_pq = N - phi_N + 1
        p, q = (add_pq+math.isqrt(add_pq**2-4*N))//2, (add_pq - math.isqrt(add_pq**2-4*N))//2
        if p * q == N:
            print("Attacked!!!")
            return d, p, q
    print('Fail to attack')
    exit(0)

if __name__ == '__main__':
    e = 284100478693161642327695712452505468891794410301906465434604643365855064101922252698327584524956955373553355814138784402605517536436009073372339264422522610010012877243630454889127160056358637599704871937659443985644871453345576728414422489075791739731547285138648307770775155312545928721094602949588237119345
    n = 468459887279781789188886188573017406548524570309663876064881031936564733341508945283407498306248145591559137207097347130203582813352382018491852922849186827279111555223982032271701972642438224730082216672110316142528108239708171781850491578433309964093293907697072741538649347894863899103340030347858867705231
    c = 225959163039382792063969156595642930940854956840991461420767658113591137387768433807406322866630268475859008972090971902714782079518283320987088621381668841235751177056166331645627735330598686808613971994535149999753995364795142186948367218065301138932337812401877312020570951171717817363438636481898904201215
    d, p, q = wienerAttack(e, n)
    #plain = decrypt(c, d, n)
    plain = quick_Decrypt(c, d, p ,q)
    print(n2s(plain))

