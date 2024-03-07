#include <stdio.h>
#include <math.h>

typedef struct {
    float left_front_speed;
    float right_front_speed;
} WheelSpeeds;

WheelSpeeds calculate_wheel_speeds(int speed, float x_coordinate, float y_coordinate) {
    int wheelBaseWidth = 31;  // 40 wheel base width in inches
    int wheelBaseLength = 48; // 43 wheel base length in inches

    float lfa, rfa, lfr, rfr, travelRadius;
    float lfs, rfs;

    WheelSpeeds speeds;

    // turning radius of tractor
    if (x_coordinate == 0 && fabs(y_coordinate) > wheelBaseLength / 2) {
        travelRadius = 0;
    } else {
        travelRadius = sqrt(pow(x_coordinate, 2) + pow(y_coordinate, 2));
    }

    // calculate left front
    // wheel angle
    if (x_coordinate == 0 && fabs(y_coordinate) > wheelBaseLength / 2) {
        lfa = 90;  // wheel angle
        lfs = speed;   // wheel speed
    } else {
        lfr = sqrt(pow(x_coordinate - (float)wheelBaseWidth / 2, 2) + pow(y_coordinate - (float)wheelBaseLength / 2, 2));
        lfa = 90 - (atan((x_coordinate - (float)wheelBaseWidth / 2) / (y_coordinate - (float)wheelBaseLength / 2)) * 180 / 3.14159);
        if (x_coordinate < 0 && y_coordinate > 0) lfa = lfa - 90;
        lfa = lfa < 90 ? lfa + 90 : lfa - 90;

        // wheel speed
        lfs = speed == 0 ? 0 : speed * (lfr / travelRadius);
    }

    // calculate right front
    // wheel angle
    if (x_coordinate == 0 && fabs(y_coordinate) > wheelBaseLength / 2) {
        rfa = 90;  // wheel angle
        rfs = speed;   // wheel speed
    } else {
        rfr = sqrt(pow(x_coordinate + (float)wheelBaseWidth / 2, 2) + pow(y_coordinate - (float)wheelBaseLength / 2, 2));
        rfa = 90 - (atan((x_coordinate + (float)wheelBaseWidth / 2) / (y_coordinate - (float)wheelBaseLength / 2)) * 180 / 3.14159);
        if (x_coordinate < 0 && y_coordinate > 0) rfa = rfa - 90;
        rfa = rfa < 90 ? rfa + 90 : rfa - 90;

        // wheel speed
        rfs = speed == 0 ? 0 : speed * (rfr / travelRadius);
    }

    speeds.left_front_speed = lfs;
    speeds.right_front_speed = rfs;

    return speeds;
}

int main() {
    int speed;
    float x_coordinate, y_coordinate;
    WheelSpeeds speeds;

    printf("Enter a speed: ");
    scanf("%d", &speed);
    printf("Enter an x_coordinate: ");
    scanf("%f", &x_coordinate);
    printf("Enter an y_coordinate: ");
    scanf("%f", &y_coordinate);

    speeds = calculate_wheel_speeds(speed, x_coordinate, y_coordinate);

    printf("Left front wheel speed: %.2f\n", speeds.left_front_speed);
    printf("Right front wheel speed: %.2f\n", speeds.right_front_speed);

    return 0;
}
