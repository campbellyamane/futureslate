import random
import math

#at bat takes in hitter, pitcher, baserunners, and overall situation
def at_bat(h, p, ob, sit):
    o = random.uniform(0, 1) #random number

    #hitting and pitching walk and strikeout ratios. .000001 added so log scores are never undefined for 0 values
    hbb = float(h[3]) + .000001
    hk = float(h[4]) + .000001
    pbb = float(p[3]) + .000001
    pk = float(p[2]) + .000001

    #regression equations borrowed from fangraphs blog
    bb = math.exp(1)**(.9427*math.log(float(hbb)) + .9254*math.log(float(pbb)) + 1.5268)
    k = math.exp(1)**(.906*math.log(float(hk)) + .8644*math.log(float(pk)) + 1.9975)
    babip = 1.0403*float(h[12]) + .9135*float(p[6]) - .2573

    #couldn't find regression equations for batted balls, so just averaged them out between pitcher and hitter
    ld = (float(h[14]) + float(p[9]))/2
    gb = (float(h[15]) + float(p[10]))/2
    fb = (float(h[16]) + float(p[11]))/2
    iffb = (float(h[17]) + float(p[12]))/2

    #initialize runs
    runs = 0

    #if random number falls in walk range, perform logic syntax to advance baserunners
    if o <= bb:
        #print h[0] + " walked."
        if ob[0] != "":
            if ob[1] != "":
                if ob[2] != "":
                    #print ob[2][0] + " scored."
                    ob[2] = ob[1]
                    ob[1] = ob[0]
                    ob[0] = h
                    runs = 1
                else:
                    ob[2] = ob[1]
                    ob[1] = ob[0]
                    ob[0] = h
            else:
                ob[1] = ob[0]
                ob[0] = h
        else:
            ob[0] = h

        return [0, ob, runs]

    #if random number falls in strikeout range, update outs
    elif o <= bb + k:
        #print h[0] + " struckout."
        return [-1, ob, runs]

    #anything else is a batted ball
    else:
        o = random.uniform(0,1)#another random number for batted ball

        #if batted ball falls in babip range, hit
        if o <= babip:
            iso = random.uniform(0,1)*float(h[10]) #random number weighted by iso or power rating

            #hard iso cutoffs based on line of best fit for 2017-2018 data trends
            #runners updated based on speed
            if iso <= .101:
                #print h[0] + " hit a single."
                if ob[2] != "":
                    #print ob[2][0] + " scored."
                    runs += 1
                    if ob[1] != "" and float(ob[1][11]) >= 3.2:
                        runs +=1
                        ob[2] = ""
                    else:
                        ob[2] = ob[1]
                elif ob[1] != "":
                    ob[1] = ob[0]
                ob[0] = h

            elif iso <= 0.132:
                #print h[0] + " hit a double."
                for b in range(2,-1,-1):
                    if ob[b] != "" and (b == 2 or b == 1):
                        #print ob[b][0] + " scored."
                        runs += 1
                        ob[b] = ""
                    elif ob[b] != "" and b == 0:
                        if float(ob[b][11]) >= 3.7:
                            #print ob[b][0] + " scored."
                            runs += 1
                            ob[0] = ""
                        else:
                            ob[2] = ob[0]
                ob[1] = h
            elif iso <= .135:
                #print h[0] + " hit a triple."
                for b in range(2,-1,-1):
                    if ob[b] != "":
                        #print ob[b][0] + " scored."
                        runs += 1
                        ob[b] = ""
                ob[2] = h
            else:
                #print h[0] + " homered."
                runs += 1
                for b in range(2,-1,-1):
                    if ob[b] != "":
                        #print ob[b][0] + " scored."
                        runs += 1
                        ob[b] = ""
                #print h[0] + " scored."
            return [1, ob, runs]

        #if not hit, out (errors seemed negligible)
        else:
            o = random.uniform(0,1)
            if o <= ld:
                #print h[0] + " lined out."
                i = o

            #groundballs with a runner on first are automatic double plays, couldn't find stats to help come up with a real percentage
            #again speed determines how other runners react i.e. scoring from third, advancing from second to third
            elif o <= ld + gb:
                if ob[0] != "" and sit[1] < 2:
                    ob[0] = ""
                    #print h[0] + " grounded into a double play."
                    if sit == 0:
                        if ob[2] != "":
                            #print ob[2][0] + " scored."
                            ob[2] = ""
                        if ob[1] != "" and float(ob[1][11]) >= 4 and ob[0] == "":
                            #print ob[1][0] + " advanced to third."
                            ob[2] = ob[1]
                            ob[1] = ""
                    return [-2, ob, runs]
                else:
                    #print h[0] + " grounded out."
                    if sit < 2:
                        if ob[2] != "":
                            #print ob[2][0] + " scored."
                            ob[2] = ""
                        if ob[1] != "" and float(ob[1][11]) >= 4 and ob[0] == "":
                            #print ob[1][0] + " advanced to third."
                            ob[2] = ob[1]
                            ob[1] = ""
            else:
                o = random.uniform(0,1) #used random number again to determine if flyball is popout or actual flyout

                #no one moves on popouts
                if o <= iffb:
                    #print h[0] + " popped out."
                    i=o

                #some runners can tag and score if SPD allows it
                else:
                    #print h[0] + " flied out."
                    if ob[2] != "" and float(ob[2][11]) >= 3:
                        #print ob[2][0] + " tagged up and scored from third."
                        runs += 1
                        ob[2] = ""
            return [-1, ob, runs]

def steal(runner, ob, base):
    o = random.uniform(0,1)
    attempt = ((1/330.0) * float(runner[11])**2) + ((13/660.0) * float(runner[11]))
    steal = ((-.6061*(float(runner[11])**2)) + (16.06 * float(runner[11])))/100.0

    #trendlines for 2017-2018 steal data used to determine likelihood of steal and likelihood of successful steal
    if o <= attempt:
        o = random.uniform(0,1)
        if o <= steal:
            string = runner[0] + " stole "
            if base == 0:
                string += "2nd base."
                ob[1] = ob[0]
                ob[0] = ""
            else:
                string += "third base."
                ob[2] = ob[1]
                ob[1] = ""
            #print string
            return [0, ob]
        else:
            #print runner[0] + " was caught stealing."
            ob[base] = ""
            return [1, ob]
    else:
        return [0, ob]
