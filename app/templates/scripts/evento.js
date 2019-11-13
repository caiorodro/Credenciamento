let ID_EVENTO = 0;
let ID_CONVIDADO = 0;

const listEvento = () => {
    const url = '/listEvento';
    const data = {
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        const data = eval(response);
        refreshGrid(['gridEventos'], data);
    };

    doranAjax(url, data, success);
};

const newEvento = () => {
    $('#divFormEvento').modal();
    resetaFormEvento();
    listEmpresas();

    setTimeout(() => {
        $('#TXT_TITULO_EVENTO').focus();
        refreshGridConvidado([], 120);
    }, 500);
};

const resetaFormEvento = () => {
    ID_EVENTO = 0;
    $('#TXT_TITULO_EVENTO').val('');
    $('#TXT_DATA_EVENTO').val(bsDate());
    $('#TXT_HORA_EVENTO').val('19:00');
    $('#TXT_OBSERVACOES').val('');
    
    resetaFormConvidado();
};

const resetaFormConvidado = (_focus) => {
    $('#TXT_NOME_CONVIDADO').val('');
    $('#TXT_CELULAR_CONVIDADO').val('');
    ID_CONVIDADO = 0;

    if (_focus) 
        $('#TXT_NOME_CONVIDADO').focus();
};

const editEvento = (_ID_EVENTO) => {

    const act = () => {

        ID_EVENTO = _ID_EVENTO;

        const url = '/getEvento';
        const data = { 
            ID_EVENTO: ID_EVENTO, 
            idUser: idUser,
            keep: keep
        };

        const success = function (response) {
            let data1 = eval(response);
            data1 = eval(data1.message)[0];

            $('#TXT_TITULO_EVENTO').val(data1.TITULO_EVENTO);
            $('#CB_ID_EMPRESA').val(data1.ID_EMPRESA);
            $('#TXT_DATA_EVENTO').val(data1.DATA_EVENTO.substring(0, data1.DATA_EVENTO.indexOf(' ')));
            $('#TXT_HORA_EVENTO').val(data1.DATA_EVENTO.substring(data1.DATA_EVENTO.indexOf(' ') + 1));
            $('#TXT_OBSERVACOES').val(data1.OBSERVACAO);
            $('#divFormEvento').modal();

            setTimeout(() => {
                $('#TXT_TITULO_EVENTO').focus();
                listConvidados();
            }, 500);
        };

        doranAjax(url, data, success);
    };

    listEmpresas(act);
};

const saveEvento = () => {
    event.preventDefault();

    [$('#TXT_TITULO_EVENTO').val(), 
     $('#TXT_DATA_EVENTO').val().trim(), 
     $('#TXT_HORA_EVENTO').val().trim()].map((item) => {
        if (item.length == 0){
            MensagemDeErro('Preencha todos os campos com *');
            return;
        }
    });

    const url = '/saveEvento';

    const dataHora = bsDateToString($('#TXT_DATA_EVENTO').val()) + ' ' + $('#TXT_HORA_EVENTO').val();

    const data = {
        ID_EVENTO: ID_EVENTO,
        TITULO_EVENTO: $('#TXT_TITULO_EVENTO').val(),
        ID_EMPRESA: $('#CB_ID_EMPRESA').val(),
        DATA_EVENTO: dataHora,
        OBSERVACOES: $('#TXT_OBSERVACOES').val(),
        ID_CONVIDADO: ID_CONVIDADO,
        NOME_CONVIDADO: $('#TXT_NOME_CONVIDADO').val().trim(),
        CELULAR_CONVIDADO: $('#TXT_CELULAR_CONVIDADO').val(),
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {

        ID_EVENTO = parseInt(response.message[0]);

        FormConvidado();
        $('#TXT_NOME_CONVIDADO').focus();

        const _refresh = [listEvento, listConvidados, carregaEventoCredenciamento];

        _refresh.map((item) => {
            item();
        });
    };

    doranAjax(url, data, success);
};

const listConvidados = () => {
    const url = '/listConvidados';
    const data = {
        ID_EVENTO: ID_EVENTO,
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        const data1 = eval(response);
        refreshGridConvidado(data1, 120);
    };

    doranAjax(url, data, success);
};

const deleteEvento = (_ID_EVENTO) => {
    MensagemDeConfirmacao('Deseja deletar o registro?', function () {
        const url = '/deleteEvento';

        const data = {
            ID_EVENTO: _ID_EVENTO,
            keep: keep,
            idUser: idUser
        };

        const success = function (response) {
            listEvento();
        }

        doranAjax(url, data, success);
    });
};

const deleteConvidado = (_ID_CONVIDADO) => {
    MensagemDeConfirmacao('Deseja deletar o(a) convidado(a)?', function () {
        const url = '/deleteConvidado';

        const data = {
            ID_CONVIDADO: _ID_CONVIDADO,
            keep: keep,
            idUser: idUser
        };

        const success = function (response) {
            resetaFormConvidado();
            listConvidados();
        }

        doranAjax(url, data, success);
    });
};

const refreshEvento = () => {
    event.preventDefault();
    listEvento();
};

const cancelEvento = () => {
    event.preventDefault();
    $('#divFormEvento').modal('hide');
};

const listEmpresas = (act) => {
    const url = '/listEmpresas';

    const data = {
        keep: keep,
        idUser: idUser
    };

    const success = function (response) {
        const data1 = response.message;

        const item = $('#CB_ID_EMPRESA');

        item.empty();

        data1.map(function (item1) {
            item.append("<option value='" + item1.ID_EMPRESA + "'>" +
                item1.NOME_FANTASIA + "</option>");
        });

        if (act) act();
    };

    doranAjax(url, data, success);
};

let gridX;

const refreshGridConvidado = (data, _height) => {
    if (!_height)
        _height = parseInt(h * .38);

    const item = 'gridConvidados';

    if (gridX) {
        $('#' + item).DataTable().clear().destroy();
        gridX = undefined;
    }

    gridX = $('#' + item).DataTable({
        data: data,
        scrollY: _height,
        searching: true,
        pageLength: 100,
        "columnDefs": [
            {
                "targets": [0],
                "visible": false,
                "searchable": false
            }
        ],
        select: {
            style: 'single'
        },
        language: ptBr
    });

    gridX.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            const rowData = gridX.rows( indexes ).data().toArray()[0];

            editConvidado(parseInt(rowData[0]), rowData[1], rowData[2]);
        }
    });
};

const editConvidado = (idConvidado, nomeConvidado, celularConvidado) => {
    ID_CONVIDADO = idConvidado;
    
    $('#TXT_NOME_CONVIDADO').val(nomeConvidado);
    $('#TXT_CELULAR_CONVIDADO').val(celularConvidado);

    $('#TXT_NOME_CONVIDADO').focus();
};