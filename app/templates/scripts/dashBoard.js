
const chartPeopleByEvents = () => {
    const url = '/chartPeopleByEvents';
    const data = {
        idUser: idUser,
        keep: keep,
        dateFrom: bsDateToString($('#TXT_FILTRO_DATA_EVENTO').val())
    };

    const success = function (response) {
        const data = eval(response.message);
        drawChart(data);
    };

    doranAjax(url, data, success);
};

const drawChart = (data1) => {

    const options = {
        fontName: 'Calibri',
        dataOpacity: 1.0,
        title: 'Presença / ausência por evento',
        height: _height = parseInt(h * .60),
        width: '100%',
        bars: 'horizontal',
        vAxis: {title: 'Convidados por evento', gridlines: { color: 'black' }, gridlines: { count: 10 } },
        hAxis: {title: 'Eventos', gridlines: { color: 'darkgray' }},
        seriesType: 'bars',

        backgroundColor: { fill: 'transparent' },
        isStacked: true,

        bar: { groupWidth: '60%' },
        legend: { position: 'bottom' },
        series: {
            0: { color: '#71B6F9' },
            1: { color: '#FFA401' },
            2: { color: 'green' },
            3: { color: 'purple' },
            4: { color: 'darkgray' },
            5: { color: '#43459d' },
        },
        titleTextStyle: {
            fontSize: 16,
            bold: true,
            italic: false,
        }
    };
    
    const data =  google.visualization.arrayToDataTable(data1);

    const chart = new google.visualization.ComboChart(document.getElementById('dashBoard1'));

    chart.draw(data, options);
};
