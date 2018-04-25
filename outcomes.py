import random
import math
import sys

#at bat takes in hitter, pitcher, baserunners, and overall situation
def at_bat(h, p, l, on_base, sit):
    outcome = random.uniform(0, 1) #random number

    #hitting and pitching walk and strikeout ratios. .000001 added so log scores are never undefined for 0 values
    hbb = float(h[2]) + .000001
    hk = float(h[3]) + .000001
    pbb = float(p[3]) + .000001
    pk = float(p[2]) + .000001

    #regression equations borrowed from fangraphs blog
    bb = math.exp(1)**(.9427*math.log(float(hbb)) + .9254*math.log(float(pbb)) + 1.5268)
    k = math.exp(1)**(.906*math.log(float(hk)) + .8644*math.log(float(pk)) + 1.9975)
    babip = 1.0403*float(h[12]) + .9135*float(p[6]) - .2573

    #line drive, ground ball, fly ball all use Morey-Z formula to predict

    h_av = float(h[13])
    p_av = float(p[9])
    l_av = float(l[0])
    v3 = math.sqrt(l_av*(1-l_av))
    v2 = (p_av - l_av)/v3
    v1 = (h_av - l_av)/v3
    ld = (((v1+v2)/math.sqrt(2)) * v3) + l_av

    h_av = float(h[14])
    p_av = float(p[10])
    l_av = float(l[1])
    v3 = math.sqrt(l_av*(1-l_av))
    v2 = (p_av - l_av)/v3
    v1 = (h_av - l_av)/v3
    gb = (((v1+v2)/math.sqrt(2)) * v3) + l_av

    h_av = float(h[15])
    p_av = float(p[11])
    l_av = float(l[2])
    v3 = math.sqrt(l_av*(1-l_av))
    v2 = (p_av - l_av)/v3
    v1 = (h_av - l_av)/v3
    fb = (((v1+v2)/math.sqrt(2)) * v3) + l_av

    #Morey-Z formula gives negative value for pop-ups, so I used log5 formula here
    h_av = float(h[16])
    p_av = float(p[12])
    l_av = float(l[3])
    v2 = ((1 - h_av)*(1 - p_av))/(1 - l_av)
    v1 = (h_av * p_av)/l_av
    iffb = v1/(v1 + v2)

    #initialize runs
    runs = 0

    #if random number falls in walk range, perform logic syntax to advance baserunners
    if outcome <= bb:
        #print h[0] + " walked."
        if on_base[0] != "":
            if on_base[1] != "":
                if on_base[2] != "":
                    #print on_base[2][0] + " scored."
                    on_base[2] = on_base[1]
                    on_base[1] = on_base[0]
                    on_base[0] = h
                    runs = 1
                else:
                    on_base[2] = on_base[1]
                    on_base[1] = on_base[0]
                    on_base[0] = h
            else:
                on_base[1] = on_base[0]
                on_base[0] = h
        else:
            on_base[0] = h

        return [0, on_base, runs]

    #if random number falls in strikeout range, update outs
    elif outcome <= bb + k:
        #print h[0] + " struckout."
        return [-1, on_base, runs]

    #anything else is a batted ball
    else:
        outcome = random.uniform(0,1)#another random number for batted ball

        #if batted ball falls in babip range, hit
        if outcome <= babip:
            iso = random.uniform(0,1)*float(h[9]) #random number weighted by iso or power rating

            #hard iso cutoffs based on line of best fit for 2017-2018 data trends
            #runners updated based on speed
            if iso <= .101:
                #print h[0] + " hit a single."
                if on_base[2] != "":
                    #print on_base[2][0] + " scored."
                    runs += 1
                    if on_base[1] != "" and float(on_base[1][10]) >= 3.2:
                        runs +=1
                        on_base[2] = ""
                    else:
                        on_base[2] = on_base[1]
                elif on_base[1] != "":
                    on_base[1] = on_base[0]
                on_base[0] = h

            elif iso <= 0.132:
                #print h[0] + " hit a double."
                for b in range(2,-1,-1):
                    if on_base[b] != "" and (b == 2 or b == 1):
                        #print on_base[b][0] + " scored."
                        runs += 1
                        on_base[b] = ""
                    elif on_base[b] != "" and b == 0:
                        if float(on_base[b][10]) >= 3.7:
                            #print on_base[b][0] + " scored."
                            runs += 1
                            on_base[0] = ""
                        else:
                            on_base[2] = on_base[0]
                on_base[1] = h
            elif iso <= .135:
                #print h[0] + " hit a triple."
                for b in range(2,-1,-1):
                    if on_base[b] != "":
                        #print on_base[b][0] + " scored."
                        runs += 1
                        on_base[b] = ""
                on_base[2] = h
            else:
                #print h[0] + " homered."
                runs += 1
                for b in range(2,-1,-1):
                    if on_base[b] != "":
                        #print on_base[b][0] + " scored."
                        runs += 1
                        on_base[b] = ""
                #print h[0] + " scored."
            return [1, on_base, runs]

        #if not hit, out (errors seemed negligible)
        else:
            outcome = random.uniform(0,1)
            if outcome <= ld:
                #print h[0] + " lined out."
                i = outcome

            #groundballs with a runner on first are automatic double plays, couldn't find stats to help come up with a real percentage
            #again speed determines how other runners react i.e. scoring from third, advancing from second to third
            elif outcome <= ld + gb:
                if on_base[0] != "" and sit[1] < 2:
                    on_base[0] = ""
                    #print h[0] + " grounded into a double play."
                    if sit == 0:
                        if on_base[2] != "":
                            #print on_base[2][0] + " scored."
                            on_base[2] = ""
                        if on_base[1] != "" and float(on_base[1][10]) >= 4 and on_base[0] == "":
                            #print on_base[1][0] + " advanced to third."
                            on_base[2] = on_base[1]
                            on_base[1] = ""
                    return [-2, on_base, runs]
                else:
                    #print h[0] + " grounded out."
                    if sit < 2:
                        if on_base[2] != "":
                            #print on_base[2][0] + " scored."
                            on_base[2] = ""
                        if on_base[1] != "" and float(on_base[1][10]) >= 4 and on_base[0] == "":
                            #print on_base[1][0] + " advanced to third."
                            on_base[2] = on_base[1]
                            on_base[1] = ""
            else:
                outcome = random.uniform(0,1) #used random number again to determine if flyball is popout or actual flyout

                #no one moves on popouts
                if outcome <= iffb:
                    #print h[0] + " popped out."
                    i = outcome

                #some runners can tag and score if SPD allows it
                else:
                    #print h[0] + " flied out."
                    if on_base[2] != "" and float(on_base[2][10]) >= 3:
                        #print on_base[2][0] + " tagged up and scored from third."
                        runs += 1
                        on_base[2] = ""
            return [-1, on_base, runs]

def steal(runner, on_base, base):
    outcome = random.uniform(0,1)
    attempt = ((1/330.0) * float(runner[10])**2) + ((13/660.0) * float(runner[10]))
    steal = ((-.6061*(float(runner[10])**2)) + (16.06 * float(runner[10])))/100.0

    #trendlines for 2017-2018 steal data used to determine likelihood of steal and likelihood of successful steal
    if outcome <= attempt:
        outcome = random.uniform(0,1)
        if outcome <= steal:
            string = runner[0] + " stole "
            if base == 0:
                string += "2nd base."
                on_base[1] = on_base[0]
                on_base[0] = ""
            else:
                string += "third base."
                on_base[2] = on_base[1]
                on_base[1] = ""
            #print string
            return [0, on_base]
        else:
            #print runner[0] + " was caught stealing."
            on_base[base] = ""
            return [1, on_base]
    else:
        return [0, on_base]
