class DiffMatch:

    def match_string(self, texts1, texts2, tests3, texts4):

        matchList = []
        matchDict = {}
        # tText1 = text1.replace("\n", "").replace(" ", "").replace("　", "")
        # tText2 = text2.replace("\n", "").replace(" ", "").replace("　", "")
        # tText3 = tText2.replace("Z", "2").replace("l", "1").replace("I", "1").replace("O", "0")
        # tText4 = tText2.replace("2", "Z").replace("1", "l").replace("1", "I").replace("0", "O")
        i = 0
        while i < len(texts1):

            j = i + 1
            searchString = texts1[i]
            matchString = ""
            while searchString in texts2[j:] or searchString in tests3[j:] or searchString in texts4[j:]:
                matchString = searchString
                i += 1
                searchString += texts1[i]

            else:
                matchLen = len(matchString)
                if matchLen != 0:
                    if matchDict.get(matchString) is None:
                        matchDict.update({matchString: matchLen})
                    # matchList.append([0, matchString])
                    # i = i - (matchLen - 1)
                else:
                    i += 1

        tmpList = sorted(matchDict.items(), key = lambda x : x[1], reverse=True)
        for tmp in tmpList:
            matchList.append([0, tmp[0]])

        return matchList