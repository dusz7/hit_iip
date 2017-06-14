
function handleDataFile(e){
  var files = e.target.files;

  var f = files[0];

  var headItem = [];
  headItem = ["A1","A2","A3","A4","A5",
        "A6","A7","A8","A9","A10",
        "A11","A12","A13","A14","A15",
        "A16","A17","A18","A19","A20","Result"]
  var dataItem = [];

  var reader = new FileReader();

  reader.onload = function(e){

    var data = e.target.result;
    var lines = data.split('\n');

    $.each(lines,function(i,line){
      var val = $.trim(line);
      if(val != ''){
        var inLineData = val.split(' ');
        dataItem.push(inLineData);
      }
    })

    var headstr = '';
    var datastr = '';

    $.each(headItem, function(i, head) {
        headstr = headstr + '<th>' + head + '</th>'
    })
    $.each(dataItem, function(i, data) {
        datastr = datastr + '<tr>';
        $.each(data, function(j, val) {
            datastr = datastr + '<td>' + val + '</td>'
        })
        datastr = datastr + '</tr>';
    })
    var table = '<table class="table table-striped"><tr>' + headstr + '</tr><tbody>' + datastr + '</tbody></table>'

    $('#content').html($('#content').html() + table);

  }
  reader.readAsText(f);
}

$("#myFile").bind('change',handleDataFile);
