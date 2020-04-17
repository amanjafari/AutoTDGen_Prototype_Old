"""

Aotumated test input generation
using activity diagram and genetic algorithm

"""

import datetime
import random
import unittest
from TestTDGen_demo import genetic


# all_dup_list = {
#     "locks":[["13", "locks>=1","Y"],
#                      ["13","locks>=1","14","15","16","T"]],
#     "locks":[["19","20","locks>=1","Y"],

#                      ["19", "20", "locks>=4", "15","16" , "T"]],
#     "stocks":[["15", "stocks>=1","T"]],
#     "barrels":[["15", "barrels>=1","T"]],
#     "sales": [["27", "sales>=1800", "Y"],
#                           ["27", "sales>=1800", "29", "Y"],
#                           ["27", "sales>=1800", "29", "30", "31", "32", "33", "T"],
#                           ["27", "29", "sales>=1000", "Y"],
#                           ["27", "sales>=1000", "35", "36", "37", "T"],
#                           ["27", "29", "sales<=990", "38", "39", "T"]],
#     "commission":[["20", "31 <= commission && commission < 15","T"]]
#                 }


all_dup_list = {
    "locks":[["13", "locks>=1","Y"],
                     ["13","locks>=1","14","15","16","N"],
                     ["19","20","locks>=1","Y"],
                     ["19", "20", "locks>=4", "15","16" , "N"]],
    "stocks":[["15", "stocks>=1","N"]],
    "barrels":[["15", "barrels>=1","N"]],
    "commission":[["20", "15 < commission && commission <= 31","N"]],
    "sales": [["27", "sales>=1800", "Y"],
                          ["27", "sales>=1800", "29", "Y"],
                          ["27", "sales>=1800", "29", "30", "31", "32", "33", "N"],
                          ["27", "29", "sales>=1000", "Y"],
                          ["27", "sales>=1000", "35", "36", "37", "N"],
                          ["27", "29", "sales<=900", "38", "39", "N"]],
                }


""" 
 all_dup_list = {
                  "engine":[["Car Simulation", "Start the car engine","Y"],
                   ["Car Simulation","Start the car engine","Fork", "Accelerate the car", "engine>0", "N"]]
                 # "brakepedal":[["Car Simulation", "Start the care engine", "Fork", "Accelerate the care", "engine is not null", "brakepedal > 0","Y"],
                 #               ["Car Simulation", "Start the care engine", "Fork", "Accelerate the care","engine is not null", "brakepedal > 0"," set brakepedel to zero","N"]],
                 # "brakepedel":[["Car Simulation", "Start the car engine", "Fork, Brake the car", "engine != null", "brakepedal < maxBrake-1", "Y"],
                 #               ["Car Simulation", "Start the car engine", "Fork, Brake the car", "engine != null", "brakepedal < 9","increment brakepedal by one","N"]],
                 # "throttle":[["Car Simulation", "Start the car engine", "Fork",  "Accelerate the car", "throttle < maxThrottle - 5","Y"],
                 #             ["Car Simulation", "Start the car engine", "Fork", "Accelerate the car", "throttle < 5", "increment throttle by five","N"]],
                 # "throttle":[["Car Simulation", "Start the car engine", "Fork", "Brake the car", "engine not null", "throttle > 0", "N"]]
                 }
"""

geneset = [i for i in range(1, 9040)]


def get_fitness(genes, dups):
    fitness = Fitness(sum(abs(e(genes)) for e in dups))
    return fitness


def display(candidate, startTime, fnGenesToInputs,v):
    timeDiff = "Time Diff ," + str(datetime.datetime.now() - startTime)
    result = str(v) +" , " +  str(fnGenesToInputs(candidate.Genes))
    print("{}\t{}\t{}".format(result, candidate.Fitness, timeDiff))


def mutate(genes, sortedGeneset, window, geneIndexes):
    indexes = random.sample(geneIndexes, random.randint(1, len(genes))) \
        if random.randint(0, 10) == 0 else [random.choice(geneIndexes)]
    window.slide()
    while len(indexes) > 0:
        index = indexes.pop()
        genesetIndex = sortedGeneset.index(genes[index])
        start = max(0, genesetIndex - window.Size)
        stop = min(len(sortedGeneset) - 1, genesetIndex + window.Size)
        genesetIndex = random.randint(start, stop)
        genes[index] = sortedGeneset[genesetIndex]



