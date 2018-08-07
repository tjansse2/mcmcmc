from Test import TEST

print("gaus-neu")
gauss = TEST("./samples/out/gauss/","./samples/IS-Camel2D-ref/",lag=[0,5,10,15,20,25])

gauss.chiq()
gauss.sequenceLength()
gauss.KolmogorowSmirnow()
gauss.save("gauss")

