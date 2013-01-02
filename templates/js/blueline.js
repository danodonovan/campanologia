var settings = {
    "canvas": {
        "x_width": 32,  "y_width": 18,
        "x_margin": 40, "x_R_margin": 12,
        "y_margin": 20,
        "y_position_margin": 200,
        "y_bottom_overlap": 20,
        "pixel_offset": 0.0,
        "x_font_offset": 0.0,
        "y_font_offset": 0.0,
        // ???
        "canvas_x_position": 50,
        // draw bell numbers
        "foncontext": "bold 18px Helvetica Neue",
        // place notation
        "pn_x_offset": 10, 
        "pn_y_offset": 10,
        "pn_foncontext": "bold 12px Helvetica Neue",
        // lead ends
        "le_colour": "#000000",
        "x_le_margin": 20,
    }
};

$(document).ready(
    function draw_blue_line() {

        var course = new Course({{method.nbells}}, {{method.nchanges}}, "{{method.places}}");

        // fact checking
        // assert(course.lead_ends.length == {{method.nleadends}});

        var le_length = course.lead_ends[0];
        var n_le = course.lead_ends.length;

        var height = (le_length * settings.canvas.y_width) + settings.canvas.y_bottom_overlap;
        var width = settings.canvas.x_margin + settings.canvas.x_R_margin + (course.n_bells * settings.canvas.x_width);

        // create the canvas
        create_lead_canvas(n_le, width, height);

		var context = document.getElementById('canvas_all').getContext("2d");
		draw_all_lines(course, context, settings.canvas, 0, le_length);

        var lead_end_i = 0;
        for (lead_end_i = 0; lead_end_i < course.lead_ends.length; ++lead_end_i ) {

            var canvas = document.getElementById('canvas_' + (lead_end_i+1));
            var context = canvas.getContext("2d");

            // start and end
            var start_y = le_length * lead_end_i;
            var end_y = le_length * (lead_end_i + 1);

            // to some extent these should be user editable

            var nchanges = course.lead_ends[lead_end_i];

            var y = 0; var x = 0; var y_i = 0; 
            var x_pos = 0; var y_pos = 0;

            // draw the numbers in
            draw_numbers(course, context, settings.canvas, start_y, end_y);

            // draw in the place notation
            if (lead_end_i == 0) {
                draw_place_notation(course, context, settings.canvas, nchanges);
            }

            // draw treble
            draw_line(1, course, context, settings.canvas, start_y, end_y, "rgba(255, 0, 0, 0.7)");

            // draw active bell
            draw_line(2, course, context, settings.canvas, start_y, end_y, "rgba(0, 0, 255, 0.7)");

            if (lead_end_i != 0) {
                draw_lead_end_line(course, context, settings.canvas);
            }
        }
    }
);