class DUPathsTests(unittest.TestCase):

    def fnBranchDistance(sefl, list, index):
        vars_key = sefl.fnGet_var()
        total_dup_list = list.__getitem__(vars_key[index])
        list_to_cover = []
        len_list = len(total_dup_list)
        num_dup_covered = 0

        for i, value in enumerate(total_dup_list):
            for e in value[-1:]:
                if e == "Y":
                    num_dup_covered+=1
                elif e == "N":
                    list_to_cover = value
                    num_dup_covered += 1
                    break
                else:
                    continue
            else:
                continue
            break

        for _ in range(num_dup_covered):
            i = 0
            total_dup_list.pop(i)

        unvisited_list = [list_to_cover]

        predicates = []
        left_operand = 0
        var = 0
        var2 = 0

        while len(unvisited_list) > 0:
            for (i, val) in enumerate(unvisited_list):
                for e in val:
                    #  ad = "&&" if e.__contains(ad) and e.con...(".")
                    if "&&" in e:
                        a = e.split()
                        predicates.append(e)
                        left_operand = ''.join(a[2:3])
                        var = ''.join(a[0:1])
                        var2 = ''.join(a[-1:])


                    elif ">=" in e:
                        ge = e.split(">=")
                        # predicates.append(ne[0] + " - " + ne[1])
                        predicates.append(e)
                        left_operand = ''.join(ge[0])
                        var = ''.join(ge[1])
                    elif ">" in e:
                        g = e.split(">")
                        predicates.append(e)
                        left_operand = ''.join(g[0])
                        var = ''.join(g[1])

                    elif "<=" in e:
                        le = e.split("<=")
                        predicates.append(e)
                        left_operand = ''.join(le[0])
                        var = ''.join(le[1])

                    elif "<" in e:
                        l = e.split("<")
                        predicates.append(e)
                        left_operand = ''.join(l[0])
                        var = ''.join(l[1])

                    elif "==" in e:
                        e = e.split("==")
                        predicates.append(e)
                        left_operand = ''.join(e[0])
                        var = ''.join(e[1])

                    elif "!=" in e:
                        ne = e.split("!=")
                        # predicates.append(ne[0] + " - " + ne[1])
                        predicates.append(e)
                        left_operand = ''.join(ne[0])
                        var = ''.join(ne[1])


            return left_operand, var, var2, num_dup_covered, total_dup_list, len_list,predicates, vars_key

    def fnGet_var(self):
        var_key_list = []
        for k in all_dup_list.keys():
            var_key_list.append(k)

        return var_key_list


    def test_real_inputs_T1(self, index=0):

        index = index
        left_operand, data_member, data_member2, dup_covered, tdl,du_pair, pred, var_list = self.fnBranchDistance(all_dup_list, index)
        print("The number of du-pair covered ,", dup_covered, "\n", "The predicate covered ,", pred)

        def fnGenesToInputs(genes):
            # return genes[0],genes[1],genes[2]
            return genes[0]


        def Branche_distance(genes):
            # locks, stocks, barrels = fnGenesToInputs(genes)
            # data_member = locks + stocks  + barrels
            left_operand = fnGenesToInputs(genes)
            branch_distance = 0
            for elem in pred:
                # if ">=" or ">" in elem:

                if "&&" in elem:
                    # branch_distance = (left_operand - int(data_member)) + (left_operand - int(data_member2))
                    branch_distance = ( left_operand - int(data_member) + int(data_member))
                    if branch_distance > 15 and branch_distance <= 31:
                        branch_distance = 0
                    else:
                        branch_distance


                elif ">=" or ">" in elem:
                    branch_distance = left_operand - int(data_member)
                    if branch_distance == 0:
                        branch_distance = 0
                    else:
                        branch_distance

                elif "<=" or "<" in elem:
                    branch_distance = int(data_member) - left_operand
                    if branch_distance == 0:
                        branch_distance = 0
                    else:
                        branch_distance

                elif "==" in elem:
                    branch_distance = abs(int(data_member) - left_operand)

                elif "!=" in elem:
                    branch_distance = abs(int(data_member) - left_operand)

                # elif "=<" or "=<" in elem:
                #     branch_distance = 0
                else:
                    branch_distance = 0

            dup_len = len(all_dup_list)
            approach_level = (du_pair - dup_covered) / (du_pair + dup_len)
            # approach_level = (du_pair - dup_covered) * 1 / (du_pair + dup_len)

            return approach_level + abs(branch_distance)

        dups = [Branche_distance]
        best = self.solve_indiuidual(1, geneset, dups, fnGenesToInputs,left_operand)

        if not best == 0 and not len(tdl)==0:
            self.test_real_inputs_T1(index)

        elif len(tdl) == 0 and not len(var_list) == 0:
            index = index + 1
            if not index > len(var_list)-1:
                self.test_real_inputs_T1(index)

        else:
            print("\n\t\t", "----Test Generation Successfuly Completed-----!")


    def solve_indiuidual(self, induiduals, geneset, dups, fnGenesToInputs,var):
        startTime = datetime.datetime.now()
        maxAge = 50
        window = Window(max(1, int(len(geneset) / (2 * maxAge))),
                        max(1, int(len(geneset) / 3)),
                        int(len(geneset) / 2))
        geneIndexes = [i for i in range(induiduals)]
        sortedGeneset = sorted(geneset)

        def fnDisplay(candidate):
            display(candidate, startTime, fnGenesToInputs, var)

        def fnGetFitness(genes):
            return get_fitness(genes, dups)

        def fnMutate(genes):
            mutate(genes, sortedGeneset, window, geneIndexes)

        optimalFitness = Fitness(0.99)
        best = genetic.get_best(fnGetFitness, induiduals, optimalFitness,
                                geneset, fnDisplay, fnMutate, maxAge=maxAge)
        print("Best", best.Fitness)
        self.assertTrue(not optimalFitness > best.Fitness)
        return best.Fitness


class Fitness:
    def __init__(self, totalFitness):
        self.TotalFitness = totalFitness

    def __gt__(self, other):
        return self.TotalFitness < other.TotalFitness

    def __str__(self):
        return "Fitness , {:0.2f}".format(float(self.TotalFitness))


class Window:
    def __init__(self, minimum, maximum, size):
        self.Min = minimum
        self.Max = maximum
        self.Size = size

    def slide(self):
        self.Size = self.Size - 1 if self.Size > self.Min else self.Max


if __name__ == '__main__':
    unittest.main()
