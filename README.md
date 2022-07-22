![](https://github.com/Berendei-Jr/CompareFace/actions/workflows/test_build.yaml/badge.svg)
# CompareFace
To use this app the docker container of [CompreFace](https://github.com/exadel-inc/CompreFace) must be running on the machine (it should be available here: http://localhost:8000).  
  
Usage: `./compare_face <path_to_the_source_photo> <path_to_the_target_photo>`  
The app returns to the terminal the "similarity" value of the comparison of 2 faces on the provided photos.  
If the target photo contains more than 1 face, the result would be the max value of similarity.
