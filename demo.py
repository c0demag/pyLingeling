import lingeling

p = lingeling.lglinit()
lingeling.lgladd(p, 1)
lingeling.lgladd(p, -1)
lingeling.lgladd(p, 0)
lingeling.lglassume(p, -1)
assert lingeling.lglsat(p) == lingeling.LGL_SATISFIABLE
print("Done.")
