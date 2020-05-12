// ========================================================================
// Class for Label Data
// The CSV file has no header, and has two columns
// First column is starting point of the duration
// Second column is end point of the duration
function LabelData(csvPath, name, div) {
    this.csvPath = csvPath;
    this.name = name;
    this.div = div;
}

LabelData.createUI = function(csvPath, name, fn) {
    var div = document.createElement('div');
    div.id = name;
    document.getElementById('contents').appendChild(div);

    $.get(csvPath, function(data) {
        Papa.parse(data, {
            header: false,
            fastMode: true,
            complete: function(results) {
                data = results.data;
                var signals = [];
                var N = data.length;

                signals.Time = [];
                signals.Y = [];

                for (var i = 0; i < data.length; i++) {
                    row = data[i];

                    timeStart = parseInt(row[0]);
                    timeEnd = parseInt(row[1]);

                    var start = new Date(timeStart);
                    var end = new Date(timeEnd);

                    if ((isNaN(start.getTime())) || (isNaN(end.getTime()))) {
                        continue;
                    } 

                    signals.Time.push(start);
                    signals.Y.push(0);
                    signals.Time.push(start);
                    signals.Y.push(1);
                    signals.Time.push(end);
                    signals.Y.push(1);
                    signals.Time.push(end);
                    signals.Y.push(0);
                }

                var traces = [{
                    x: signals.Time,
                    y: signals.Y,
                    name: name,
                    line: {color: 'green'}
                }];

                var layout = {
                    showlegend: true,
                    autosize: true,
                    legend: {
                        x: 1,
                        y: 1,
                        font: { size: 10.5,
                                family: 'courier',
                                }
                    },
                    margin: {
                        l: 50,
                        r: 130,
                        b: 5,
                        t: 5,
                        pad: 0
                    },
                    height: 50,
                    yaxis: {tickvals:[0,1]}
                };

                Plotly.newPlot(div, traces, layout);

                fn(new LabelData(csvPath, name, div));
            }
        });
    });
};

LabelData.updateTime = function(topics, data) {
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
    Plotly.relayout(this.div, update);
};
