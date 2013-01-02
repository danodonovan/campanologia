// Dan's n00b helper functions
function print(n) {
    document.write("<br />" + n + "</br />");
}

// extend the String prototype
String.prototype.contains_bell = function (obj) {
    "use strict"; var i = this.length;
    while (i--) {
        if (this[i] == obj) {
            return true;
        }
    }
    return false;
}

// extend the Array prototype
Array.prototype.contains = function (obj) {
    "use strict"; var i = this.length;
    while (i--) {
        if (this[i] == obj) {
            return true;
        }
    }
    return false;
}

Array.prototype.not_rounds = function (obj) {
    "use strict"; var i;
    for (i = 0; i < this.length; ++i) {
        if (this[i] != i+1) {
            return true;
        }
    }
    return false;
}

// extend the generic object prototype
Object.prototype.clone = function () {
    "use strict"; var newObj = (this instanceof Array) ? [] : {};
    for (var i in this) {
        if (i == 'clone') continue;
            if (this[i] && typeof this[i] == "object") {
                newObj[i] = this[i].clone();
        } else newObj[i] = this[i]
    } return newObj;
};

// ring some bells
function Course(n_bells, nchanges, raw_notation) {
    "use strict"; var MAX_ITER = 1280;
    var print_bells = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
    var place_bells = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'E', 'T', 'A', 'B', 'C', 'D'];

    // perform one change of the bells - either switch, or make places "place"
    var _change = function(bells, place) {
        if (place_bells.contains(place[0])) {
            if (/2|4|6|8|0|T|B|D/.test(place[0])) {
                place = 1 + place;
            }
        }

        var i = 0;
        while (i < bells.length-1) {
            if (place.contains_bell(place_bells[i]) || place.contains_bell(place_bells[i+1])) {
                i += 1;
            } else {
                var temp_bell = bells[i];
                bells[i] = bells[i+1];
                bells[i+1] = temp_bell;
                i += 2;
            }
        } 
        return bells;
    }

    function sanitise_notation() {
        // clean up the notation for the ringing algorithm
        var bells = []; var i; var nr = null; var lh = null;
        for (i = 0; i < n_bells; ++i) { bells[i] = print_bells[i]; }
        if (/LH/.test(raw_notation)) {
            nr = raw_notation.split("LH")[0];
            lh = raw_notation.split("LH")[1];
        } else {
            nr = raw_notation;
            lh = null;
        }

        var i = 0;
        var n_t = []; var n = [];
        var n_t_reset = false;

        // there are edge case problems for Orignal N and Cheeky Little Place Minimus
        if (nr.length == 1) {
            // if we're dealing with original even
            if (nr[0] == '-') {
                n = n.concat("X");
                n = n.concat("1");
                return [n, lh];
            }
            // if we're dealing with original odd
            if (/3|5|7|9|E|A|C/.test(nr[0])) {
                n = n.concat("X");
                n = n.concat("1");
                return [n, lh];
            }
            // if we're dealing with Cheeky Little Place
            else if (nr[0] == '1') {
                n = n.concat("14");
                n = n.concat("12");
                return [n, lh];
            }
        }

        while (i<nr.length) {
            if (n_t_reset) {
                n_t = [];
            }
            if (/-|X|x/.test(nr[i])) {
                if (n_t.length>0) {
                    n = n.concat(n_t.join(""));
                    n_t = [];
                }
                n = n.concat("X");
                n_t_reset = true;
            } else if (place_bells.contains(nr[i])) { 
                n_t = n_t.concat(nr[i]);
                n_t_reset = false;
            } else {
                n = n.concat(n_t.join(""));
                n_t_reset = true;
            }
            i += 1;
        }

        if (n_t.length != 0) {
            n = n.concat(n_t.join(""));
        }

        return [n, lh];
    }

    var s_not_lh = sanitise_notation();
    var notation = s_not_lh[0]; var lead_head = s_not_lh[1];

    var ring = function(n_bells, notation, lead_head) {
        // ring the method using notation provided

        var bells = []; var i; var changes = [nchanges]; var lead_ends = [];
        for (i = 0; i < n_bells; ++i) { bells[i] = i+1; }
        changes[0] = bells.clone();
        var l_i = 0; var p_i = 0; var reverse = false; var lead_end = false;
        var le_i = 0;

        while ((bells.not_rounds() || (l_i==0)) && (l_i < MAX_ITER)) {

            if ((!lead_end) || (!lead_head)) {
                bells = _change(bells, notation[p_i]);
            } else {
                bells = _change(bells, lead_end);
            }

            changes[l_i+1] = bells.clone();
            //  Just count the changes
            l_i += 1;

            // odd bell methods aren't tripped with lead_end = True
            if ((!lead_head) && (p_i == notation.length-1)) {
                le_i += 1;
                lead_ends[lead_ends.length] = l_i;
            }

            if (lead_end) {
				// keep a track of lead ends (only for lead_head exists methods)
                le_i += 1;
				lead_ends[lead_ends.length] = l_i;

                lead_end = false;
                p_i = 0;
                continue;
            }

            // if in first half, increase place notation counter - else decrease counter
            if (lead_head) {
                if (!reverse) { p_i += 1; }
                else { p_i -= 1; }
            } else {
                if (p_i == notation.length-1) { p_i = 0; }
                else { p_i += 1; }
            }

            // Mark the half lead and lead end
            if (p_i == notation.length-1) { reverse = true; }
            if (p_i < 0) { reverse = false; }

            // test to see if we are at a lead end
            if (p_i == -1) { lead_end = lead_head; } 
            else { lead_end = false; }
        }

        return {changes:changes, lead_ends:lead_ends};
    }
    // ring the changes 
    var method_rung = ring(n_bells, notation, lead_head);

    // I'm still working out how to use globals, and set 'this'
    this.changes = method_rung.changes;
    this.lead_ends = method_rung.lead_ends;
    this.notation = notation;
	this.n_bells = n_bells;
}

