# ROS
echo "Installing ROS "
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
#sudo apt-get install ros-kinetic-desktop-full # all dependencies
sudo apt-get install ros-kinetic-ros-base
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
source /opt/ros/kinetic/setup.bash
#echo "source /opt/ros/kinetic/setup.zsh" >> ~/.zshrc
#source ~/.zshrc
sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential


# Dependencies
echo "Installing Dependencies "
sudo apt install  cmake qt5-default qt4-default libqt5svg5-dev libprotobuf-dev protobuf-compiler libode-dev screen 
sudo apt install python-qt4 git


## Install latest cmake
echo "Installing latest cmake"
mkdir temp_dir && cd temp_dir
wget https://cmake.org/files/v3.8/cmake-3.8.0.tar.gz
tar xf cmake-3.8.0.tar.gz
cd cmake-3.8.0
./configure
make --quiet -j4
sudo make install
cd ../../
rm -rf temp_dir

## Install vartypes
echo "Installing vartypes"
mkdir temp_dir && cd temp_dir
git clone https://github.com/legacy-roboime/vartypes.git
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/vartypes/vartypes-0.7.tar.gz
tar xfz vartypes-0.7.tar.gz
cd vartypes
mkdir build && cd build
cmake ..
make --quiet -j4
sudo make install
cd ../../../
rm -rf temp_dir

#catkin_make
catkin_make --pkg krssg_ssl_msgs
catkin_make