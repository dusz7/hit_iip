function handleDataFile(e) {
    var files = e.target.files;

    var headItem = [];
    headItem = ["车辆标识", "触发事件", "运营状态",
    "GPS时间", "GPS经度","GPS纬度", "GPS速度","GPS方位", "GPS状态"]
    var dataItem = [];

    var i, f;
    var file_num = files.length;
    var complete_num = 0;

    function completeReader(){
      complete_num++;
      console.log(complete_num);
      if(complete_num == file_num){
        console.log("complete_num");
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
    }

    for (i = 0, f = files[i]; i != file_num; ++i) {

        var reader = new FileReader();

        reader.onload = function(e) {

            var data = e.target.result;
            var lines = data.split('\n');

            $.each(lines, function(i, line) {
                var val = $.trim(line);
                if (val != '') {
                    var inLineData = val.split(',');
                    dataItem.push(inLineData);
                }
            })

        }
        reader.onloadend = function(e){
          completeReader();
        }
        reader.readAsText(f);
    }

}

$("#myFile").bind('change', handleDataFile);
