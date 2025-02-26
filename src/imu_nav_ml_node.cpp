/*
Два пути:
nn_path_ — путь для данных из топика /imu_nav/nn_predictions (нейронная сеть).
ekf_path_ — путь для данных из топика /imu_nav/ned_ekf (EKF).

Два издателя:
nn_path_pub_ — публикует путь для нейронной сети в топик /imu_nav/nn_path.
ekf_path_pub_ — публикует путь для EKF в топик /imu_nav/ekf_path.

Коллбеки:
В imuNavCallback данные добавляются в nn_path_ и публикуются.
В posVelCallback данные добавляются в ekf_path_ и публикуются.

Функция addPointToPath:
Универсальная функция для добавления точки в любой путь (nn_path_ или ekf_path_).
*/

#include <ros/ros.h>
#include <imu_nav_ml/ImuNavPrediction.h>
#include <imu_nav_ml/PosVel.h>
#include <nav_msgs/Path.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/PoseStamped.h>
#include <std_msgs/Header.h>

class ImuNavMLNode {
public:
    ImuNavMLNode() {
        // Инициализация подписчиков
        imu_nav_sub_ = nh_.subscribe("/imu_nav/nn_predictions", 10, &ImuNavMLNode::imuNavCallback, this);
        pos_vel_sub_ = nh_.subscribe("/imu_nav/ned_ekf", 10, &ImuNavMLNode::posVelCallback, this);

        // Инициализация издателей для Path
        nn_path_pub_ = nh_.advertise<nav_msgs::Path>("/imu_nav/nn_path", 10);
        ekf_path_pub_ = nh_.advertise<nav_msgs::Path>("/imu_nav/ekf_path", 10);

        // Инициализация Path
        nn_path_.header.frame_id = "map"; // Указываем фрейм для RViz
        ekf_path_.header.frame_id = "map"; // Указываем фрейм для RViz
    }

private:
    ros::NodeHandle nh_;
    ros::Subscriber imu_nav_sub_;
    ros::Subscriber pos_vel_sub_;
    ros::Publisher nn_path_pub_;
    ros::Publisher ekf_path_pub_;
    nav_msgs::Path nn_path_;
    nav_msgs::Path ekf_path_;

    void imuNavCallback(const imu_nav_ml::ImuNavPrediction::ConstPtr& msg) {
        // Добавляем точку из ImuNavPrediction в Path для нейронной сети
        addPointToPath(nn_path_, msg->position, msg->header.stamp);

        // Публикуем Path для нейронной сети
        nn_path_pub_.publish(nn_path_);
    }

    void posVelCallback(const imu_nav_ml::PosVel::ConstPtr& msg) {
        // Добавляем точку из PosVel в Path для EKF
        addPointToPath(ekf_path_, msg->position, msg->header.stamp);

        // Публикуем Path для EKF
        ekf_path_pub_.publish(ekf_path_);
    }

    void addPointToPath(nav_msgs::Path& path, const geometry_msgs::Point& point, const ros::Time& timestamp) {
        // Создаем PoseStamped для добавления в Path
        geometry_msgs::PoseStamped pose_stamped;
        pose_stamped.header.stamp = timestamp;
        pose_stamped.header.frame_id = "map";
        pose_stamped.pose.position = point;

        // Добавляем PoseStamped в Path
        path.poses.push_back(pose_stamped);

        // Обновляем заголовок Path
        path.header.stamp = ros::Time::now();
    }
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "imu_nav_ml_node");
    ImuNavMLNode node;
    ros::spin();
    return 0;
}