// ========================================================================
function extraInfo() {
}

extraInfo.createUI = function(fn) {

    var divUnixTime = document.createElement('div');
    document.getElementById('extraInfo').appendChild(divUnixTime);

    var inputMinTime = document.createElement('input');
    inputMinTime.type = "text";
    inputMinTime.id = 'inputMinTime';
    divUnixTime.appendChild(inputMinTime);

    var inputMaxTime = document.createElement('input');
    inputMaxTime.type = "text";    
    inputMaxTime.id = 'inputMaxTime';
    divUnixTime.appendChild(inputMaxTime);

    var inputMarkerTime = document.createElement('input');
    inputMarkerTime.type = "text";
    inputMarkerTime.id = 'inputMarkerTime';
    divUnixTime.appendChild(inputMarkerTime);

    var divHumanTime = document.createElement('div');
    document.getElementById('extraInfo').appendChild(divHumanTime);

    var labelMinTime = document.createElement('LABEL');
    labelMinTime.type = "text";  
    labelMinTime.id = 'labelMinTime';
    divHumanTime.appendChild(labelMinTime);

    var linebreak = document.createElement("br");
    divHumanTime.appendChild(linebreak);
    var labelMaxTime = document.createElement('label');

    labelMaxTime.type = "text";  
    labelMaxTime.id = 'labelMaxTime';
    divHumanTime.appendChild(labelMaxTime);

    var linebreak = document.createElement("br");
    divHumanTime.appendChild(linebreak);

    var labelMarkerTime = document.createElement('label');
    labelMarkerTime.type = "text";
    labelMarkerTime.id = 'labelMarkerTime';
    divHumanTime.appendChild(labelMarkerTime);

    fn(new extraInfo());
}

extraInfo.updateTime = function(topics, data) {
    var absoluteTime = data.timeMarker;
    var minTime = data.minTime;
    var maxTime = data.maxTime;

    $("#inputMinTime").val(minTime);
    $("#inputMaxTime").val(maxTime);
    $("#inputMarkerTime").val(absoluteTime);

    $("#labelMinTime").html(new Date(minTime).toString());
    $("#labelMaxTime").html(new Date(maxTime).toString());
    $("#labelMarkerTime").html(new Date(absoluteTime).toString());
}
