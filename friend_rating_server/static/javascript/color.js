function getAtcoderRatingColor(rating) {
    if (rating < 400) {
        return "#808080";
    } else if (rating < 800) {
        return "#804000";
    } else if (rating < 1200) {
        return "#008000";
    } else if (rating < 1600) {
         return "#00C0C0";
    } else if (rating < 2000) {
        return "#0000FF";
    } else if (rating < 2400) {
        return "#C0C000";
    } else if (rating < 2800) {
        return "#FF8000";
    } else {
        return "#FF0000";
    }
}

function getCodeforcesRatingColor(rating) {
    if (rating < 1200) {
        return "gray";
    } else if (rating < 1400) {
        return "green";
    } else if (rating < 1600) {
        return "cyan";
    } else if (rating < 1900) {
        return "blue";
    } else if (rating < 2100) {
        return "violet";
    } else if (rating < 2400) {
        return "orange";
    } else if (rating < 3000) {
        return "red";
    } else {
        return "black";
    }
}

let atcoder_ratings = [400, 800, 1200, 1600, 2000, 2400, 2800, 4000];

let codeforces_ratings = [1200, 1400, 1600, 1900, 2100, 2400, 3000, 4000];


/*
@param rating point of the different color, function map rating to color
@return [the background data of graph, conifg of visual_map which show how rating match color]
*/
function get_line_graph_background_data(ratings, get_color) {
    let color_data = [];
    let visual_map_pieces = [];
    let pre = 0;
    for (let x of ratings) {
        color_data.push([
            {
                yAxis: pre.toString(),
                itemStyle: {
                    color: get_color(pre),
                    opacity: 0.8
                }
            },
            {
                yAxis: x.toString()
            }
        ]);
        visual_map_pieces.push({
            min: pre,
            max: x,
            color: get_color(pre)
        });
        pre = x;
    }
    return [color_data, visual_map_pieces];
}