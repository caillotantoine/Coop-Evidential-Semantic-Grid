# Config file name after "config_" with no extention 
configname="perfect_full_testBBA16"

# Run for each algorithm
echo "Dempster"
python ./Sources/testbench.py --algo Dempster --save_img True --mean True --cooplvl 2 --json_path ./Sources/configs/config_$configname.json --save_path ~/Desktop/Output_Algo/$configname --dataset_path /home/caillot/Documents/Datasets/CARLA_Dataset_B
echo "Conjunctive"
python ./Sources/testbench.py --algo Conjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources//configs/config_$configname.json --save_path ~/Desktop/Output_Algo/$configname --dataset_path /home/caillot/Documents/Datasets/CARLA_Dataset_B
echo "Disjonctive"
python ./Sources/testbench.py --algo Disjunctive --save_img False --mean False --cooplvl 2 --json_path ./Sources/configs/config_$configname.json --save_path ~/Desktop/Output_Algo/$configname --dataset_path /home/caillot/Documents/Datasets/CARLA_Dataset_B
