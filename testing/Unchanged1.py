def unchanging_plurals():

 with open("sentences.txt", "r") as f:

        NNS_list = []
        NN_list = []
        noun_list = []
        count = 0

        for line in f:
            words = line.split(" ")
            for w in words:
                x = w.split("|") 
                
                if (x[1] == "NNS"):
                    NNS_list.append(x[0]) 
                elif (x[1] == "NN"):
                    NN_list.append(x[0])

        #lists with no duplicates
        n_NNS_list = list(set(NNS_list))   
        n_NN_list = list(set(NN_list))

        for i in range(len(n_NNS_list)):
            for j in range(len(n_NN_list)):
                if (n_NNS_list[i] == n_NN_list[j]):
                    noun_list.append(n_NNS_list[i]) 
                    break 
                    #y = len(NNS_list) #to make the loop terminate faster
                    #x += 1
                    #value = NN_list[j]
                    #NNS_list.remove(value)
                   # while  < range(len(NN_list)): #maybe add extra loop
                    #    NN_list.remove(NN_list[j])
        """          
        for i in range(len(NNS_list)):
        #NNS#_list
            for j in range(1, len(NN_list)):
            #NN_list:
                if (NNS_list[i] == NN_list[j]):
                    noun_list.append(NNS_list[i])

                    #NN_list.remove(NN_list[j])
                    #i += 1
                    j = len(NN_list)
                    #print (i)
                    #print (NNS_list[i])     
        
         

            for line in f:
            pos += [(w,t) for (w,t) in (tuple(p.split('|')) for p in line.split()) if (t == "NNS" or t == "NN")]
        for (w, t) in pos:
            try:
                if t not in cands[w]:
                    cands[w] += [t]
            except KeyError:
                cands[w] = [t]

        for w in cands:
            if len(cands[w]) == 2:
                plurals += [w]
        return plurals
        """

        return list(set(noun_list)) 

if __name__ == "__main__":
    
    print(unchanging_plurals())
    
    