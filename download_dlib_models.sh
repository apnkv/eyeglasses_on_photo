echo "Downloading dlib's face detector"
wget http://dlib.net/files/mmod_human_face_detector.dat.bz2
bzip2 -d ./mmod_human_face_detector.dat.bz2

echo "Downloading dlib's face shape predictor..."
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d ./shape_predictor_68_face_landmarks.dat.bz2

echo "Downloading dlib's face shape predictor..."
wget http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2
bzip2 -d ./shape_predictor_5_face_landmarks.dat.bz2

echo "Done"
