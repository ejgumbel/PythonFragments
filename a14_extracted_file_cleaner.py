from os import chdir, listdir
from os.path import isfile, join


def remove_ext(s):
    return s[0:-4]


working_dir = "D:\\DSOD\\Data\\AMAX_Files\\1_day\\"
chdir(working_dir)
onlyfiles = [f for f in listdir(working_dir) if isfile(join(working_dir, f))]

for f in onlyfiles:
    g = working_dir + "\\cleaned\\" + f
    with open(f) as infile:
        with open(g, "w") as outfile:
            for line in infile:
                if line == "\n":
                    break
                s = line.split("\t")
                s1 = s[0]
                s2 = s[1]
                # this detects that a date is in the first column, retrieves the year only
                if "/" in s1:
                    dt = s1.split("/")
                    yr = dt[2]
                    val = s2
                else:
                    # this detects if the value is in the first column, should only be year in second column
                    if "." in s1:
                        val = s1 + "\n"
                        yr = s2.strip()
                outline = yr + "," + val
                outfile.write(outline)
