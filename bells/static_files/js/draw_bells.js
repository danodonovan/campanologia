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
        "x_le_margin": 20
    }
};

function create_lead_canvas(nleadends, width, height) {

    var div = document.getElementById('method_blocks')
    div.setAttribute('height', height * nleadends);

    span = document.createElement('span');
    span.setAttribute('id', 'span_canvas_all');
    document.getElementById('method_blocks').appendChild(span);

    var canvas = document.createElement('canvas');
    canvas.setAttribute('class', 'method_block');
    canvas.setAttribute('width', width);
    canvas.setAttribute('height', height);
    canvas.setAttribute('id', 'canvas_all');

    document.getElementById('span_canvas_all').appendChild(canvas);

    var lead_end_i = 0;
    for (lead_end_i = 0; lead_end_i < nleadends; ++lead_end_i ) {

        var span_id = 'dc_' + (lead_end_i+1);
        var canvas_id = 'canvas_' + (lead_end_i+1);

        span = document.createElement('span');
        span.setAttribute('id', span_id);
        document.getElementById('method_blocks').appendChild(span);

        var canvas = document.createElement('canvas');
        canvas.setAttribute('class', 'method_block');
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        canvas.setAttribute('id', canvas_id);

        document.getElementById(span_id).appendChild(canvas);
    }
}

function draw_numbers(course, context, sc, start_y, end_y) {
    context.font = sc.foncontext;
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    var y_0 = 0; var y = 0;  var x = 0; var bell = 1;
    var x_pos = 0; var y_pos = 0;
    for (y = start_y; y < end_y; ++y) {
        for (bell = 1; bell < course.n_bells+1; ++bell) {
            x = course.changes[y].indexOf(bell);
            x_pos = sc.x_margin+(x  *sc.x_width)+sc.pixel_offset+sc.x_font_offset;
            y_pos = sc.y_margin+(y_0*sc.y_width)+sc.pixel_offset+sc.y_font_offset;
            context.fillText(bell, x_pos, y_pos);
        }
        y_0 += 1;
    }
}

function draw_place_notation(course, context, sc, nchanges) {
    // draw the place notation
    context.font = sc.pn_foncontext;
    var y = 0; var x_pos = 0; var y_pos = 0;
    for (y = 0; y < nchanges; ++y) {
        if (course.notation[y]) {
            x_pos = sc.pn_x_offset;
            y_pos = sc.y_margin+(y*sc.y_width)+sc.pixel_offset+sc.pn_y_offset;
            context.fillText(course.notation[y], x_pos, y_pos);
        }
    }
}

function draw_line(bell, course, context, sc, start_y, end_y, colour) {
    // draw the lines on the chart
    context.beginPath();
    context.strokeStyle = colour;
    context.lineCap="round";
    context.lineWidth = 4;

    var y_0 = 0; var y = 0; var x = 0;
    var x_pos = 0; var y_pos = 0;
    for (y = start_y; y < end_y; ++y) {
        x = course.changes[y].indexOf(bell);

        x_pos = sc.x_margin+(x  *sc.x_width)+sc.pixel_offset;
        y_pos = sc.y_margin+(y_0*sc.y_width)+sc.pixel_offset;

        context.lineTo(x_pos, y_pos);
        context.moveTo(x_pos, y_pos);
        y_0 += 1;
     }
     context.stroke();
     context.closePath();
}

function draw_lead_end_line(course, context, sc) {
    // draw in the lead_ends
    context.strokeStyle = sc.le_colour;
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(sc.x_le_margin+sc.pixel_offset,                              (sc.y_margin * 0.5)+sc.pixel_offset);
    context.lineTo(sc.x_le_margin+(course.n_bells*sc.x_width)+sc.pixel_offset,  (sc.y_margin * 0.5)+sc.pixel_offset);
    context.stroke();
    context.closePath();
}

function draw_all_lines(course, context, sc, start_y, end_y) {
    // draw the lines on the chart
    context.lineCap = "round";
    context.lineWidth = 4;

    var y_0 = 0; var y = 0; var x = 0;
    var x_pos = 0; var y_pos = 0;
    var bell = 0;
    for (bell = 1; bell <=course.n_bells; ++bell) {
        y_0 = 0;
        if (bell == 1) {
            context.strokeStyle = "rgba(255, 0, 0, 1.0)";
        } else if (bell == 2) {
            context.strokeStyle = "rgba(0, 0, 255, 1.0)";
        } else {
            context.strokeStyle = "rgba(0, 0, 0, 1.0)";
        }
        context.beginPath();
        for (y = start_y; y < end_y; ++y) {
            x = course.changes[y].indexOf(bell);

            x_pos = sc.x_margin+(x  *sc.x_width)+sc.pixel_offset;
            y_pos = sc.y_margin+(y_0*sc.y_width)+sc.pixel_offset;

            context.lineTo(x_pos, y_pos);
            context.moveTo(x_pos, y_pos);
            y_0 += 1;
        }
        context.stroke();
        context.closePath();
    }
}

function draw_blue_line(course) {

    // fact checkin g
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