# gbRelease
geoBoundaries : A Political Administrative Boundaries Dataset (www.geoboundaries.org)

Please visit www.geoboundaries.org for more details.

#Note: As per https://github.com/mattijn/topojson/issues/84,
#The build of geoBoundaries relies on a slightly modified version
#of topojson, which will be formally incorporated in later builds.
#For the build of geoBoundaries to succeed, until that fix is pushed,
#within toposimplify the default for shapely is changed from
#False to True on line 569: simple_ls = simple_ls.simplify(epsilon, preserve_topology=True) 