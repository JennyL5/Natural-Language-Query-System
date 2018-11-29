def unchanging_plurals():

 with open("sentences.txt", "r") as f:

        NNS_list = []
        NN_list = []
        noun_list = []
        for line in f:
            words = line.split(" ")
            for w in words:
                x = w.split("|") 
                
                if (x[1] == "NNS"):
                    NNS_list.append(x[0]) 
                elif (x[1] == "NN"):
                    NN_list.append(x[0])
            
            #print (x[0]) 
            #/for i in NN_list: 
        for i in range(10):      
            if (NNS_list[i] == NN_list[w]):
                noun_list.append(NNS_list[i])
                i += 1
                print ("h")
                print (NNS_list[i])
              #  print (NN_list[i] )      
                
        """
         #for i in range(10):
        for i in range(1):
            print (NNS_list[i])  
            print ("H")

      #  for i in range(10):
        for i in NN_list:
            print (NN_list[i] )         
        
        for i in range(1, len(NNS_list)):
        #NNS_list
            for j in range(1, len(NN_list)):
            #NN_list:
                if (NNS_list[i] == NN_list[j]):
                    noun_list.append(NNS_list[i])
                    i += 1
                    print (NNS_list[i])
        
        #for i in range(10):
        for i in NN_list:
            print (noun_list[i] )         
        """
        
        return noun_list  

if __name__ == "__main__":
    
    print(unchanging_plurals())
    
    