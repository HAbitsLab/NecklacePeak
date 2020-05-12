function getUnixTime(dateString) {
  var obj = new Date(dateString);
  return obj.getTime();
}


// ========================================================================
// Class for Time Series data
// there always should be a column named "Time" which is the UNIX time stamp
// csvPath: path of the csv file
// name:    name of the div to be painted
// subset:  array of columns to be parsed
// example -> 'data/sensor.csv', 'necklace', ['Top', 'Bottom']

function TimeSeries(csvPath, name, subset, yrange, delay, div) {
  this.csvPath = csvPath;
  this.name = name;
  this.subset = subset;
  this.delay = delay;
  this.div = div;
  this.yrange = yrange;
}

TimeSeries.createUI = function(csvPath, name, subset, yrange, delay, fn) {
  var div = document.createElement('div');
  div.id = name;
  document.getElementById('contents').appendChild(div);

  $.get(csvPath, function(data) {
    Papa.parse(data, {
      header: true,
      fastMode: true,
      complete: function(results) {
        data = results.data;
        var header;

        if (typeof(subset) === 'undefined') {
          header = [];
          for (var i = 0; i < results.meta.fields.length; i++) {
            if (results.meta.fields[i] !== 'Time') {
              header.push(results.meta.fields[i]);
            }
          }
        } else {
          for (var i = 0; i < subset.length; i++) {
            if ($.inArray(subset[i], results.meta.fields) < 0) {
              throw 'Subset is invalid';
            }
          }
          header = subset;
        }

        var signals = [];
        var N = data.length;

        for (var i = 0; i < header.length; i++) {
          signals[header[i]] = [];
        }
        signals.Time = [];

        for (var i = 0; i < data.length; i++) {
          row = data[i];

          var date = new Date(parseInt(row.Time));
          if (isNaN(date.getTime())) {
            continue;
          }
          signals.Time.push(date);
          for (var j = 0; j < header.length; j++) {
            signals[header[j]].push(parseFloat(row[header[j]]));
          }
        }

        var traces = [];
        for (var i = 0; i < header.length; i++) {
          traces.push(
              {x: signals.Time, y: signals[header[i]], name: header[i]});
        }

        var layout = {
          paper_bgcolor: '#ccccff',
          showlegend: true,
          legend: {
            x: 1,
            y: 1,
            font: {
              size: 10.5,
              family: 'courier',
            }
          },
          autosize: true,
          margin: {l: 50, r: 130, b: 40, t: 5, pad: 0},
          height: 200,
          // xaxis: {rangeslider: {}},
          // yaxis: {'autorange': true}
          yaxis: {range: [yrange.ymin, yrange.ymax]}
        };

        Plotly.newPlot(div, traces, layout);

        div.on('plotly_relayout', function(data) {
          if (myVideoPlayer.paused() && ('xaxis.range' in data)) {
            var minTime = getUnixTime(data['xaxis.range'][0]);
            var maxTime = getUnixTime(data['xaxis.range'][1]);

            boundRange = maxTime - minTime;
            var absoluteTime = minTime + boundRange / 4;

            pubsubz.publish('timeMarker', {
              'timeMarker': absoluteTime,
              'minTime': minTime,
              'maxTime': maxTime
            });

            myVideoPlayer.currentTime(absoluteTimeToCamera(absoluteTime));
          }
        });
        fn(new TimeSeries(csvPath, name, subset, yrange, delay, div));
      }
    });
  });
};

TimeSeries.updateTime = function(topics, data) {
  var absoluteTime = data.timeMarker;
  var minTime = data.minTime;
  var maxTime = data.maxTime;
  var delay = this.delay;

  var update = {
    shapes: [{
      type: 'line',
      yref: 'paper',
      x0: absoluteTime + global_delay,
      y0: -0.1,
      x1: absoluteTime + global_delay,
      y1: 1.2,
      line: {
        color: 'red',
        width: 1.5,
      }
    }],
    xaxis: {range: [minTime + global_delay, maxTime + global_delay]}
    // rangeslider: {}},
    // yaxis: {range: [this.yrange.ymin, this.yrange.ymax]}
  };

  Plotly.relayout(this.div, update);
};
