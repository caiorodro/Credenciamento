let ID_EMPRESA = 0;

const listEmpresa = () => {
    const url = '/listEmpresa';
    const data = {
        idUser: idUser,
        name: '',
        email: '',
        keep: keep
    };

    const success = function (response) {
        const data = eval(response);
        refreshGrid(['gridEmpresa'], data);
    };

    doranAjax(url, data, success);
};

const newEmpresa = () => {
    $('#divFormEmpresa').modal();
    resetaFormEmpresa();

    setTimeout(() => {
        $('#TXT_RAZAO_SOCIAL').focus();
    }, 500);
};

const resetaFormEmpresa = () => {
    ID_EMPRESA = 0;
    $('#TXT_RAZAO_SOCIAL').val('');
    $('#TXT_NOME_FANTASIA').val('');
    $('#TXT_CNPJ').val('');
    $('#TXT_IE').val('');
    $('#TXT_ENDERECO').val('');
    $('#TXT_NUMERO').val('');
    $('#TXT_COMPLEMENTO').val('');
    $('#TXT_CEP').val('');
    $('#TXT_MUNICIPIO').val('');
    $('#TXT_UF').val('');
    $('#TXT_EMAIL').val('');
    $('#TXT_TELEFONE').val('');
    $('#TXT_CONTATO').val('');
};

const editEmpresa = (_ID_EMPRESA) => {
    ID_EMPRESA = _ID_EMPRESA;

    const url = '/getEmpresa';
    const data = { 
        ID_EMPRESA: ID_EMPRESA, 
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        let data1 = eval(response);
        data1 = eval(data1.message)[0];

        $('#TXT_RAZAO_SOCIAL').val(data1.RAZAO_SOCIAL);
        $('#TXT_NOME_FANTASIA').val(data1.NOME_FANTASIA);
        $('#TXT_CNPJ').val(data1.CNPJ);
        $('#TXT_IE').val(data1.IE);
        $('#TXT_ENDERECO').val(data1.ENDERECO);
        $('#TXT_NUMERO').val(data1.NUMERO);
        $('#TXT_COMPLEMENTO').val(data1.COMPLEMENTO);
        $('#TXT_CEP').val(data1.CEP);
        $('#TXT_MUNICIPIO').val(data1.MUNICIPIO);
        $('#TXT_UF').val(data1.UF);
        $('#TXT_EMAIL').val(data1.EMAIL);
        $('#TXT_TELEFONE').val(data1.TELEFONE);
        $('#TXT_CONTATO').val(data1.CONTATO);

        $('#divFormEmpresa').modal();

        setTimeout(() => {
            $('#TXT_RAZAO_SOCIAL').focus();
        }, 500);
    }

    doranAjax(url, data, success);
};

const saveEmpresa = () => {
    event.preventDefault();

    if ($('#TXT_RAZAO_SOCIAL').val().trim() == ''
        || $('#TXT_NOME_FANTASIA').val().trim() == ''
        || $('#TXT_ENDERECO').val().trim() == ''
        || $('#TXT_NUMERO').val().trim() == ''
        || $('#TXT_CEP').val().trim() == ''
        || $('#TXT_MUNICIPIO').val().trim() == ''
        || $('#TXT_UF').val().trim() == ''
        || $('#TXT_TELEFONE').val().trim() == ''
        || $('#TXT_EMAIL').val().trim() == '') {
        MensagemDeErro('Preencha todos os campos com *');
        return;
    }

    const url = '/saveEmpresa';

    const data = {
        ID_EMPRESA: ID_EMPRESA,
        RAZAO_SOCIAL: $('#TXT_RAZAO_SOCIAL').val(),
        NOME_FANTASIA: $('#TXT_NOME_FANTASIA').val(),
        CNPJ: $('#TXT_CNPJ').val(),
        IE: $('#TXT_IE').val(),
        ENDERECO: $('#TXT_ENDERECO').val(),
        NUMERO: $('#TXT_NUMERO').val(),
        COMPLEMENTO: $('#TXT_COMPLEMENTO').val(),
        CEP: $('#TXT_CEP').val(),
        MUNICIPIO: $('#TXT_MUNICIPIO').val(),
        UF: $('#TXT_UF').val(),
        EMAIL: $('#TXT_EMAIL').val(),
        TELEFONE: $('#TXT_TELEFONE').val(),
        CONTATO: $('#TXT_CONTATO').val(),
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        if (parseInt(ID_EMPRESA) > 0)
            $('#divFormEmpresa').modal('hide');

        resetaFormEmpresa();

        listEmpresa();
    };

    doranAjax(url, data, success);
};

const deleteEmpresa = (_ID_EMPRESA) => {
    MensagemDeConfirmacao('Deseja deletar o registro?', function () {
        const url = '/deleteEmpresa';

        const data = {
            ID_EMPRESA: _ID_EMPRESA,
            keep: keep,
            idUser: idUser
        };

        const success = function (response) {
            listEmpresa();
        }

        doranAjax(url, data, success);
    });
};

const refreshEmpresa = () => {
    event.preventDefault();
    listEmpresa();
};

const cancelEmpresa = () => {
    event.preventDefault();
    $('#divFormEmpresa').modal('hide');
};
