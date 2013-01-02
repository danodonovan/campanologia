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
    context.lineCap="round";
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
