
// ========================================================================
// Class for annotating Points

function AnnotationPoint(jsonFile, start, stop, step, name, div) {
    this.start = start;
    this.stop = stop;
    this.step = step;
    this.name = name;
    this.div = div;
    this.minTime = start;
    this.maxTime = stop;
}

AnnotationPoint.createUI = function(jsonFile, start, stop, step, name, fn) {
    var div = document.createElement('div');
    div.id = name;
    document.getElementById('contents').appendChild(div);

    var divPlotly = document.createElement('div');
    divPlotly.id = name + '_plotly';
    div.appendChild(divPlotly);

    var divControl = document.createElement('div');
    divControl.id = name + '_control';
    divControl.style.backgroundColor = 'rgb(255, 255, 153)';
    div.appendChild(divControl);

    var exportButton = document.createElement('button');
    exportButton.id = 'export';
    exportButton.innerHTML = 'Export labels';
    divControl.appendChild(exportButton);

    divControl.insertAdjacentHTML('beforeend', '<a id="downloadAnchorElem" style="display:none"></a>');

    var annTemplate = {
            x: 2,
            y: 5,
            xref: 'x',
            yref: 'y',
            text: 'Eating',
            showarrow: true,
            arrowhead: 7,
            ax: 0,
            ay: -40,
            bordercolor: '#000000',
            borderwidth: 1,
            borderpad: 1,
            bgcolor: '#ff7f0e',
            opacity: 0.8
    }

    var layout = {
        autosize: true,
        paper_bgcolor: '#ffff99',
        title: '',
        showlegend: true,
        legend: {
            x: 1,
            y: 1,
            font: { size: 10.5,
                    family: 'courier',
                    }
        },
        yaxis: {
            tickvals:[0,1],
            title: ''
        },
        xaxis: {title: ''},
        margin: {
            l: 50,
            r: 130,
            b: 40,
            t: 5,
            pad: 0
        },
        height: 150
    };

    var serialize = function(dictAnns) {
        return Object.values(dictAnns);
    };

    var range = function(start, stop, step) {
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }

        var result = {};
        result.x = [];
        result.y = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.x.push(new Date(i));
            result.y.push(0);
        }
        return result;
    }; 

    $.getJSON(jsonFile, function(json) {

        var dictAnns = {};
        for (var key in json) {
            var newAnn = JSON.parse(JSON.stringify(annTemplate));
            newAnn.x = key;
            newAnn.y = 0;
            newAnn.text = json[key];
            dictAnns[new Date(key).toISOString()] = newAnn;
        }

        var data = range(start, stop, step);

        layout.annotations = serialize(dictAnns);
        Plotly.plot(divPlotly, [{x: data.x, y: data.y, name: 'annotation'}], layout, {editable: true});

        exportButton.onclick = function() {
            var results = {};
            
            var syncValue = parseInt($('#videodelay').val());

            for (key in dictAnns) {
                if (dictAnns.hasOwnProperty(key)) {
                    var value = dictAnns[key];
                    
                    dateTimeValue = new Date(value.x);
                    dateTimeValue = new Date(dateTimeValue.getTime() + syncValue);
                    var dateText = dateTimeValue.getFullYear()+"-"+("0"+(dateTimeValue.getMonth()+1)).slice(-2)+"-"+("0"+dateTimeValue.getDate()).slice(-2)+" "+("0"+dateTimeValue.getHours()).slice(-2)+":"+("0"+dateTimeValue.getMinutes()).slice(-2)+":"+("0"+dateTimeValue.getSeconds()).slice(-2)+"."+(dateTimeValue.getMilliseconds()+"000").slice(0,3);
                    
                    results[dateText] = value.text;
                }
            }

            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(results,Object.keys(results).sort(),2));
            var dlAnchorElem = document.getElementById('downloadAnchorElem');
            dlAnchorElem.setAttribute("href",     dataStr     );
            dlAnchorElem.setAttribute("download", "labels.json");
            dlAnchorElem.click();
        }

        var that = new AnnotationPoint(jsonFile, start, stop, step, name, divPlotly);
       
        divPlotly.on('plotly_click', function(data) {
            console.log(data.points[0].x);
            console.log(data.points[0].y);

            if (myVideoPlayer.paused()) {

                var key = new Date(data.points[0].x).toISOString();

                if (key in dictAnns) {
                    delete dictAnns[key];
                } else {
                    var newAnn = JSON.parse(JSON.stringify(annTemplate));
                    newAnn.x = data.points[0].x;
                    newAnn.y = data.points[0].y;
                    dictAnns[new Date(data.points[0].x).toISOString()] = newAnn;
                };

                var update = {
                    annotations: serialize(dictAnns),
                    xaxis: {range: [that.minTime, that.maxTime]}
                }

                Plotly.relayout(divPlotly, update, {editable:true});                
            }
        });

        fn(that);
    })
}


AnnotationPoint.updateTime = function(topics, data) {
    var absoluteTime = data.timeMarker;
    var minTime = data.minTime;
    var maxTime = data.maxTime;

    var update = {
        shapes: [{
            type: 'line',
            yref: 'paper',
            x0: absoluteTime,
            y0: -0.1,
            x1: absoluteTime,
            y1: 1.2,
            line: {
                color: 'red',
                width: 1.5,
            } 
        }],
        xaxis: {range: [minTime, maxTime]}
    };

    this.minTime = minTime;
    this.maxTime = maxTime;

    Plotly.relayout(this.div, update);
}