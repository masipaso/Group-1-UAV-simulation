var RealWorldCanvas = function(canvas_width, canvas_height, grid_width, grid_height) {
	// Create the element
	// ------------------
	gridColor = "#8b8b8b";
	drawLines = false;

	// Create the tag:
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px solid red'></canvas>";
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("body").append(canvas);

	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new RealWorldVisualization(canvas_width, canvas_height, grid_width, grid_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.drawGrid(drawLines, gridColor, data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};

var RealWorldVisualization = function(height, width, gridWidth, gridHeight, context) {
    var height = height;
    var width = width;
    var gridWidth = gridWidth;
	var gridHeight = gridHeight;
	var context = context;

	// Find cell size:
	var cellWidth = Math.floor(width / gridWidth);
	var cellHeight = Math.floor(height / gridHeight);

	// Find max radius of the circle that can be inscribed (fit) into the
    // cell of the grid.
	var maxR = Math.min(cellHeight, cellWidth)/2 - 1;

	// Draw all layers
	this.drawLayers = function(data) {
	    for (layer in data) {
		    this.drawLayer(data[layer]);
		}
	};

   // Calls the appropriate shape(agent)
    this.drawLayer = function(portrayalLayer) {
		for (var i in portrayalLayer) {
			var p = portrayalLayer[i];
            // Does the inversion of y positioning because of html5
            // canvas y direction is from top to bottom. But we
            // normally keep y-axis in plots from bottom to top.
            p.y = gridHeight - p.y - 1;
			if (p.Type == "Uav")
			    this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled, p.text, p.text_color);
			if (p.Type == "BaseStation")
			    this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.Filled, p.text, p.text_color);
			if (p.Type == "Obstacle")
			    return
			    this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.Filled, p.text, p.text_color);
		}
	};

	// DRAWING METHODS
	// =====================================================================

	/**
	Draw a circle in the specified grid cell.
	x, y: Grid co-ordinates
	r: Radius, as a multiple of cell size
	color: Code for the fill color
	fill: Boolean for whether or not to fill the circle.
        text: Inscribed text in rectangle.
        text_color: Color of the inscribed text.
        */
	this.drawCircle = function(x, y, radius, color, fill, text, text_color) {
		var cx = (x + 0.5) * cellWidth;
		var cy = (y + 0.5) * cellHeight;
		var r = radius * maxR;

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}

        // This part draws the text inside the Circle
        if (text !== undefined) {
                context.fillStyle = text_color;
                context.textAlign = 'center';
                context.textBaseline= 'middle';
                context.fillText(text, cx, cy);
        }

	};

	/**
	Draw a rectangle in the specified grid cell.
	x, y: Grid coords
	w, h: Width and height, [0, 1]
	color: Color for the rectangle
	fill: Boolean, whether to fill or not.
        text: Inscribed text in rectangle.
        text_color: Color of the inscribed text.
	*/
	this.drawRectangle = function(x, y, w, h, color, fill, text, text_color) {
		context.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;

		// Keep in the center of the cell:
		var x0 = (x + 0.5) * cellWidth - dx/2;
		var y0 = (y + 0.5) * cellHeight - dy/2;

		context.strokeStyle = color;
		context.fillStyle = color;
		if (fill)
			context.fillRect(x0, y0, dx, dy);
		else
			context.strokeRect(x0, y0, dx, dy);

            // This part draws the text inside the Rectangle
            if (text !== undefined) {
                    var cx = (x + 0.5) * cellWidth;
                    var cy = (y + 0.5) * cellHeight;
                    context.fillStyle = text_color;
                    context.textAlign = 'center';
                    context.textBaseline= 'middle';
                    context.fillText(text, cx, cy);
            }
    };

    /**
    Draw Grid lines in the full grid
    */

	this.drawGrid = function(drawLines, color, layers) {
	    var that = this;
		maxX = cellWidth * gridWidth;
		maxY = cellHeight * gridHeight;

		var position = {
		    coords: {
		        latitude: 40.753460,
		        longitude: -73.988869
		    }
		}

		var backgroundImage = new Image();
		var google_tile = "http://maps.google.com/maps/api/staticmap?sensor=false&center=" + position.coords.latitude + "," +
                        position.coords.longitude + "&zoom=16&size=" + width + "x"+ height + "&scale=2&maptype=satellite";
        backgroundImage.src = google_tile;

		// Drawing of the background
        backgroundImage.onload = function () {
            // Draw background image
            context.drawImage(backgroundImage, 0, 0, width, height);

            if(drawLines) {
		        context.beginPath();
        		context.strokeStyle = color || '#eee';
                // Draw horizontal grid lines
                for(var y=0; y<=maxY; y+=cellHeight) {
                    context.moveTo(0, y+0.5);
                    context.lineTo(maxX, y+0.5);
                }

                for(var x=0; x<=maxX; x+= cellWidth) {
                    context.moveTo(x+0.5, 0);
                    context.lineTo(x+0.5, maxY);
                }
                context.stroke();
            }

            // Draw everything that is not in the background
		    that.drawLayers(layers);
        };



	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, width, height);
		context.beginPath();
	};

}