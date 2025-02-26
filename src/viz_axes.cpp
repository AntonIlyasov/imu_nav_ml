#include <ros/ros.h>
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "axes_with_labels_publisher");
    ros::NodeHandle nh;
    ros::Publisher marker_pub = nh.advertise<visualization_msgs::Marker>("axes_with_labels", 10);
    ros::Rate rate(10);

    // Смещение начала координат
    double offset_x = 0.0;
    double offset_y = 0.0;
    double offset_z = 0.0;

    while (ros::ok()) {
        // Создаем маркеры для каждой оси
        visualization_msgs::Marker axis_x, axis_y, axis_z;

        // Общие настройки для всех осей
        axis_x.header.frame_id = axis_y.header.frame_id = axis_z.header.frame_id = "map";
        axis_x.header.stamp = axis_y.header.stamp = axis_z.header.stamp = ros::Time::now();
        axis_x.ns = "axis_x";  // Уникальные пространства имен для каждой оси
        axis_y.ns = "axis_y";
        axis_z.ns = "axis_z";
        axis_x.action = axis_y.action = axis_z.action = visualization_msgs::Marker::ADD;
        axis_x.type = axis_y.type = axis_z.type = visualization_msgs::Marker::LINE_LIST;
        axis_x.scale.x = axis_y.scale.x = axis_z.scale.x = 0.1;  // Толщина линий

        // Настройка цветов
        axis_x.color.r = 1.0; axis_x.color.a = 1.0;  // Ось X — красная
        axis_y.color.g = 1.0; axis_y.color.a = 1.0;  // Ось Y — зеленая
        axis_z.color.b = 1.0; axis_z.color.a = 1.0;  // Ось Z — синяя

        // Точки для осей
        geometry_msgs::Point p1, p2_x, p2_y, p2_z, p3_x, p3_y, p3_z;

        // Начало координат с учетом смещения
        p1.x = offset_x;
        p1.y = offset_y;
        p1.z = offset_z;

        // Ось X (красная)
        p2_x.x = offset_x + 100;  // Конец оси X (+100)
        p2_x.y = offset_y;
        p2_x.z = offset_z;
        p3_x.x = offset_x - 100;  // Конец оси X (-100)
        p3_x.y = offset_y;
        p3_x.z = offset_z;

        // Ось Y (зеленая)
        p2_y.x = offset_x;
        p2_y.y = offset_y + 100;  // Конец оси Y (+100)
        p2_y.z = offset_z;
        p3_y.x = offset_x;
        p3_y.y = offset_y - 100;  // Конец оси Y (-100)
        p3_y.z = offset_z;

        // Ось Z (синяя)
        p2_z.x = offset_x;
        p2_z.y = offset_y;
        p2_z.z = offset_z + 100;  // Конец оси Z (+100)
        p3_z.x = offset_x;
        p3_z.y = offset_y;
        p3_z.z = offset_z - 100;  // Конец оси Z (-100)

        // Добавляем линии осей
        axis_x.points.push_back(p1); axis_x.points.push_back(p2_x);  // Ось X (+)
        axis_x.points.push_back(p1); axis_x.points.push_back(p3_x);  // Ось X (-)
        axis_y.points.push_back(p1); axis_y.points.push_back(p2_y);  // Ось Y (+)
        axis_y.points.push_back(p1); axis_y.points.push_back(p3_y);  // Ось Y (-)
        axis_z.points.push_back(p1); axis_z.points.push_back(p2_z);  // Ось Z (+)
        axis_z.points.push_back(p1); axis_z.points.push_back(p3_z);  // Ось Z (-)

        // Публикуем оси
        marker_pub.publish(axis_x);
        marker_pub.publish(axis_y);
        marker_pub.publish(axis_z);

        // Создаем маркеры для подписей
        for (int i = -1000; i <= 1000; i += 20) {  // Подписи через каждые 5 метров
            if (i == 0) continue;  // Пропускаем начало координат

            // Подписи для оси X
            visualization_msgs::Marker text_marker_x;
            text_marker_x.header.frame_id = "map";
            text_marker_x.header.stamp = ros::Time::now();
            text_marker_x.ns = "axes_labels_x";
            text_marker_x.id = i + 1000;  // Уникальный ID
            text_marker_x.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
            text_marker_x.action = visualization_msgs::Marker::ADD;
            text_marker_x.pose.position.x = i;  // Подписи не смещены
            text_marker_x.pose.position.y = 0;
            text_marker_x.pose.position.z = 0;
            text_marker_x.scale.z = 6;  // Размер текста
            text_marker_x.color.r = 1.0;  // Красный цвет для подписей оси X
            text_marker_x.color.g = 0.0;
            text_marker_x.color.b = 0.0;
            text_marker_x.color.a = 1.0;
            text_marker_x.text = std::to_string(i) + "m";
            marker_pub.publish(text_marker_x);

            // Подписи для оси Y
            visualization_msgs::Marker text_marker_y;
            text_marker_y.header.frame_id = "map";
            text_marker_y.header.stamp = ros::Time::now();
            text_marker_y.ns = "axes_labels_y";
            text_marker_y.id = i + 2000;  // Уникальный ID
            text_marker_y.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
            text_marker_y.action = visualization_msgs::Marker::ADD;
            text_marker_y.pose.position.x = 0;
            text_marker_y.pose.position.y = i;  // Подписи не смещены
            text_marker_y.pose.position.z = 0;
            text_marker_y.scale.z = 6;  // Размер текста
            text_marker_y.color.r = 0.0;
            text_marker_y.color.g = 1.0;  // Зеленый цвет для подписей оси Y
            text_marker_y.color.b = 0.0;
            text_marker_y.color.a = 1.0;
            text_marker_y.text = std::to_string(i) + "m";
            marker_pub.publish(text_marker_y);

            // Подписи для оси Z
            visualization_msgs::Marker text_marker_z;
            text_marker_z.header.frame_id = "map";
            text_marker_z.header.stamp = ros::Time::now();
            text_marker_z.ns = "axes_labels_z";
            text_marker_z.id = i + 3000;  // Уникальный ID
            text_marker_z.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
            text_marker_z.action = visualization_msgs::Marker::ADD;
            text_marker_z.pose.position.x = 0;
            text_marker_z.pose.position.y = 0;
            text_marker_z.pose.position.z = i;  // Подписи не смещены
            text_marker_z.scale.z = 6;  // Размер текста
            text_marker_z.color.r = 0.0;
            text_marker_z.color.g = 0.0;
            text_marker_z.color.b = 1.0;  // Синий цвет для подписей оси Z
            text_marker_z.color.a = 1.0;
            text_marker_z.text = std::to_string(i) + "m";
            marker_pub.publish(text_marker_z);
        }

        rate.sleep();
    }

    return 0;
}