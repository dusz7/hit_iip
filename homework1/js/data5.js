
function handleDataFile(e){
  var files = e.target.files;

  var f = files[0];

  var headItem = [];
  headItem = ["Sepal_length","Sepal_width","Petal_length","Petal_width","Class"]
  var dataItem = [];

  var reader = new FileReader();

  reader.onload = function(e){

    var data = e.target.result;
    var lines = data.split('\n');

    $.each(lines,function(i,line){
      var val = $.trim(line);
      if(val != ''){
        var inLineData = val.split(',');
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
