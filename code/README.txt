In the atrain dataset, the list of movies in the testset that are completely new to the user:
(userID movieID)
900 280
708 280
81 280
2 280
319 267
576 280
637 280
891 280
52 280
477 280

Results for various functions for the atrain.json and atest.json datasets:
value + attrib: 1.07378821562
1/value * 1/attrib: 1.1094408883
1/value**2 * 1/attrib**2: 1.12611371607
value ** attrib: 1.07042054757
value ** (1/attrib): nan, for some reason
attrib ** value: 1.07655367918
attrib ** (1/attrib): nan, for some reason
1 / value ** attrib: 1.09066530721