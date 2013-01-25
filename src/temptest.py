'''
Created on 2013-1-24

@author: VTX
'''

result =   [[["国","state","Guó",""]],
            [
             ["名词",
              ["州","态","状况","国","境界","邦","状","态势","国度","局势","公家","候"],
              [
               ["州",["state","prefecture","province","commonwealth"],,0.035304319],
               ["态",["state","condition","form","appearance","voice"],,0.029729217],
               ["状况",["situation","status","condition","state","circumstance","fettle"],,0.01720595],
               ["国",["country","state","nation"],,0.012987733],
               ["境界",["realm","state","boundary","border","ambit"],,0.0024403227],
               ["邦",["state","nation","country","commonwealth"],,0.0024024891],
               ["状",["shape","state","condition","certificate","account","written complaint"],,0.0019304542],
               ["态势",["situation","posture","state"],,0.00040464516],
               ["国度",["country","nation","state"],,0.00025322047],
               ["局势",["situation","state"],,2.4300831e-05],
               ["公家",["public","state","organization"],,1.8058845e-05],
               ["候",["time","season","condition","state"],,1.6797342e-06]
              ]
             ],
             ["形容词",["国家的","国营的","国有的","国立的"],[["国家的",["state"],,0.0048531611],["国营的",["state"],,7.6030577e-05],["国有的",["state"],,7.031679e-05],["国立的",["state"],,6.4390792e-06]]],
             ["动词",["述","声明","陈述","表示","申明","称","声称","申述","述说","诉说","陈","称述","申","发表","诉","陈说","胪","发言","硬说","拥","摅"],[["述",["state","narrate","relate","tell"],,0.0010332976],["声明",["declare","state","announce"],,0.0010172778],["陈述",["state"],,0.00069916417],["表示",["represent","indicate","express","show","mean","state"],,0.00023787863],["申明",["declare","state","avow"],,0.00021323303],["称",["say","call","name","weigh","praise","state"],,3.4809334e-05],["声称",["claim","assert","proclaim","state"],,2.4683513e-05],["申述",["state","explain in detail"],,9.368805e-06],["述说",["recount","narrate","state"],,4.3568989e-06],["诉说",["tell","recount","relate","narrate","pour","state"],,3.7853395e-06],["陈",["explain","exhibit","narrate","arrange","display","state"],,2.9023204e-06],["称述",["state","narrate","relate"],,2.857324e-06],["申",["explain","state","extend"],,2.4439987e-06],["发表",["publish","issue","deliver","announce","address","state"],,1.9033882e-06],["诉",["appeal","tell","pour","recount","lodge a complaint","state"],,1.4823602e-06],["陈说",["state","explain"],,1.3287791e-06],["胪",["state"],,1.1015966e-06],["发言",["speak","say","voice","remark","express","state"],,7.2244467e-07],["硬说",["assert","allege","avow","emphasize","stubbornly insist","state"],,7.0021741e-07],["拥",["have","own","possess","embrace","support","state"],,7.0021741e-07],["摅",["express","jump up","dart","leap up","scatter","state"],,7.0021741e-07]]]
            ], 
            "en",,
            [["国",[5],0,0,1000,0,1,0]],
            [["state",4,,,""],["state",5,[["国",1000,0,0],["州",0,0,0],["态",0,0,0],["状况",0,0,0],["国家的",0,0,0]],[[0,5]],"state"]]
            ]


simple = result[0][0] # list
words = result[1]
for i in words:
    print u'词性', i[0]
    for j in i[1]:
        print u'推荐', j
    for j in i[2]:
        for k in j:
            for l in k:
                print 'details', 
            


if __name__ == '__main__':
    pass