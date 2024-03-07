fn calculate_angle() {
    let mut speed = 0;
    let mut x_coordinate = 0.0; // steering coordinate from center
    let mut y_coordinate = 0.0; // steering coordinate from center
    let wheel_base_width = 31; // 40 wheel base width in inches
    let wheel_base_length = 48; // 43 wheel base length in inches
    let mut left_front_wheel_angle = 90.0; // left front wheel angle
    let mut left_rear_wheel_angle = 90.0; // left rear wheel angle
    let mut right_front_wheel_angle = 90.0; // right front wheel angle
    let mut right_rear_wheel_angle = 90.0; // right rear wheel angle
    let mut left_front_wheel_radius = 0.0; // left front wheel radius
    let mut left_rear_wheel_radius = 0.0; // left rear wheel radius
    let mut right_front_wheel_radius = 0.0; // right front wheel radius
    let mut right_rear_wheel_radius = 0.0; // right rear wheel radius
    let mut travel_radius; // radius of tractor travel
    let mut left_front_wheel_speed = 0.0; // left front wheel speed
    let mut left_rear_wheel_speed = 0.0; // left rear wheel speed
    let mut right_front_wheel_speed = 0.0; // right front wheel speed
    let mut right_rear_wheel_speed = 0.0; // right rear wheel speed
    let mut left_front_wheel_direction = 0; // left front wheel direction
    let mut left_rear_wheel_direction = 0; // left rear wheel direction
    let mut right_front_wheel_direction = 0; // right front wheel direction
    let mut right_rear_wheel_direction = 0; // right rear wheel direction

    loop {
        // turning radius of tractor
        if x_coordinate == 0.0 && y_coordinate.abs() > (wheel_base_length as f64) / 2.0 {
            travel_radius = 0.0;
        } else {
            travel_radius = (x_coordinate.powi(2) + y_coordinate.powi(2)).sqrt();
        }

        // calculate left front
        if x_coordinate == 0.0 && y_coordinate.abs() > (wheel_base_length as f64) / 2.0 {
            left_front_wheel_angle = 90.0; // wheel angle
            left_front_wheel_speed = speed as f64; // wheel speed
            left_front_wheel_direction = if y_coordinate > 0.0 { 1 } else { 0 }; // wheel direction
        } else {
            // wheel angle
            left_front_wheel_radius = ((x_coordinate - (wheel_base_width as f64) / 2.0).powi(2) + (y_coordinate - (wheel_base_length as f64) / 2.0).powi(2)).sqrt();
            left_front_wheel_angle = 90.0 - (x_coordinate - (wheel_base_width as f64) / 2.0).atan2(y_coordinate - (wheel_base_length as f64) / 2.0).to_degrees();
            if x_coordinate < 0.0 && y_coordinate > 0.0 {
                left_front_wheel_angle -= 90.0;
            }
            left_front_wheel_angle = if left_front_wheel_angle < 90.0 { left_front_wheel_angle + 90.0 } else { left_front_wheel_angle - 90.0 };

            // wheel speed
            left_front_wheel_speed = if speed == 0 { 0.0 } else { speed as f64 * (left_front_wheel_radius / travel_radius) };

            // wheel direction
            left_front_wheel_direction = if x_coordinate < (wheel_base_width as f64) / 2.0 && y_coordinate < (wheel_base_length as f64) / 2.0 { 1 } else { 0 };
        }

        // calculate right front
        if x_coordinate == 0.0 && y_coordinate.abs() > (wheel_base_length as f64) / 2.0 {
            right_front_wheel_angle = 90.0; // wheel angle
            right_front_wheel_speed = speed as f64; // wheel speed
            right_front_wheel_direction = if y_coordinate > 0.0 { 0 } else { 1 }; // wheel direction
        } else {
            // wheel angle
            right_front_wheel_radius = ((x_coordinate + (wheel_base_width as f64) / 2.0).powi(2) + (y_coordinate - (wheel_base_length as f64) / 2.0).powi(2)).sqrt();
            right_front_wheel_angle = 90.0 - (x_coordinate + (wheel_base_width as f64) / 2.0).atan2(y_coordinate - (wheel_base_length as f64) / 2.0).to_degrees();
            if x_coordinate < 0.0 && y_coordinate > 0.0 {
                right_front_wheel_angle -= 90.0;
            }
            right_front_wheel_angle = if right_front_wheel_angle < 90.0 { right_front_wheel_angle + 90.0 } else { right_front_wheel_angle - 90.0 };

            // wheel speed
            right_front_wheel_speed = if speed == 0 { 0.0 } else { speed as f64 * (right_front_wheel_radius / travel_radius) };

            // wheel direction
            right_front_wheel_direction = if x_coordinate < (wheel_base_width as f64) / 2.0 && y_coordinate < (wheel_base_length as f64) / 2.0 { 0 } else { 1 };
        }
    }
}



fn main() {
    println!("Hello, world!")
}


