//对表格文件的处理：读取表格文件中的数据
function handleExcelFile(e) {
    var files = e.target.files;

    var i, f;
    for (i = 0, f = files[i]; i != files.length; ++i) {

        var reader = new FileReader();

        reader.onload = function(e) {
            var data = e.target.result;
            //表格文件：workbook
            var workbook = XLSX.read(data, {
                type: 'binary'
            });
            //表格文件的tab列表
            var sheet_name_list = workbook.SheetNames;
            var result = [];
            var dataFormulae = [];
            var headItem = [];
            var dataItem = [];
            var dataCsv = [];
            var headCode = [];
            var rowNum = 0;

            //对每个tab页的内容进行读取
            sheet_name_list.forEach(function(y) {
                //当前页
                var worksheet = workbook.Sheets[y];
                //转换数据格式
                var json = XLSX.utils.sheet_to_json(workbook.Sheets[y]);
                var formulae = XLSX.utils.sheet_to_formulae(workbook.Sheets[y]);
                var csv = XLSX.utils.sheet_to_formulae(workbook.Sheets[y]);
                if (json.length > 0) {
                    result = json;
                    dataCsv = csv;
                    dataFormulae = formulae;
                }
            });



            $.each(dataFormulae,function (j,head) {
                var headlist=head.split("='")
                if(/^[A-Z]1$/.test(headlist[0])){
                    headItem.push(headlist[1])
                }
            });

            $.each(result,function (i,val) {
                var data=[]
                $.each(headItem,function (k,head) {
                    val[head]!=undefined?data.push(val[head]):data.push("")
                })
                dataItem.push(data)
            });

            // $.each(dataCsv, function(j, head) {
            //     var headlist = head.split("='")
            //     rowNum = /^[A-Z]+(\d+)$/.exec(headlist[0])[1];
            //     headCode.indexOf(/^([A-Z]+)\d+$/.exec(headlist[0])[1]) == -1 ? headCode.push(/^([A-Z]+)\d+$/.exec(headlist[0])[1]) : '';
            // });
            // headCode = headCode.sort();
            // $.each(headCode, function(i, val) {
            //     // headItem[val] = '';
            // });
            // for (var i = 0; i < Number(rowNum) - 1; i++) {
            //     var obj = {};
            //     $.each(headCode, function(i, val) {
            //         obj[val] = '';
            //     })
            //     dataItem[i] = obj;
            // }
            // $.each(dataCsv, function(j, head) {
            //     var headlist = head.split("='")
            //     var code = /^([A-Z]+)\d+$/.exec(headlist[0])[1];
            //     var row = /^[A-Z]+(\d+)$/.exec(headlist[0])[1];
            //     if (row == 1) {
            //         headItem[code] = headlist[1]
            //     } else {
            //         dataItem[row - 2][code] = headlist[1];
            //     }
            // });

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

        };
        reader.readAsBinaryString(f);
    }

}

$('#myFile').bind('change', handleExcelFile);
