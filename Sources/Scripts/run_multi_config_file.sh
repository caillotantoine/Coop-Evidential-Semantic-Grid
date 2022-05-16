datasetname="CARLA_Dataset_B"

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1a"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_2"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname


# Config file name after "config_" with no extention 
configname="test_config/full_NN_3"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_disj1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname





datasetname="CARLA_Dataset_original"

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1a"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_2"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname


# Config file name after "config_" with no extention 
configname="test_config/full_NN_3"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_disj1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname






datasetname="CARLA_Dataset_intersec_dense"

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_1a"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_2"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname


# Config file name after "config_" with no extention 
configname="test_config/full_NN_3"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname

# Config file name after "config_" with no extention 
configname="test_config/full_NN_disj1"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --start 50 --end 200 --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Conjunctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname
echo "Disjonctive"
python ./Sources/testbench.py --start 50 --end 200 --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/$configname.json --save_path ~/Desktop/Output_Algo/$datasetname/$configname --dataset_path /home/caillot/Documents/Datasets/$datasetname





