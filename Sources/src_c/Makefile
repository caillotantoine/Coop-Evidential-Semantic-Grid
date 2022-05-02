CXX=g++
CFLAGS = -I/usr/local/include/opencv4/opencv2 -I/usr/local/include/opencv4 -L/usr/local/lib/
LIBS = -lopencv_stitching -lopencv_aruco -lopencv_bgsegm -lopencv_bioinspired -lopencv_ccalib -lopencv_dnn_objdetect -lopencv_dnn_superres -lopencv_dpm -lopencv_highgui -lopencv_face -lopencv_freetype -lopencv_fuzzy -lopencv_hdf -lopencv_hfs -lopencv_img_hash -lopencv_line_descriptor -lopencv_quality -lopencv_reg -lopencv_rgbd -lopencv_saliency -lopencv_shape -lopencv_stereo -lopencv_structured_light -lopencv_phase_unwrapping -lopencv_superres -lopencv_optflow -lopencv_surface_matching -lopencv_tracking -lopencv_datasets -lopencv_text -lopencv_dnn -lopencv_plot -lopencv_ml -lopencv_videostab -lopencv_videoio -lopencv_viz -lopencv_ximgproc -lopencv_video -lopencv_xobjdetect -lopencv_objdetect -lopencv_calib3d -lopencv_imgcodecs -lopencv_features2d -lopencv_flann -lopencv_xphoto -lopencv_photo -lopencv_imgproc -lopencv_core

target_1=rasterizer
target_2=merger
target_3=decision

# targets := decision merger metrics rasterizer seg_filter

targets := $(shell echo *.cpp )

# gcc -shared -Wl,-soname,PixAvg -o PixAvg.so -fPIC fastAverage.c
# --compiler-options '-fPIC'

#  -fPIC -fdiagnostics-color=always -Wall
#https://forums.developer.nvidia.com/t/shared-library-creation/4776/2
#https://www.geeksforgeeks.org/how-to-call-c-c-from-python/


# all: $(target_1).so $(target_1) $(target_2) $(target_2).so $(target_3) $(target_3).so

# g++ -o rasterizer rasterizer.cpp `pkg-config --cflags --libs opencv4`
print-%  : ; @echo $* = $($*)

# all: $(targets:.cpp=) $(targets:.cpp=.so)

all: $(targets:.cpp=.so) $(targets:.cpp=.out)

%.out: %.cpp
	$(CXX) -o $@ -std=c++11 -g -fdiagnostics-color=always -Wall $? `pkg-config --cflags --libs opencv4`

%.so: %.cpp
	$(CXX) -o $@ -g -std=c++11 -fPIC -shared -fdiagnostics-color=always -Wall $? `pkg-config --cflags --libs opencv4`
	nm -gD $@ | grep ' T ' | grep -v '_Z' | cut -d' ' -f3

clean:
	$(RM) *.out *.o *.so
