class Girls:

    def __init__(self):
        self.topgirl = []
        self.girl0 = ["Olivia", "Mahjong", "Sumo", "Eating out"]
        self.girl1 = ["Emma", "Amateur pankration", "Motor sports", "Cycling"]
        self.girl2 = ["Ava", "Juggling", "Karate", "Powerlifting", "Quidditch"]
        self.girl3 = ["Sophia", "Eating out", "Bowling", "Darts"]
        self.girl4 = ["Isabella", "Fishing", "Kombucha"]
        self.girl5 = ["Charlotte", "Fishing", "Movies"]
        self.girl6 = ["Amelia", "Movies", "Music", "Cycling"]
        self.girl7 = ["Mia", "Music", "Kites", "Models"]
        self.girl8 = ["Harper", "Origami", "Puzzles", "Quilting", "Surfing"]
        self.girl9 = ["Evelyn", "Video Games", "Yoga", "Jogging"]
        self.allgirls = [self.girl0, self.girl1, self.girl2, self.girl3, self.girl4, self.girl5, self.girl6, self.girl7, self.girl8, self.girl9]

    def search(self, hobbies):
        maxscore = -1
        bestgirl = "nobody"
        nowscore = 0
        for i in self.allgirls:
            #print(i[0])
            for h in hobbies:
              if h in i:
                #print(i[0] + " has " + h)
                nowscore+=1
            if nowscore > maxscore:
              maxscore = nowscore
              bestgirl = i
            nowscore = 0
        self.topgirl = bestgirl 
        if maxscore == 0:
            return ["None"]
        print("BG: ", self.topgirl)
        return(bestgirl)

    
    def normalPrint(self, s):
      output = ""
      i = 0
      if len(s) == 0:
          return "None!"
      else:
          while i < len(s):
            output += s[i]
            if (i+1 < len(s)):
              output+= " and "
            else:
              output+="!"
            i+=1
          return output
    
    def details(self, hobbies, girl):
        #print("H ", hobbies)
        #print("G ", girl)
        match = []
        other = []

        i = 0
        while i < len(girl):
          if i == 0:
            print(girl[i] , "is your best match!")
          else:
            if girl[i] in hobbies:
              match.append(girl[i])
            else:
              other.append(girl[i])
          i+=1

        #print("You both like: ", self.normalPrint(match))
        #print("Her other interests are: ", self.normalPrint(other))

        return("You both like: ", self.normalPrint(match), ";  Her other interests are: ", self.normalPrint(other))
