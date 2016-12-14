var RealWorldCanvas = function(canvas_width, canvas_height, grid_width, grid_height) {
	// Defined options
	// ---------------
	gridColor = "#8b8b8b";
	drawLines = false;

	// Styles
	// ----------
	$("body").css("margin", 0);
	$("h2").css("text-align", "center");
	$("h2").css("width", canvas_width);

	// Create stuff (TO BE REMOVED -> Add to template)
	// ------------
	var controlsTag = "<div class='controls'></div>"
	$("body").append(controlsTag);
	var toggleTag = "<button class='toggleButton'>Toggle!</button>"
	$(".controls").append(toggleTag);

	$(".toggleButton").click(function() {
	    if ($("canvas.realWorld").is(":visible")) {
	        $("canvas.realWorld").css("display", "none");
	    } else {
	        $("canvas.realWorld").css("display", "block");
	    }
	})

    // Create background canvas
    // ------------------------
    // Create the tag
    var backgroundCanvasTag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
    backgroundCanvasTag += "style='position: absolute; left: 0; display: block'></canvas>";
    // Append it to the body
    var backgroundCanvas = $(backgroundCanvasTag)[0];
    $("body").append(backgroundCanvas);
    // Get the context
    var backgroundContext = backgroundCanvas.getContext("2d");

    // Create foreground canvas
    // ------------------------
	// Create the tag
	var foregroundCanvasTag = "<canvas class='realWorld' width='" + canvas_width + "' height='" + canvas_height + "' ";
	foregroundCanvasTag += "style='position: absolute; left: 0;'></canvas>";
	// Append it to body
	var foregroundCanvas = $(foregroundCanvasTag)[0];
	$("body").append(foregroundCanvas);
	// Get the context
	var foregroundContext = foregroundCanvas.getContext("2d");

	// Create drawing controller
	// -------------------------
	var drawController = new RealWorldVisualization(canvas_width, canvas_height, grid_width, grid_height, foregroundContext, backgroundContext);

	this.render = function(data) {
		drawController.resetCanvas();
		drawController.drawGrid(drawLines, gridColor, data);
	};

	this.reset = function() {
		drawController.resetCanvas();
	};

};

var RealWorldVisualization = function(height, width, gridWidth, gridHeight, foregroundContext, backgroundContext) {
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
	this.maxR = Math.min(cellHeight, cellWidth)/2 - 1;

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
//			    this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled, p.text, p.text_color);
			    this.drawUav(p.x, p.y);
			if (p.Type == "BaseStation") {
			    this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.Filled, p.text, p.text_color);
			}
			if (p.Type == "Obstacle") {
			    return
			    this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.Filled, p.text, p.text_color);
			}
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
		var r = radius || 1;
		r = r * this.maxR;

		foregroundContext.beginPath();
		foregroundContext.arc(cx, cy, r, 0, Math.PI * 2, false);
		foregroundContext.closePath();

		foregroundContext.strokeStyle = color;
		foregroundContext.stroke();

		if (fill) {
			foregroundContext.fillStyle = color;
			foregroundContext.fill();
		}

        // This part draws the text inside the Circle
        if (text !== undefined) {
                foregroundContext.fillStyle = text_color;
                foregroundContext.textAlign = 'center';
                foregroundContext.textBaseline= 'middle';
                foregroundContext.fillText(text, cx, cy);
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
		foregroundContext.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;

		// Keep in the center of the cell:
		var x0 = (x + 0.5) * cellWidth - dx/2;
		var y0 = (y + 0.5) * cellHeight - dy/2;

		foregroundContext.strokeStyle = color;
		foregroundContext.fillStyle = color;
		if (fill)
			foregroundContext.fillRect(x0, y0, dx, dy);
		else
			foregroundContext.strokeRect(x0, y0, dx, dy);

            // This part draws the text inside the Rectangle
            if (text !== undefined) {
                    var cx = (x + 0.5) * cellWidth;
                    var cy = (y + 0.5) * cellHeight;
                    foregroundContext.fillStyle = text_color;
                    foregroundContext.textAlign = 'center';
                    foregroundContext.textBaseline= 'middle';
                    foregroundContext.fillText(text, cx, cy);
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
            backgroundContext.drawImage(backgroundImage, 0, 0, width, height);

            if(drawLines) {
		        backgroundContext.beginPath();
        		backgroundContext.strokeStyle = color || '#eee';
                // Draw horizontal grid lines
                for(var y=0; y<=maxY; y+=cellHeight) {
                    backgroundContext.moveTo(0, y+0.5);
                    backgroundContext.lineTo(maxX, y+0.5);
                }

                for(var x=0; x<=maxX; x+= cellWidth) {
                    backgroundContext.moveTo(x+0.5, 0);
                    backgroundContext.lineTo(x+0.5, maxY);
                }
                backgroundContext.stroke();
                backgroundContext.stroke();
            }

            // Draw everything that is not in the background
		    that.drawLayers(layers);
        };

	};


    /**
    Draw a Uav in the specified grid cell.
    x, y: Grid co-ordinates
    */
    this.drawUav = function(x, y) {
        var uavImage = new Image();
        uavImage.src = 'data:image/png;base64,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'

        // Calculate position
		var x0 = (x + 0.5) * cellWidth - cellWidth / 1;
		var y0 = (y + 0.5) * cellHeight - cellHeight / 1;

         // Draw image
         uavImage.onload = function () {
            foregroundContext.drawImage(uavImage, x0, y0, cellWidth * 2, cellHeight * 2);
         };
    };

	this.resetCanvas = function() {
		foregroundContext.clearRect(0, 0, width, height);
		foregroundContext.beginPath();
	};

}