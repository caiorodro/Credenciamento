
const carregaEventoCredenciamento = () => {
    const url = '/carregaEventoCredenciamento';

    const data = {
        DATA: bsDate(),
        keep: keep,
        idUser: idUser
    };

    const success = function (response) {
        const data1 = response.message;

        const item = $('#CB_FILTRO_EVENTO');

        item.empty();
        
        item.append("<option value='0'>aqui...</option>");

        data1.map(function (item1) {
            item.append("<option value='" + item1.ID_EVENTO + "'>" +
                item1.TITULO_EVENTO + "</option>");
        });

        item.val(0);
    };

    doranAjax(url, data, success);
};

const listCredenciamento = () => {
    idEvento = parseInt($('#CB_FILTRO_EVENTO').val());

    if (idEvento > 0){
        const url = '/listCredenciamento';
        const data = {
            ID_EVENTO: idEvento,
            idUser: idUser,
            keep: keep
        };

        const success = function (response) {
            const data1 = eval(response);
            refreshGrid(['gridCredenciamento'], data1);
        };

        doranAjax(url, data, success);
    }
};

const adicionaPresenca = (_ID_EVENTO, _ID_CONVIDADO) => {

    const url = '/adicionaPresenca';
    const data = {
        ID_EVENTO: _ID_EVENTO,
        ID_CONVIDADO: _ID_CONVIDADO,
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        const data1 = eval(response);
        listCredenciamento();
    };

    doranAjax(url, data, success);
};

const deletePresenca = (ID_CREDENCIAMENTO) => {
    MensagemDeConfirmacao('Deseja deletar a presença?', function () {
        const url = '/deletePresenca';

        const data = {
            ID_CREDENCIAMENTO: ID_CREDENCIAMENTO,
            idUser: idUser,
            keep: keep
        };

        const success = function (response) {
            const data1 = eval(response);
            listCredenciamento();
        };

        doranAjax(url, data, success);
    });
};