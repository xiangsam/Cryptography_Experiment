# -*- coding: utf-8 -*-
#!/bin/usr/python3

table = 'abcdefghijklmnopqrstuvwxyz'


def encrypt(p, k):
    list_c = []
    for e in p:
        if e.isalpha():
            t_index = table.index(e.lower())
            list_c.append(table[(t_index + k) % 26])
        else:
            list_c.append(e)
    c = ''.join(list_c)
    return c


def decrypt(c, k):
    list_p = []
    for e in c:
        if e.isalpha():
            t_index = table.index(e.lower())
            list_p.append(table[(t_index - k) % 26])
        else:
            list_p.append(e)
    p = ''.join(list_p)
    return p


if __name__ == '__main__':
    key = 11
    plain = "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort. It had a perfectly round door like a porthole, painted green, with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, provided with polished chairs, and lots and lots of pegs for hats and coats - the hobbit was fond of visitors. The tunnel wound on and on, going fairly but not quite straight into the side of the hill - The Hill, as all the people for many miles round called it - and many little round doors opened out of it, first on one side and then on another. No going upstairs for the hobbit: bedrooms, bathrooms, cellars, pantries (lots of these), wardrobes (he had whole rooms devoted to clothes), kitchens, dining-rooms, all were on the same floor, and indeed on the same passage. The best rooms were all on the left-hand side (going in), for these were the only ones to have windows, deep-set round windows looking over his garden and meadows beyond, sloping down to the river."
    cypher = 'ty l szwp ty esp rczfyo espcp wtgpo l szmmte. yze l yldej, otcej, hpe szwp, qtwwpo htes esp pyod zq hzcxd lyo ly zzkj dxpww, yzc jpe l ocj, mlcp, dlyoj szwp htes yzestyr ty te ez dte ozhy zy zc ez ple: te hld l szmmte-szwp, lyo esle xplyd nzxqzce. te slo l apcqpnewj czfyo ozzc wtvp l azceszwp, altyepo rcppy, htes l dstyj jpwwzh mcldd vyzm ty esp pilne xtoowp. esp ozzc zapypo zy ez l efmp-dslapo slww wtvp l efyypw: l gpcj nzxqzcelmwp efyypw hteszfe dxzvp, htes alypwwpo hlwwd, lyo qwzzcd etwpo lyo nlcapepo, aczgtopo htes azwtdspo nsltcd, lyo wzed lyo wzed zq aprd qzc sled lyo nzled - esp szmmte hld qzyo zq gtdtezcd. esp efyypw hzfyo zy lyo zy, rztyr qltcwj mfe yze bftep decltrse tyez esp dtop zq esp stww - esp stww, ld lww esp apzawp qzc xlyj xtwpd czfyo nlwwpo te - lyo xlyj wteewp czfyo ozzcd zapypo zfe zq te, qtcde zy zyp dtop lyo espy zy lyzespc. yz rztyr fadeltcd qzc esp szmmte: mpoczzxd, mlesczzxd, npwwlcd, alyectpd (wzed zq espdp), hlcoczmpd (sp slo hszwp czzxd opgzepo ez nwzespd), vtenspyd, otytyr-czzxd, lww hpcp zy esp dlxp qwzzc, lyo tyoppo zy esp dlxp alddlrp. esp mpde czzxd hpcp lww zy esp wpqe-slyo dtop (rztyr ty), qzc espdp hpcp esp zywj zypd ez slgp htyozhd, oppa-dpe czfyo htyozhd wzzvtyr zgpc std rlcopy lyo xplozhd mpjzyo, dwzatyr ozhy ez esp ctgpc.'
    print(encrypt(plain, key))
    print(decrypt(cypher, key))
